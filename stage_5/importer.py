import importlib.util
import subprocess
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec, ExtensionFileLoader
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType


class GitHubRustFinder(MetaPathFinder):
    def __init__(self, package: str, git_repo: str):
        self.package = package
        self.git_repo = git_repo

    def find_spec(
            self,
            fullname: str,
            path: str | None,
            target: ModuleType | None = None,
    ) -> ModuleSpec | None:

        if fullname != self.package:
            return None

        repo_clone = self._clone_repo()
        extension_file = self._build_extension(repo_clone)

        spec = importlib.util.spec_from_loader(
            name=fullname,
            loader=ExtensionFileLoader(self.package, str(extension_file)),
            origin=str(extension_file),
            is_package=True,
        )
        spec.submodule_search_locations = []

        return spec

    def _clone_repo(self) -> Path:
        temp_dir = TemporaryDirectory(delete=False)
        temp_dir_path = Path(temp_dir.name)

        subprocess.run(["git", "clone", self.git_repo, temp_dir_path], check=True)

        return temp_dir_path

    def _build_extension(self, rust_project_dir: Path) -> Path:
        subprocess.run(["cargo", "build", "--release"], cwd=rust_project_dir, check=True)

        so_file = rust_project_dir / "target" / "release" / f"lib{self.package}.so"
        assert so_file.exists()

        return so_file
