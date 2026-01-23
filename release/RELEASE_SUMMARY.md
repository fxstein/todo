This beta fixes repository root resolution when running inside submodules, so
`show-root` now reliably points to the superproject instead of the nested
submodule directory. The shell and Python CLIs both detect submodule gitdir
paths and resolve back to the correct top-level repo for consistent behavior.

The update tightens submodule path detection to avoid false matches, making the
root logic more robust across complex workspaces. This ensures Cursor rules and
todo.ai data stay scoped to the intended repository even when working deep in
submodule trees.
