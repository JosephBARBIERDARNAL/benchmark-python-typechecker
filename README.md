# Comparison of Python type checkers performance

How long does it take to type check the [scikit-learn codebase](https://github.com/scikit-learn/scikit-learn)?

![Barplot of a benchmark of all major Python type checkers](benchmark.png)

This benchmark compares 4 Python type checkers

- [mypy](https://github.com/python/mypy)
- [pyright](https://github.com/microsoft/pyright)
- [pyrefly](https://github.com/facebook/pyrefly)
- [ty](https://github.com/astral-sh/ty)

<br>

## Run the benchmark

- Install type checkers & plotting dependencies (matplotlib + theme)

```bash
uv sync
```

- Run the benchmark (it will git clone scikit learn codebase locally first)

```bash
uv run benchmark.py
```
