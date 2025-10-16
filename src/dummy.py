import subprocess
from pathlib import Path

REPO_URL = "https://github.com/scikit-learn/scikit-learn.git"
TARGET_DIR = Path("dummy")


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


if __name__ == "__main__":
    main()
