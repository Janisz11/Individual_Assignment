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
