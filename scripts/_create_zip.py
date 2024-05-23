import zipfile
from pathlib import Path
from typing import Final

CLONE_DIR: Final = Path("/tmp/pycon-italia-2024/")
ZIP_PATH: Final = Path("/tmp/pycon-italia-2024.zip")

PACKAGE_DIR = "what/"


def main() -> None:
    assert CLONE_DIR.exists(), "Run scripts/_clone_repo.py"

    print(f"Creating {ZIP_PATH}")

    # zip directory in ZIP_PATH
    with zipfile.ZipFile(ZIP_PATH, mode='w') as zf:
        for directory, _, filenames in (CLONE_DIR / PACKAGE_DIR).walk():
            for filename in filenames:
                # Use relative path inside the zip file. Otherwise, it becomes /tmp/x.zip/tmp/what/*
                zip_path = (directory / filename).relative_to(CLONE_DIR)

                zf.write(directory / filename, zip_path)


if __name__ == '__main__':
    main()
