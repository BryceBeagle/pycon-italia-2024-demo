import importlib.util
import shutil
import urllib.request
from functools import cache
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import PurePath, Path
from tempfile import NamedTemporaryFile
from types import ModuleType
from urllib.error import HTTPError

from stage_4.loader import GitLoader, GitLoaderState


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
        if (download_file := self._download_file(package)) is not None:
            return self._new_spec(fullname, package, download_file, is_package=True)
        if (download_file := self._download_file()) is not None:
            return self._new_spec(fullname, module, download_file, is_package=False)

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
            loader=GitLoader(),
            origin=origin,
            is_package=is_package,
        )
        spec.loader_state = GitLoaderState(download_file=download_file)

        if is_package:
            spec.submodule_search_locations = []

        return spec

    @cache
    def _file_url(self, repo_path: PurePath) -> str:
        return f"https://raw.githubusercontent.com/{self.repo}/main/{repo_path}"
