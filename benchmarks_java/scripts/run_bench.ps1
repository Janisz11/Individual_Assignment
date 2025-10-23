param(
  [Parameter(Mandatory=$true)][int]$MatrixSize,
  [Parameter(Mandatory=$true)][int]$Rounds
)

$ErrorActionPreference = 'Stop'


$scriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$javaRoot    = Split-Path -Parent $scriptDir
$projectRoot = Split-Path -Parent $javaRoot


Set-Location $javaRoot
Write-Host "==> Building Java benchmark (Maven)..."
mvn -q -DskipTests package


$jar = Join-Path $javaRoot "target\benchmarks-java-jar-with-dependencies.jar"
if (-not (Test-Path $jar)) {
  throw "JAR not found: $jar"
}


Set-Location $projectRoot
Write-Host "==> Running: size=$MatrixSize rounds=$Rounds"
& java -jar $jar $MatrixSize $Rounds
