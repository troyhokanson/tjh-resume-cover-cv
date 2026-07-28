[CmdletBinding()]
param(
    [Parameter()]
    [string[]]$SourceRoot,

    [Parameter(Mandatory = $true)]
    [string]$GoogleDriveRoot,

    [Parameter()]
    [string]$DestinationRoot = "Career Evidence\00_Source Documents\Cloud Intake",

    [Parameter()]
    [string]$ManifestDirectory = (Join-Path $PSScriptRoot "private-manifests"),

    [Parameter()]
    [switch]$IncludeCloudOnly,

    [Parameter()]
    [switch]$Execute
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-DefaultSourceRoots {
    $candidates = @(
        [pscustomobject]@{ Label = "OneDrive"; Path = $env:OneDriveConsumer },
        [pscustomobject]@{ Label = "OneDrive"; Path = $env:OneDrive },
        [pscustomobject]@{ Label = "OneDrive"; Path = (Join-Path $env:USERPROFILE "OneDrive") },
        [pscustomobject]@{ Label = "iCloud Drive"; Path = (Join-Path $env:USERPROFILE "iCloudDrive") },
        [pscustomobject]@{ Label = "iCloud Drive"; Path = (Join-Path $env:USERPROFILE "iCloud Drive") }
    )

    $seen = @{}
    foreach ($candidate in $candidates) {
        if (-not $candidate.Path) {
            continue
        }

        if (-not (Test-Path -LiteralPath $candidate.Path -PathType Container)) {
            continue
        }

        $resolved = (Resolve-Path -LiteralPath $candidate.Path).Path
        $key = $resolved.ToLowerInvariant()
        if (-not $seen.ContainsKey($key)) {
            $seen[$key] = $true
            [pscustomobject]@{
                Label = $candidate.Label
                Path  = $resolved
            }
        }
    }
}

function Resolve-SourceRoots {
    param([string[]]$RequestedRoots)

    if ($RequestedRoots -and $RequestedRoots.Count -gt 0) {
        $resolved = foreach ($root in $RequestedRoots) {
            $path = (Resolve-Path -LiteralPath $root).Path
            [pscustomobject]@{
                Label = (Split-Path -Leaf $path)
                Path  = $path
            }
        }
        return @($resolved)
    }

    return @(Get-DefaultSourceRoots)
}

function Get-SafeLabel {
    param([string]$Value)

    $invalid = [IO.Path]::GetInvalidFileNameChars()
    $result = $Value
    foreach ($character in $invalid) {
        $result = $result.Replace([string]$character, "_")
    }
    return $result.Trim()
}

function Get-RecordClass {
    param([string]$RelativePath)

    $value = $RelativePath.ToLowerInvariant()

    if ($value -match "health|medical|fmla|worker.?comp|psych|therapy|pera|va.claim|disability") {
        return "restricted-health-employment"
    }

    if ($value -match "case|court|victim|suspect|evidence|icac|ectf|forensic|disposition|complaint") {
        return "restricted-case-court"
    }

    if ($value -match "training|post|certif|award|commend|assignment|resume|cover.letter|achievement") {
        return "career-evidence"
    }

    return "unclassified-review"
}

function Test-NeedsHydration {
    param([IO.FileInfo]$File)

    $attributeText = $File.Attributes.ToString()
    return $attributeText -match "Offline|RecallOnDataAccess|RecallOnOpen"
}

function Get-RelativePath {
    param(
        [string]$BasePath,
        [string]$FullPath
    )

    $baseWithSeparator = $BasePath.TrimEnd(
        [IO.Path]::DirectorySeparatorChar,
        [IO.Path]::AltDirectorySeparatorChar
    ) + [IO.Path]::DirectorySeparatorChar

    if (-not $FullPath.StartsWith($baseWithSeparator, [StringComparison]::OrdinalIgnoreCase)) {
        throw "The file path is not inside the expected source root: $FullPath"
    }

    return $FullPath.Substring($baseWithSeparator.Length)
}

function Get-HashSafe {
    param([string]$Path)

    try {
        return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    catch {
        return $null
    }
}

$sources = @(Resolve-SourceRoots -RequestedRoots $SourceRoot)
if ($sources.Count -eq 0) {
    throw "No local OneDrive or iCloud Drive folder was found. Pass -SourceRoot with one or more local folders."
}

$resolvedGoogleDrive = (Resolve-Path -LiteralPath $GoogleDriveRoot).Path
$resolvedDestination = Join-Path $resolvedGoogleDrive $DestinationRoot

foreach ($source in $sources) {
    if ($resolvedDestination.StartsWith($source.Path, [StringComparison]::OrdinalIgnoreCase)) {
        throw "The Google Drive destination cannot be inside a source folder: $($source.Path)"
    }
}

if (-not (Test-Path -LiteralPath $ManifestDirectory)) {
    New-Item -ItemType Directory -Path $ManifestDirectory | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$manifestPath = Join-Path $ManifestDirectory "cloud-inventory-$timestamp.csv"
$summaryPath = Join-Path $ManifestDirectory "cloud-summary-$timestamp.txt"
$records = [Collections.Generic.List[object]]::new()

foreach ($source in $sources) {
    $sourceLabel = Get-SafeLabel -Value $source.Label
    $files = Get-ChildItem -LiteralPath $source.Path -File -Recurse -Force |
        Where-Object {
            $_.Name -notlike "~`$*" -and
            $_.Extension -notin @(".tmp", ".partial", ".crdownload")
        }

    foreach ($file in $files) {
        $relativePath = Get-RelativePath -BasePath $source.Path -FullPath $file.FullName
        $needsHydration = Test-NeedsHydration -File $file
        $destinationPath = Join-Path (Join-Path $resolvedDestination $sourceLabel) $relativePath
        $classification = Get-RecordClass -RelativePath $relativePath
        $sourceHash = $null
        $destinationHash = $null
        $status = "inventory-only"
        $detail = ""

        if ($needsHydration -and -not $IncludeCloudOnly) {
            $status = "needs-hydration"
            $detail = "Skipped until the source file is kept/downloaded locally."
        }
        else {
            $sourceHash = Get-HashSafe -Path $file.FullName
            if (-not $sourceHash) {
                $status = "source-read-error"
                $detail = "The source could not be read or hashed."
            }
            elseif (Test-Path -LiteralPath $destinationPath -PathType Leaf) {
                $destinationHash = Get-HashSafe -Path $destinationPath
                if ($destinationHash -and $destinationHash -eq $sourceHash) {
                    $status = "duplicate-identical"
                    $detail = "Destination already contains the same bytes."
                }
                else {
                    $status = "conflict-different"
                    $detail = "Destination path exists with different bytes; nothing was overwritten."
                }
            }
            elseif (-not $Execute) {
                $status = "planned-copy"
                $detail = "Dry run only."
            }
            else {
                $destinationDirectory = Split-Path -Parent $destinationPath
                if (-not (Test-Path -LiteralPath $destinationDirectory)) {
                    New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null
                }

                try {
                    [IO.File]::Copy($file.FullName, $destinationPath, $false)
                    [IO.File]::SetLastWriteTimeUtc($destinationPath, $file.LastWriteTimeUtc)
                    $destinationHash = Get-HashSafe -Path $destinationPath

                    if ($destinationHash -eq $sourceHash) {
                        $status = "copied-verified"
                        $detail = "Copied and verified by SHA-256."
                    }
                    else {
                        $status = "copy-verification-failed"
                        $detail = "The copied file did not match the source hash."
                    }
                }
                catch {
                    $status = "copy-error"
                    $detail = $_.Exception.Message
                }
            }
        }

        $records.Add([pscustomobject]@{
            SourceLabel      = $sourceLabel
            RelativePath    = $relativePath
            SizeBytes       = $file.Length
            ModifiedUtc     = $file.LastWriteTimeUtc.ToString("o")
            SHA256          = $sourceHash
            Classification  = $classification
            NeedsHydration   = $needsHydration
            DestinationPath = $destinationPath
            DestinationHash = $destinationHash
            Status           = $status
            Detail           = $detail
            InventoryTimeUtc = (Get-Date).ToUniversalTime().ToString("o")
        })
    }
}

$records | Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8

$statusCounts = $records |
    Group-Object -Property Status |
    Sort-Object -Property Name

$summaryLines = [Collections.Generic.List[string]]::new()
$summaryLines.Add("Cloud storage inventory and safe-copy summary")
$summaryLines.Add("Inventory time (UTC): $((Get-Date).ToUniversalTime().ToString("o"))")
$summaryLines.Add("Mode: $(if ($Execute) { 'COPY' } else { 'DRY RUN' })")
$summaryLines.Add("Destination: $resolvedDestination")
$summaryLines.Add("Source roots:")
foreach ($source in $sources) {
    $summaryLines.Add("  - $($source.Label): $($source.Path)")
}
$summaryLines.Add("Status counts:")
foreach ($count in $statusCounts) {
    $summaryLines.Add("  - $($count.Name): $($count.Count)")
}
$summaryLines.Add("Manifest: $manifestPath")

$summaryLines | Set-Content -LiteralPath $summaryPath -Encoding UTF8
$summaryLines | ForEach-Object { Write-Host $_ }

if (($records | Where-Object Status -eq "copy-verification-failed").Count -gt 0) {
    throw "At least one copied file failed SHA-256 verification. Review the local manifest."
}

Write-Host "Source files were not deleted, moved, renamed, or modified."
