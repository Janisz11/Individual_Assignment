Write-Host "Generating benchmark plots..."
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "make_plots.py"

if (-not (Test-Path $pythonScript)) {
    Write-Host "Error: make_plots.py not found in $scriptDir"
    exit 1
}

try {
    python $pythonScript
    Write-Host "Plots successfully generated in the 'plots' folder."
} catch {
    Write-Host "An error occurred while generating plots:"
    Write-Host $_.Exception.Message
    exit 1
}
