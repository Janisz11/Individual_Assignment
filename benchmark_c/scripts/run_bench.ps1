param(
  [Parameter(Mandatory = $true)][int]$MatrixSize,
  [Parameter(Mandatory = $true)][int]$Rounds
)

$ErrorActionPreference = 'Stop'
[System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$cRoot = Split-Path -Parent $scriptDir
$srcDir = Join-Path $cRoot "src"
$targetDir = Join-Path $cRoot "target"
$resultsDir = Join-Path $cRoot "results"
$exePath = Join-Path $targetDir "matrix_bench"
$csvPath = Join-Path $resultsDir "matrix_bench_c.csv"

New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null

function Ensure-CsvHeader {
  if (-not (Test-Path $csvPath) -or (Get-Item $csvPath).Length -eq 0) {
    "language,size,execution_time_s,memory_usage_mb" | Out-File -FilePath $csvPath -Encoding UTF8
  }
}


Write-Host "==> Compiling C benchmark..."
if ($IsLinux) {
  & gcc -O3 -march=native -o "$exePath" "$srcDir/matrix.c" "$srcDir/runner.c"
} else {
  & gcc -O3 -march=native -o "$exePath.exe" "$srcDir\matrix.c" "$srcDir\runner.c" -lpsapi
}


Write-Host "==> Running: size=$MatrixSize rounds=$Rounds"

if ($IsLinux) {
  $output = bash -c "$exePath $MatrixSize $Rounds"
} else {
  $output = & "$exePath.exe" $MatrixSize $Rounds
}

$parts = $output.Trim().Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)
if ($parts.Count -lt 2) {
  throw "Unexpected runner output: $output"
}

$avg = [double]$parts[0]
$mem = [double]$parts[1]

Ensure-CsvHeader
$line = [string]::Format([System.Globalization.CultureInfo]::InvariantCulture, "c,{0},{1:F6},{2:F2}", $MatrixSize, $avg, $mem)
Add-Content -Path $csvPath -Value $line
Write-Host "Appended -> $csvPath"
