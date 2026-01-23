This beta improves repository root detection for submodule layouts by correctly
handling gitdir pointer files. Running `show-root` from inside a submodule now
resolves to the superproject root instead of the nested module directory.

The update ensures consistent scoping for Cursor rules and todo.ai data when
working in projects that use submodules, reducing accidental initialization in
the wrong directory.
