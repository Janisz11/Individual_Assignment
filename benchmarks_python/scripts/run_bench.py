import sys
import os
import pytest
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: python benchmarks_python/scripts/run_bench.py <matrix_size> <number_of_tests>")
        sys.exit(1)

    n = sys.argv[1]
    runs = sys.argv[2]

    
    os.environ["MATRIX_N"] = str(n)
    os.environ["MATRIX_RUNS"] = str(runs)

    
    script_path = Path(__file__).resolve()
    bp_root = script_path.parents[1]          
    project_root = bp_root.parent            
    test_path = bp_root / "tests" / "test_bench_matrix.py"
    src_path = bp_root / "src"

    if not test_path.exists():
        print(f"ERROR: test file not found: {test_path}")
        sys.exit(2)

   
    prev_pp = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = (str(src_path) + os.pathsep + prev_pp) if prev_pp else str(src_path)

   
    os.chdir(project_root)
    sys.exit(pytest.main(["-q", str(test_path)]))


if __name__ == "__main__":
    main()
