from dataclasses import dataclass
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from pathlib import Path, PurePath
from types import ModuleType
from zipfile import ZipFile


@dataclass
class ZipLoaderState:
    zip_file: Path


class ZipLoader(Loader):
    def create_module(self, spec: ModuleSpec) -> ModuleType | None:
        return None

    def exec_module(self, module: ModuleType) -> None:
        loader_state = module.__spec__.loader_state
        assert isinstance(loader_state, ZipLoaderState)

        origin = module.__spec__.origin
        path_in_zip = PurePath(origin).relative_to(loader_state.zip_file)

        with ZipFile(loader_state.zip_file) as zf:
            file_content = zf.read(str(path_in_zip)).decode()

        code = compile(file_content, origin, mode="exec")

        exec(code, module.__dict__)
