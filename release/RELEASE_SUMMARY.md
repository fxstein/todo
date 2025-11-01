This release fixes the release log prepend bug that was causing older entries to remain at the top of the log file.

The bug fix resolves an issue where the header detection logic was incorrectly including the first log entry in the header section. The fix ensures that new log entries are correctly prepended at the top of the log file, maintaining proper newest-first chronological order.

The release log has also been cleaned up to remove duplicates and ensure proper ordering with newest entries at the top, matching the todo.ai log file architecture.
