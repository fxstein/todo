This release fixes a critical bug in the release log prepend logic that was causing incorrect header detection.

The bug fix ([2b7558a](https://github.com/fxstein/todo.ai/commit/2b7558a...)) resolves an issue where the header detection logic was matching the empty line separator instead of the first actual log entry. The header detection now correctly identifies the first line starting with a timestamp (digit), ensuring that new log entries are always prepended correctly after the header and empty line separator, maintaining the newest-first chronological order.

The log has also been cleaned up to remove duplicates and ensure proper ordering with newest entries at the top, matching the todo.ai log file architecture.
