This beta hardens repo-scoped usage by pinning todo.ai to the repository (or
super-repo) root by default, preventing accidental initialization in the wrong
directory. It also adds a `show-root` command with `--root` and `TODO_AI_ROOT`
overrides, plus parity tests to verify the behavior across the shell and Python
interfaces.

Release tooling is more reliable with a clarified AI summary pipeline, a
finalized `--set-version` workflow, and CI gating that focuses on the latest
commit to avoid false failures. Documentation updates cover the pinned-root
feature, usage patterns, and the overall design so users and contributors have
clear guidance.
