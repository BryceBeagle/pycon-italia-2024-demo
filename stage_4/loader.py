from dataclasses import dataclass
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from pathlib import Path, PurePath
from types import ModuleType
from zipfile import ZipFile


@dataclass
class GitHubLoaderState:
    download_file: Path


class GitHubLoader(Loader):
    def create_module(self, spec: ModuleSpec) -> ModuleType | None:
        return None

    def exec_module(self, module: ModuleType) -> None:
        loader_state = module.__spec__.loader_state
        assert isinstance(loader_state, GitHubLoaderState)

        origin = module.__spec__.origin

        file_content = loader_state.download_file.read_text()

        code = compile(file_content, origin, mode="exec")

        module.__dict__["__file__"] = origin
        exec(code, module.__dict__)
