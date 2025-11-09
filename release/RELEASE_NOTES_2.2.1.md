# Release Summary

This patch release fixes a bug discovered shortly after v2.2.0 where adding subtasks to tasks with notes would incorrectly split the notes from their parent tasks.

## Bug Fix

**Add_subtask No Longer Splits Task Notes**

Fixed a bug where adding a subtask to a task that has notes (blockquotes) would insert the subtask between the task line and its notes, separating them. The `add_subtask()` function now correctly skips over all blockquote notes following the parent task before inserting the new subtask. This ensures notes remain directly attached to their parent tasks where they belong ([a81da43](https://github.com/fxstein/todo.ai/commit/a81da43)).

**Testing:** Verified with single notes, multiple notes, and nested subtasks at various levels. All note positioning scenarios now work correctly.

## Additional Changes

- Added exploratory subtask to investigate bash version for improved portability and potential size reduction
- Note positioning automatically corrected for existing tasks affected by the bug

---

### Fixed
- fix: Add_subtask now inserts after parent task notes instead of splitting them (task#136) ([a81da43](https://github.com/fxstein/todo.ai/commit/a81da436fb2d301900c2aad248a063c02b4c3f13))
- Fix task#132 note positioning after subtask insertion fix ([5849ccb](https://github.com/fxstein/todo.ai/commit/5849ccb35732801dc2acf0b47aba9c32aeea846a))
- Archive completed task#136: Fix subtask insertion splitting notes ([c6cb431](https://github.com/fxstein/todo.ai/commit/c6cb431d402b829f7e3573046049015f5ee1a492))

### Other
- Add implementation note to task#136 ([cc0cb1c](https://github.com/fxstein/todo.ai/commit/cc0cb1ca6afb49cb4989d6b254ead57ff86d74d9))
- Add task#136: Fix bug where adding subtasks splits task notes ([d5726eb](https://github.com/fxstein/todo.ai/commit/d5726eb817f073f8c708e6780e2b48198a9e645f))
- Add subtask to explore bash version for size/portability (task#132.3) ([0a70669](https://github.com/fxstein/todo.ai/commit/0a70669ce8f89e0b9b23f39b3767a6bf5d91b925))

*Total commits: 6*

