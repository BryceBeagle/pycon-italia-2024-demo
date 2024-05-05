import importlib.util
from functools import cached_property
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from pathlib import Path, PurePath
from types import ModuleType
from zipfile import ZipFile

from stage_3.loader import ZipLoader, ZipLoaderState


class ZipFinder(MetaPathFinder):
    def __init__(self, path: Path):
        self.path = path

    def find_spec(
            self,
            fullname: str,
            path: str | None,
            target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        # If both foo/ and foo.py exist, foo/ takes priority
        if (file := (PurePath(fullname) / "__init__.py")) in self._files:
            return self._new_spec(fullname, file, is_package=True)
        if (file := PurePath(fullname).with_suffix(".py")) in self._files:
            return self._new_spec(fullname, file, is_package=False)

        return None

    @cached_property
    def _files(self) -> set[PurePath]:
        files = set()
        with ZipFile(self.path) as zip_file:
            for info in zip_file.infolist():
                file_path = PurePath(info.filename)
                files.add(file_path)

        return files

    def _new_spec(
            self, fullname: str, file: PurePath, *, is_package: bool
    ) -> ModuleSpec:
        origin = str(self.path / file)
        spec = importlib.util.spec_from_loader(
            name=fullname,
            loader=ZipLoader(),
            origin=origin,
            is_package=is_package,
        )
        spec.submodule_search_locations = [self.path / fullname]
        spec.loader_state = ZipLoaderState(zip_file=self.path)

        return spec
