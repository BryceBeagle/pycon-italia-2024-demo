# Import from a zipfile using our own MetaPathFinder

import sys
from typing import Final

from stage_4.finder import GitHubFinder

GITHUB_REPO: Final = "BryceBeagle/pycon-italia-2024-python"

sys.meta_path.append(GitHubFinder(GITHUB_REPO))

from what import FooBar

print(FooBar.hello_world)

import what
print(what.__file__)