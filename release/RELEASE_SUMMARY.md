# todo.ai v2.7.3 - Delete Command Format Fix

This patch release completes the task ID format handling improvements by updating the `delete` command to support both bold and non-bold task ID formats. This ensures consistency across all task management commands (add, modify, note, complete, archive, delete, show) - they all now handle tasks regardless of whether they're formatted with bold markers (`**#task_id**`) or plain format (`#task_id`).

The fix updates the `delete_task()` function to use extended regex patterns that match both formats, similar to the fixes applied to other commands in v2.7.2. This prevents the "Task not found" error when attempting to delete tasks that exist in non-bold format, ensuring reliable task deletion regardless of formatting.
