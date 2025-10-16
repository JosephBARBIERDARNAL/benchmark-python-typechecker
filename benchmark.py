import subprocess
import math
import time
import statistics
import matplotlib.pyplot as plt
import morethemes as mt
from pathlib import Path

mt.set_theme("ft")

REPO_URL = "https://github.com/scikit-learn/scikit-learn.git"
TARGET_DIR: Path = Path("codebase")


PROJECT_PATH = "codebase"
CHECKERS: dict = {
    "mypy": ["uv", "run", "mypy", PROJECT_PATH],
    "pyright": ["uv", "run", "pyright", PROJECT_PATH],
    "ty": ["uv", "run", "ty", "check", PROJECT_PATH],
    "pyrefly": ["uv", "run", "pyrefly", "check", PROJECT_PATH],
}
REPEATS = 5


def run_benchmark(cmd):
    times: list = []
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

    results: dict = {}
    for name, cmd in CHECKERS.items():
        print(f"Running {name}...")
        mean, std = run_benchmark(cmd)
        results[name] = (mean, std)

    print("\n=== Benchmark Results (avg over {} runs) ===".format(REPEATS))
    for name, (mean, std) in results.items():
        print(f"{name:<10} {mean:.2f}s ± {std:.2f}s")

    checkers: list = list(results.keys())
    means: list = [results[c][0] for c in checkers]
    stds: list = [results[c][1] for c in checkers]
    std_errors = [s / math.sqrt(REPEATS) if REPEATS > 1 else 0.0 for s in stds]

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(checkers, means, height=0.6)

    for bar, val, se in zip(bars, means, std_errors):
        ax.text(
            bar.get_width() + 0.05,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f} sec (±{se:.2f})",
            ha="left",
            va="center",
            fontsize=9,
        )

    fig.text(
        x=0.5,
        y=0.98,
        s="Python Type Checker Benchmark",
        size=16,
        ha="center",
        va="top",
    )

    fig.text(
        x=0.5,
        y=0.92,
        s=f"Type checking the entire scikit-learn codebase {REPEATS} times",
        fontsize=12,
        color="grey",
        va="top",
        ha="center",
    )

    plt.savefig("benchmark.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
