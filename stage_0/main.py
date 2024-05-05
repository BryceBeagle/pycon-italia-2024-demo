import sys
from pathlib import Path
from typing import Final

CLONE_DIR: Final = Path("/tmp/pycon-italia-2024/")
assert CLONE_DIR.exists()

sys.path.insert(0, str(CLONE_DIR))

from what import FooBar
print(FooBar.hello_world)
