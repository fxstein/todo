Pinned Project Directory Design
===============================

Goal
----
Ensure todo.ai always operates against the correct repository root, even when
invoked from subdirectories or submodules. The design must be deterministic
and avoid directory traversal heuristics.

Scope
-----
This design applies to the todo.ai CLI (shell script), not the Python MCP
server. The feature is repo-scoped, not global.

Core Principle
--------------
The root is pinned to the repo or super-repo root by default (a fixed choice),
with deterministic overrides. There is no config setting for this pin.

Root Resolution Order
---------------------
1) Git root anchor (default pin)
   - If inside a git repo, use `git rev-parse --show-toplevel`.
   - If inside a submodule, prefer the superproject root via
     `git rev-parse --show-superproject-working-tree` when available.
2) `--root /path` override
   - If provided, use it as the root (absolute or relative path resolved to
     an absolute path).
3) `TODO_AI_ROOT` environment variable override
   - If set, use it as the root (absolute or relative path resolved to
     an absolute path).
4) Fallback
   - If none of the above are available, use `ORIGINAL_WORKING_DIR`.

User-Facing Commands
--------------------
New or updated commands:
1) `show-root`
   - Displays the resolved root and the source (git, override, env, fallback).
2) `--root /path`
   - One-time override.

Behavior Details
----------------
- Determinism: No directory traversal, no marker file lookup.
- Submodules: Default to superproject root when available; provide
  `--root` to override if the submodule should be treated as the root.
- Non-git directories: Use overrides when needed; otherwise fallback to
  `ORIGINAL_WORKING_DIR`.
- Safety: If an override points to a missing path, warn and fall back to
  `ORIGINAL_WORKING_DIR`.

User Messaging
--------------
Examples:
- `show-root`:
  - "Resolved root: /path (source: git)"
  - "Override: TODO_AI_ROOT=/path"

Open Questions
--------------
1) Should submodule default be superproject or require explicit override?
2) Should overrides warn when they replace a resolved git root?
