# Description

This repository corresponds to a presentation given at [Pycon Italia 2024][pycon-it].
It contains some long-form implementations of the truncated examples given at the 
end of the presentation. 

- `stage_0`: Importing a normal package by adding it to `sys.path`
- `stage_1`: Importing from `.zip` files using the built-in `zipimport` importer
- `stage_2`: Importing from `.zip` files using custom `PathEntryFinder` and `Loader`
- `stage_3`: Importing from `.zip` files using custom `MetaPathFinder`s and `Loader`
- `stage_4`: Importing from GitHub repositories using custom `MetaPathFinder` and
  built-in `SourceFileLoader`
- `stage_5`: Importing from Rust bindings on GitHub using custom `MetaPathFinder` and
  built-in `ExtensionFileLoader`

[pycon-it]: https://2024.pycon.it

# Initial Setup

Install project with Poetry

```shell
poetry install
```

Clone helper repo (used for `stage_0` -> `stage_3`) and create `.zip` archive (used for
`stage_1` -> `stage_3`)

```shell
python scripts/_clone_repo.py
python scripts/_create_zip.py
```

# Running Examples

> `Note: ` These examples only work on Linux/MacOS. Windows users are on their own.

Run examples

```shell
python scripts/stage_0.py
python scripts/stage_1.py
python scripts/stage_2.py
python scripts/stage_3.py
python scripts/stage_4.py
python scripts/stage_5.py
```