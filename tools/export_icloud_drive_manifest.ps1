<#
.SYNOPSIS
Export a local iCloud Drive manifest for private duplicate reconciliation.

.DESCRIPTION
Scans a locally synced iCloud Drive folder on Windows and writes a CSV compatible
with tools/reconcile_file_manifests.py. Metadata is collected without downloading
cloud-only placeholders. Use -IncludeHash to calculate SHA-256 only for files that
are already locally available. Keep the resulting manifest private; paths and names
may contain sensitive information.
#>

[CmdletBinding()]
param(
    [string]$RootPath,
    [string]$OutputCsv = (Join-Path (Get-Location) "icloud_drive_manifest.csv"),
    [switch]$IncludeHash,
    [switch]$IncludeHidden,
    [long]$MaxHashBytes = 2147483648
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-ICloudRoot {
    param([string]$RequestedRoot)
    if ($RequestedRoot) {
        return (Resolve-Path -LiteralPath $RequestedRoot -ErrorAction Stop).Path
    }

    $candidates = @(
        (Join-Path $env:USERPROFILE "iCloudDrive"),
        (Join-Path $env:USERPROFILE "iCloud Drive"),
        (Join-Path $env:USERPROFILE "Apple\iCloudDrive")
    ) | Select-Object -Unique

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Container) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    throw "Could not locate iCloud Drive. Re-run with -RootPath 'C:\path\to\iCloudDrive'."
}

function Get-MimeType {
    param([string]$Extension)
    switch ($Extension.ToLowerInvariant()) {
        ".pdf"  { "application/pdf" }
        ".docx" { "application/vnd.openxmlformats-officedocument.wordprocessingml.document" }
        ".doc"  { "application/msword" }
        ".xlsx" { "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" }
        ".xls"  { "application/vnd.ms-excel" }
        ".csv"  { "text/csv" }
        ".txt"  { "text/plain" }
        ".jpg"  { "image/jpeg" }
        ".jpeg" { "image/jpeg" }
        ".png"  { "image/png" }
        default  { "application/octet-stream" }
    }
}

function Test-CloudOnlyPlaceholder {
    param([System.IO.FileInfo]$File)
    $offline = [System.IO.FileAttributes]::Offline
    $recallOnOpen = [System.IO.FileAttributes]::RecallOnOpen
    $recallOnDataAccess = [System.IO.FileAttributes]::RecallOnDataAccess
    return (($File.Attributes -band $offline) -ne 0) -or
           (($File.Attributes -band $recallOnOpen) -ne 0) -or
           (($File.Attributes -band $recallOnDataAccess) -ne 0)
}

$root = Resolve-ICloudRoot -RequestedRoot $RootPath
$outputPath = [System.IO.Path]::GetFullPath($OutputCsv)
$outputDirectory = Split-Path -Parent $outputPath
if ($outputDirectory -and -not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$getChildItemArgs = @{
    LiteralPath = $root
    File = $true
    Recurse = $true
    ErrorAction = "SilentlyContinue"
}
if ($IncludeHidden) { $getChildItemArgs["Force"] = $true }

$rows = foreach ($file in Get-ChildItem @getChildItemArgs) {
    $relativePath = [System.IO.Path]::GetRelativePath($root, $file.FullName)
    $cloudOnly = Test-CloudOnlyPlaceholder -File $file
    $hash = ""
    $hashStatus = "NotRequested"

    if ($IncludeHash) {
        if ($cloudOnly) {
            $hashStatus = "CloudOnlyOrOffline"
        }
        elseif ($file.Length -gt $MaxHashBytes) {
            $hashStatus = "SkippedOverMaxHashBytes"
        }
        else {
            try {
                $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                $hashStatus = "SHA256"
            }
            catch {
                $hashStatus = "HashFailed: $($_.Exception.Message)"
            }
        }
    }

    [PSCustomObject]@{
        provider = "iCloud Drive"
        path = $relativePath
        name = $file.Name
        size = $file.Length
        modified_time = $file.LastWriteTimeUtc.ToString("o")
        content_hash = $hash
        mime_type = Get-MimeType -Extension $file.Extension
        url = ""
        local_state = $(if ($cloudOnly) { "CloudOnlyOrOffline" } else { "LocallyAvailable" })
        hash_status = $hashStatus
    }
}

$rows | Sort-Object path | Export-Csv -LiteralPath $outputPath -NoTypeInformation -Encoding UTF8

$summary = [PSCustomObject]@{
    root_path = $root
    output_csv = $outputPath
    file_count = @($rows).Count
    locally_available = @($rows | Where-Object local_state -eq "LocallyAvailable").Count
    cloud_only_or_offline = @($rows | Where-Object local_state -eq "CloudOnlyOrOffline").Count
    hashed = @($rows | Where-Object content_hash -ne "").Count
}

$summary | ConvertTo-Json -Depth 3
