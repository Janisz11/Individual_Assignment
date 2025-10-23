
import sys
from pathlib import Path


THIS_FILE = Path(__file__).resolve()
BP_ROOT = THIS_FILE.parents[1]            
SRC = BP_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import os
import csv
import time
import tracemalloc
from matrix import random_matrix, matmul_basic

LANGUAGE = "python"
RESULTS_DIR = BP_ROOT / "results"
CSV_PATH = RESULTS_DIR / "matrix_bench_python.csv"


def _ensure_header():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["language", "size", "execution_time_s", "memory_usage_mb"])


def test_matrix_multiplication_benchmark(benchmark):
    """
    R rounds -> record per-round time+peak locally, but write ONLY averages to CSV (to match Java).
    """
    n = int(os.environ.get("MATRIX_N", "256"))
    rounds = int(os.environ.get("MATRIX_RUNS", "5"))

    A = random_matrix(n)
    B = random_matrix(n)

    times = []
    peaks = []

    def run_once():
        tracemalloc.start()
        t0 = time.perf_counter()
        _ = matmul_basic(A, B)
        elapsed = time.perf_counter() - t0
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(elapsed)
        peaks.append(peak_bytes / (1024 * 1024))

    
    benchmark.pedantic(run_once, rounds=rounds, iterations=1)

    avg_time = sum(times) / len(times)
    avg_peak = sum(peaks) / len(peaks)

    _ensure_header()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([LANGUAGE, n, f"{avg_time:.6f}", f"{avg_peak:.2f}"])
