param(
  [int[]]$Sizes = @(64,128,256),
  [int]$Rounds = 5
)

$ErrorActionPreference = 'Stop'

[System.Threading.Thread]::CurrentThread.CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture

$pythonBench = "benchmarks_python"
$javaBench   = "benchmarks_java"
$cBench      = "benchmark_c"

$csvPaths = @(
  "$pythonBench\results\matrix_bench_python.csv",
  "$javaBench\results\matrix_bench_java.csv",
  "$cBench\results\matrix_bench_c.csv"
)

Write-Host "==> Cleaning old CSVs..."
foreach ($path in $csvPaths) {
  if (Test-Path $path) {
    Remove-Item $path -Force
    Write-Host "Removed $path"
  }
}

Write-Host "`n==> Running all benchmarks..."
foreach ($size in $Sizes) {
  Write-Host "`n--- Matrix size = $size ---"

  Write-Host ">>> Python"
  & python ".\benchmarks_python\scripts\run_bench.py" $size $Rounds

  Write-Host ">>> Java"
  & ".\benchmarks_java\scripts\run_bench.ps1" $size $Rounds

  Write-Host ">>> C"
  & ".\benchmark_c\scripts\run_bench.ps1" $size $Rounds
}

Write-Host "`n✅ All benchmarks completed successfully."
