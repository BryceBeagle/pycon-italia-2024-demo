import importlib.util
import shutil
import urllib.request
from functools import cache
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec, SourceFileLoader
from pathlib import PurePath, Path
from tempfile import NamedTemporaryFile
from types import ModuleType
from urllib.error import HTTPError


class GitHubFinder(MetaPathFinder):
    def __init__(self, repo: str):
        self.repo = repo

    def find_spec(
            self,
            fullname: str,
            path: str | None,
            target: ModuleType | None = None,
    ) -> ModuleSpec | None:

        package = PurePath(fullname) / "__init__.py"
        module = PurePath(fullname).with_suffix(".py")

        # If both foo/ and foo.py exist, foo/ takes priority
        if (downloaded_file := self._download_file(package)) is not None:
            return self._new_spec(fullname, package, downloaded_file, is_package=True)
        if (downloaded_file := self._download_file()) is not None:
            return self._new_spec(fullname, module, downloaded_file, is_package=False)

        return None

    @cache
    def _download_file(self, file_path: PurePath) -> Path | None:
        # Technically this should have a way to clean up if the module cache is cleared
        temp_file = NamedTemporaryFile(delete=False)

        url = self._file_url(file_path)
        try:
            with urllib.request.urlopen(url) as response:
                shutil.copyfileobj(response, temp_file)
        except HTTPError:
            # Naively assume file doesn't exist
            return None

        return Path(temp_file.name)

    def _new_spec(
            self, fullname: str, repo_path: PurePath, download_file: Path, *, is_package: bool
    ) -> ModuleSpec:
        origin = self._file_url(repo_path)

        spec = importlib.util.spec_from_loader(
            name=fullname,
            loader=SourceFileLoader(fullname, str(download_file)),
            origin=origin,
            is_package=is_package,
        )

        if is_package:
            # Becomes __path__ in the imported module, and then the `path` argument to find_spec
            # for subpackage searches
            # Meant to be a hint to future searches of where to look?
            spec.submodule_search_locations = []

        return spec

    @cache
    def _file_url(self, repo_path: PurePath) -> str:
        return f"https://raw.githubusercontent.com/{self.repo}/main/{repo_path}"
