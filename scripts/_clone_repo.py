import shutil
import subprocess
from pathlib import Path
from typing import Final

GIT_REPO: Final = "https://github.com/brycebeagle/pycon-italia-2024-python.git"
CLONE_DIR: Final = Path("/tmp/pycon-italia-2024/")


def main() -> None:
    if CLONE_DIR.exists():
        shutil.rmtree(CLONE_DIR)

    subprocess.run(["git", "clone", GIT_REPO, CLONE_DIR], check=True)


if __name__ == '__main__':
    main()
