This beta focuses on reliability for hierarchical task management in the new
Python-based todo.ai. Subtasks now insert directly under their intended parent
task (or the parent’s last subtask), preventing the mis-grouping that previously
collapsed all subtasks under a single task.

Alongside the fix, the release includes routine maintenance and task cleanup to
keep the repository and workflows tidy. The core user-facing change is the
correct subtask placement behavior, which restores confidence in multi-parent
task trees.
