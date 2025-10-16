# Comparison of Python type checkers performance

How long does it take to type check the [scikit-learn codebase](https://github.com/scikit-learn/scikit-learn)?

This benchmark compares 4 Python type checkers

- [mypy](https://github.com/python/mypy)
- [pyright](https://github.com/microsoft/pyright)
- [pyrefly](https://github.com/facebook/pyrefly)
- [ty](https://github.com/astral-sh/ty)

## Run the benchmark

- Install type checkers

```bash
uv sync
```

- Run the benchmark (git clone scikit-learn + run all type checkers)

```bash
uv run src/dummy.py            # git clone codebase in dummy/
uv run src/benchmark.py        # run the benchmark
```
