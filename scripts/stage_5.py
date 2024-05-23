# Import from a Rust extension that is both cloned and built during import-time

import sys
from typing import Final

from pycon_italia_2024.stage_5.finder import GitHubRustFinder

RUST_PACKAGE: Final = "what"
GIT_REPO: Final = "https://github.com/BryceBeagle/pycon-italia-2024-rust"

sys.meta_path.append(GitHubRustFinder(RUST_PACKAGE, GIT_REPO))

from what import FooBar

print(FooBar.hello_world)
