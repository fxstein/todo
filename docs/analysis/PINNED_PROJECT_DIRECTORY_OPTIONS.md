Pinned Project Directory Options
================================

Goal
----
Prevent accidental initialization in unintended directories by pinning
todo.ai to a specific project root, regardless of where the command is run.

Options
-------
Option A: Git Root Anchor (Repo-Scoped, No Search)
1) If inside a git repo, resolve the repo root with
   `git rev-parse --show-toplevel`.
2) If inside a submodule, prefer the superproject root via
   `git rev-parse --show-superproject-working-tree` (if set).
3) Use that repo root as the authoritative base directory.
4) Derive `TODO_FILE`, `LOG_FILE`, `SERIAL_FILE`, `CONFIG_FILE` from the
   resolved root before any init or migrations.
5) Provide CLI commands:
   - `pin` writes `project.root` into `${REPO_ROOT}/.todo.ai/config.yaml`
   - `unpin` clears `project.root`
   - `show-pin` displays the resolved root and config value

Pros:
- Deterministic: relies on git metadata, no directory traversal
- Repo-scoped (not global), works from any subdirectory
- Explicit and durable configuration in repo

Cons:
- Requires git (or a fallback for non-git folders)
- Submodule handling needs explicit policy

Option B: Repo-Scoped Config with Explicit Root
1) Require `--root /path/to/repo` to bootstrap when not in a git repo.
2) Use that root to read/write `${ROOT}/.todo.ai/config.yaml`.
3) Subsequent runs can use the configured root when invoked from within
   that repo, or require `--root` again when outside.

Pros:
- Deterministic and explicit
- Works for non-git directories

Cons:
- Requires explicit root for initial setup or non-git usage

Option C: Environment Variable Override
1) Support `TODO_AI_ROOT=/path/to/root` for CI or scripted usage.
2) Use this value as root if set; otherwise rely on Option A.

Pros:
- Deterministic override without changing repo config
- Useful for automation

Cons:
- Not discoverable for most users

Option D: Hybrid Repo Config + Env Var
1) Use `TODO_AI_ROOT` if set (highest priority).
2) Otherwise use git root (Option A) and repo config.
3) Otherwise require `--root` (Option B) or fallback to cwd.

Pros:
- Deterministic with explicit override
- Flexible for CI and ad-hoc usage

Cons:
- Adds precedence complexity

Recommendation
--------------
Prefer Option D (Hybrid Repo Config + Env Var). It stays deterministic and
repo-scoped via git root/config, while allowing explicit override for CI or
special cases via `TODO_AI_ROOT` and `--root` when needed.
