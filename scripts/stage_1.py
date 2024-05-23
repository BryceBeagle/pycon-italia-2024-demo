# Import from a zipfile using the built-in zipimport logic

import sys
from pathlib import Path
from typing import Final

ZIP_PATH: Final = Path("/tmp/pycon-italia-2024.zip")
assert ZIP_PATH.exists()

sys.path.append(str(ZIP_PATH))
from what import FooBar

print(FooBar.hello_world)
