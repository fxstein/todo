Pinned Project Directory Options
================================

Goal
----
Prevent accidental initialization in unintended directories by pinning
todo.ai to a specific project root, regardless of where the command is run.

Options
-------
Option A: Git Root Pin (Repo-Scoped, No Search)
1) If inside a git repo, resolve the repo root with
   `git rev-parse --show-toplevel`.
2) If inside a submodule, prefer the superproject root via
   `git rev-parse --show-superproject-working-tree` (if set).
3) Use that repo root as the pinned base directory.
4) Derive `TODO_FILE`, `LOG_FILE`, `SERIAL_FILE`, `CONFIG_FILE` from the
   resolved root before any init or migrations.

Pros:
- Deterministic: relies on git metadata, no directory traversal
- Repo-scoped (not global), works from any subdirectory
- No extra config or markers required

Cons:
- Requires git (or a fallback for non-git folders)
- Submodule handling needs explicit policy

Option B: CLI Override
1) Use `--root /path/to/repo` to override the pinned git root.
2) When provided, it becomes the root for that invocation only.

Pros:
- Deterministic and explicit
- Works for non-git directories

Cons:
- Requires explicit root for non-git usage

Option C: Environment Variable Override
1) Support `TODO_AI_ROOT=/path/to/root` for CI or scripted usage.
2) Use this value as root if set; otherwise rely on Option A.

Pros:
- Deterministic override without changing repo config
- Useful for automation

Cons:
- Not discoverable for most users

Option D: Hybrid Pin + Overrides (Chosen)
1) Pin to git root (Option A) by default.
2) Allow `--root` (Option B) or `TODO_AI_ROOT` (Option C) to override.
3) If git is unavailable and no override is set, fall back to cwd.

Pros:
- Deterministic with explicit override
- Flexible for CI and ad-hoc usage

Cons:
- Adds precedence complexity

Recommendation
--------------
Prefer Option D (Hybrid Pin + Overrides). It pins to repo/super-repo root
by default, with explicit overrides via `--root` or `TODO_AI_ROOT`, and
uses cwd only as a last resort.
