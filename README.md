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
