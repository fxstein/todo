This release addresses a critical bug (GitHub Issue #49) where archived tasks with incomplete subtasks would incorrectly reappear in the Tasks section when adding new tasks. The fix changes how task status is determined during parsing: section membership now takes precedence over checkbox state, ensuring that all tasks in "Recently Completed" or "Archived Tasks" sections are properly treated as archived regardless of their checkbox character.

Additionally, this release fixes the `config://settings` MCP resource to correctly report `coordination.enabled` status. Previously it was checking for a non-existent configuration key, causing it to always return `false`. The resource now properly derives the enabled state from the configured coordination type.

Both fixes include regression tests to prevent these issues from recurring. Users who experienced archived tasks unexpectedly appearing in their active task list should update to this version immediately.
