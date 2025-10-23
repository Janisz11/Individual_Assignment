import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
PLOTS_DIR = ROOT / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATHS = {
    "python": ROOT / "benchmarks_python" / "results" / "matrix_bench_python.csv",
    "java":   ROOT / "benchmarks_java"   / "results" / "matrix_bench_java.csv",
    "c":      ROOT / "benchmark_c"       / "results" / "matrix_bench_c.csv",
}


LANG_ORDER = ["java", "c", "python"]

def load_csv(path: Path):
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                rows.append({
                    "language": row["language"].strip().lower(),
                    "size": int(row["size"]),
                    "execution_time_s": float(row["execution_time_s"]),
                    "memory_usage_mb": float(row["memory_usage_mb"]),
                })
            except Exception:
                pass
    return rows

def build_index():

    metrics = {lang: {} for lang in LANG_ORDER}
    all_sizes = set()
    for lang, path in CSV_PATHS.items():
        for row in load_csv(path):
            s = row["size"]
            all_sizes.add(s)
            metrics[lang][s] = (row["execution_time_s"], row["memory_usage_mb"])
    sizes_sorted = sorted(all_sizes)
    return sizes_sorted, metrics

def barplot_grouped(sizes, metrics, value_idx, ylabel, title, outfile):

    if not sizes:
        return

   
    data_by_lang = {}
    for lang in LANG_ORDER:
        vals = []
        for s in sizes:
            if s in metrics[lang]:
                vals.append(metrics[lang][s][value_idx])
            else:
                vals.append(np.nan) 
        data_by_lang[lang] = np.array(vals, dtype=float)

   
    x = np.arange(len(sizes))
    width = 0.25  
    offsets = np.linspace(-width, width, num=len(LANG_ORDER)) 

    plt.figure()
    for i, lang in enumerate(LANG_ORDER):
        heights = data_by_lang[lang]
        
        mask = ~np.isnan(heights)
        plt.bar(x[mask] + offsets[i], heights[mask], width=width, label=lang.capitalize())

    plt.title(title)
    plt.xlabel("Matrix size (n)")
    plt.ylabel(ylabel)
    plt.xticks(x, [str(s) for s in sizes])
    plt.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / outfile, dpi=200, bbox_inches="tight")
    plt.close()

def main():
    sizes, metrics = build_index()


    barplot_grouped(
        sizes=sizes,
        metrics=metrics,
        value_idx=0,
        ylabel="Execution time (s)",
        title="Execution time vs size — grouped by language",
        outfile="bar_time_all_languages.png",
    )

    
    barplot_grouped(
        sizes=sizes,
        metrics=metrics,
        value_idx=1,
        ylabel="Memory usage (MB)",
        title="Memory usage vs size — grouped by language",
        outfile="bar_memory_all_languages.png",
    )

    print(f"[OK] Bar plots saved in {PLOTS_DIR}")

if __name__ == "__main__":
    main()
