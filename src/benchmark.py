import subprocess
import time
import statistics

PROJECT_PATH = "dummy"
CHECKERS = {
    "mypy": ["uv", "run", "mypy", PROJECT_PATH],
    "pyright": ["uv", "run", "pyright", PROJECT_PATH],
    "ty": ["uv", "run", "ty", "check", PROJECT_PATH],
    "pyrefly": ["uv", "run", "pyrefly", "check", PROJECT_PATH],
}
REPEATS = 1


def run_benchmark(cmd):
    times = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        times.append(time.perf_counter() - start)
    return statistics.mean(times), statistics.stdev(times)


def main():
    results = {}
    for name, cmd in CHECKERS.items():
        print(f"Running {name}...")
        mean, std = run_benchmark(cmd)
        results[name] = (mean, std)

    print("\n=== Benchmark Results (avg over {} runs) ===".format(REPEATS))
    for name, (mean, std) in results.items():
        print(f"{name:<10} {mean:.2f}s ± {std:.2f}s")


if __name__ == "__main__":
    main()
