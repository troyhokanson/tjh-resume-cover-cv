param(
    [string]$RegistryCsv = "",
    [string]$OutputDir = "build_logs/cloud_inventory",
    [string[]]$Roots = @()
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptPath = Join-Path $PSScriptRoot "cloud_evidence_inventory.py"

if (-not (Test-Path $scriptPath)) {
    throw "Inventory script not found: $scriptPath"
}

$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    $pythonCommand = @("py", "-3")
} else {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        throw "Python 3 was not found. Install Python 3 or run this from an environment where python/py is available."
    }
    $pythonCommand = @("python")
}

$argsList = @($scriptPath, "--output-dir", (Join-Path $repoRoot $OutputDir))

if ($RegistryCsv) {
    $resolvedRegistry = Resolve-Path $RegistryCsv
    $argsList += @("--registry-csv", $resolvedRegistry.Path)
}

foreach ($root in $Roots) {
    if ($root) {
        $argsList += @("--root", $root)
    }
}

Write-Host "Running read-only cloud evidence inventory..." -ForegroundColor Cyan
Write-Host "No files will be moved, renamed, deleted, or uploaded." -ForegroundColor Yellow

if ($pythonCommand.Count -eq 2) {
    & $pythonCommand[0] $pythonCommand[1] @argsList
} else {
    & $pythonCommand[0] @argsList
}

if ($LASTEXITCODE -ne 0) {
    throw "Inventory failed with exit code $LASTEXITCODE"
}

Write-Host "Inventory complete. Review:" -ForegroundColor Green
Write-Host (Join-Path $repoRoot $OutputDir)
