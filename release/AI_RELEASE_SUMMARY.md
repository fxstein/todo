This beta hardens repo-scoped usage by pinning todo.ai to the repository (or
super-repo) root by default, preventing accidental initialization in the wrong
directory. It also adds a `show-root` command with `--root` and `TODO_AI_ROOT`
overrides so users can verify and control the resolved root explicitly.

The release brings parity updates in the Python CLI alongside new validation
tests, plus clearer guidance in the Getting Started and Usage Patterns docs.
CI gating is now scoped to the latest commit for release preparation, reducing
false stops from older failed runs.
