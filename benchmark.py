import subprocess
import time
import statistics
import matplotlib.pyplot as plt
import morethemes as mt
from pathlib import Path

mt.set_theme("ft")

REPO_URL = "https://github.com/scikit-learn/scikit-learn.git"
TARGET_DIR = Path("codebase")


PROJECT_PATH = "codebase/sklearn/cross_decomposition/tests"
CHECKERS = {
    "mypy": ["uv", "run", "mypy", PROJECT_PATH],
    "pyright": ["uv", "run", "pyright", PROJECT_PATH],
    "ty": ["uv", "run", "ty", "check", PROJECT_PATH],
    "pyrefly": ["uv", "run", "pyrefly", "check", PROJECT_PATH],
}
REPEATS = 10


def run_benchmark(cmd):
    times = []
    print(PROJECT_PATH)
    for _ in range(REPEATS):
        start = time.perf_counter()
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        times.append(time.perf_counter() - start)
    return statistics.mean(times), statistics.stdev(times)


def main():
    if TARGET_DIR.exists():
        print("Updating existing scikit-learn repo...")
        subprocess.run(["git", "-C", str(TARGET_DIR), "pull"], check=True)
    else:
        print("Cloning scikit-learn repo...")
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, str(TARGET_DIR)], check=True
        )
    print("Codebase ready at:", TARGET_DIR.resolve())

    results = {}
    for name, cmd in CHECKERS.items():
        print(f"Running {name}...")
        mean, std = run_benchmark(cmd)
        results[name] = (mean, std)

    print("\n=== Benchmark Results (avg over {} runs) ===".format(REPEATS))
    for name, (mean, std) in results.items():
        print(f"{name:<10} {mean:.2f}s ± {std:.2f}s")

    checkers = list(results.keys())
    means = [results[c][0] for c in checkers]
    stds = [results[c][1] for c in checkers]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(checkers, means, yerr=stds, capsize=5)
    ax.set_title("Python Type Checker Benchmark")
    ax.set_ylabel("Average Runtime (s)")
    ax.set_xlabel("Checker")

    for bar, val in zip(bars, means):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{val:.2f}s",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    text = f"Project: {PROJECT_PATH}\nRepeats: {REPEATS}\nCommand runner: uv"
    fig.text(0.01, 0.01, text, fontsize=8, va="bottom", ha="left")
    plt.savefig("benchmark.png", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
