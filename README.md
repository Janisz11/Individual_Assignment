##  How to Run Everything

###  Prerequisites
Make sure you have installed:
- **Python 3.12+**
- **Java 17+ (JDK)**
- **GCC** (for compiling C code)
- **PowerShell** (for running `.ps1` scripts)
- **matplotlib** (for plots)
- **pytest-benchmark** (for Python benchmarking)

To install required Python packages:
```powershell
pip install matplotlib pytest pytest-benchmark

to run benchmarks
.\scripts_top\run_all.ps1 -Sizes 10,50,100,200,400 -Rounds 10

This script will:

Clean up old CSV files.

Run all three benchmarks (Python, Java, and C).

Save results to:

benchmarks_python/results/matrix_bench_python.csv

benchmarks_java/results/matrix_bench_java.csv

benchmark_c/results/matrix_bench_c.csv

To generate plots
.\scripts_top\make_plots.ps1

Run Individual Benchmarks
Python
python .\benchmarks_python\scripts\run_bench.py

Java
cd benchmarks_java
mvn clean package
java -jar .\target\benchmarks-java-jar-with-dependencies.jar

c
.\benchmark_c\scripts\run_bench.ps1 200 10

## Common Issues

### Windows: Java Compilation Error (BOM)

If you encounter a compilation error like:
```
[ERROR] illegal character: '\ufeff'
```

This is caused by UTF-8 BOM (Byte Order Mark) in Java files. Fix it by running this PowerShell script in the `benchmarks_java` directory:
```powershell
Get-ChildItem -Path ".\src" -Filter "*.java" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $utf8NoBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($_.FullName, $content, $utf8NoBom)
    Write-Host "Fixed: $($_.FullName)"
}
```

Or in VS Code:
1. Open the Java file
2. Click on the encoding in the bottom-right corner
3. Select "Save with Encoding"
4. Choose **"UTF-8"** (without BOM)

### Windows: C Compilation Error (sys/resource.h)

The C benchmark uses Windows-specific APIs for memory measurement. Make sure to compile with:
```powershell
gcc -O3 -march=native -o target\matrix_bench.exe src\matrix.c src\runner.c -lpsapi
```

The `-lpsapi` flag links the Windows Process Status API library.