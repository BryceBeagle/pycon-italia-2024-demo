# Import from a zipfile using our own MetaPathFinder

import sys
from pathlib import Path
from typing import Final

from pycon_italia_2024.stage_3.finder import ZipFinder

ZIP_PATH: Final = Path("/tmp/pycon-italia-2024.zip")
assert ZIP_PATH.exists()

sys.meta_path.append(ZipFinder(ZIP_PATH))

from what import FooBar

print(FooBar.hello_world)
