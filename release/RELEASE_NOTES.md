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
