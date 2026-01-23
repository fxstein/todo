## Release 3.0.0b4

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

---

### ✨ Features

- add show-root parity tests (task#182.5, task#182.6) ([429af92](https://github.com/fxstein/todo.ai/commit/429af92c94203bf036799bf655ca1379e6ec416a))
- add pinned root resolution (task#182.4) ([42733df](https://github.com/fxstein/todo.ai/commit/42733df68c7ad6c48e7a115b79273f775ceeeef5))
- add task#182 for pinned directory design ([c845a42](https://github.com/fxstein/todo.ai/commit/c845a42a2a348eb17aa71970ae0a51d70946aba9))

### 🐛 Bug Fixes

- skip show-root shell test on Windows ([2cbcc0e](https://github.com/fxstein/todo.ai/commit/2cbcc0e765b641651d74d7fb2682e0276325c97a))

### 🔧 Other Changes

- docs: add AI release summary ([8d9e63f](https://github.com/fxstein/todo.ai/commit/8d9e63f7879cd1d101d232c570e08b2b6f60d08a))
- docs: shorten release agent rules ([2656ba6](https://github.com/fxstein/todo.ai/commit/2656ba650e9a7c0ae594e23f76f987bde6b8047c))
- chore: add AI release summary ([d78b30e](https://github.com/fxstein/todo.ai/commit/d78b30e7a57ef0091710028e02380fa39ee7fc6e))
- infra: scope CI gate to HEAD commit ([89c6ec4](https://github.com/fxstein/todo.ai/commit/89c6ec413176352af519e44b67a1073f11841ef1))
- infra: check latest CI run only ([1924a58](https://github.com/fxstein/todo.ai/commit/1924a58691bf5951ead2f7bc81731310a0aa9b07))
- docs: document pinned root usage (task#182.7) ([59b67ab](https://github.com/fxstein/todo.ai/commit/59b67ab29e569aa0dde4c72ec6eced24308dfa8f))
- docs: update pinned root task tracking (task#182) ([c292b40](https://github.com/fxstein/todo.ai/commit/c292b4017677fe8425f45ea6e635fedf5e3f4e3c))
- docs: finalize pinned root design (task#182.3) ([6aacf1e](https://github.com/fxstein/todo.ai/commit/6aacf1e9126f3c8d846891802f5e5df161d9f151))
- docs: analyze pinned directory options (task#182) ([40d1eaf](https://github.com/fxstein/todo.ai/commit/40d1eaf40959b26d05613bea15ff27dff13c81e0))

## Previous Beta Release Notes

## Release 3.0.0b3

This beta focuses on reliability for hierarchical task management in the new
Python-based todo.ai. Subtasks now insert directly under their intended parent
task (or the parent’s last subtask), preventing the mis-grouping that previously
collapsed all subtasks under a single task.

Alongside the fix, the release includes routine maintenance and task cleanup to
keep the repository and workflows tidy. The core user-facing change is the
correct subtask placement behavior, which restores confidence in multi-parent
task trees.

---

### 🐛 Bug Fixes

- Place subtasks under correct parent (task#178, #40) ([9e1d668](https://github.com/fxstein/todo.ai/commit/9e1d668edc958818951bde86011e9f2469109efd))

### 🔧 Other Changes

- docs: refresh release summary (task#179) ([7eece50](https://github.com/fxstein/todo.ai/commit/7eece500ddc61fbdedca8c63df6ab7b8874353b5))
- chore: add AI release summary ([d5208d4](https://github.com/fxstein/todo.ai/commit/d5208d420489125a686a17f1e963c8bec5b54dce))
- chore: Archive completed tasks 173-178 (task#178) ([f68320c](https://github.com/fxstein/todo.ai/commit/f68320c606dad5391510440a0b60857df92799f1))
