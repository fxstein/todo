# Release Summary

This patch release fixes a bug discovered shortly after v2.2.0 where adding subtasks to tasks with notes would incorrectly split the notes from their parent tasks.

## Bug Fix

**Add_subtask No Longer Splits Task Notes**

Fixed a bug where adding a subtask to a task that has notes (blockquotes) would insert the subtask between the task line and its notes, separating them. The `add_subtask()` function now correctly skips over all blockquote notes following the parent task before inserting the new subtask. This ensures notes remain directly attached to their parent tasks where they belong ([a81da43](https://github.com/fxstein/todo.ai/commit/a81da43)).

**Testing:** Verified with single notes, multiple notes, and nested subtasks at various levels. All note positioning scenarios now work correctly.

## Additional Changes

- Added exploratory subtask to investigate bash version for improved portability and potential size reduction
- Note positioning automatically corrected for existing tasks affected by the bug
