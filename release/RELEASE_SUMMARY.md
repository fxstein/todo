This release fixes a critical bug in the bug reporting feature where log collection was retrieving the oldest entries instead of the newest ones.

**Key Fixes:**
- Fixed log collection order: Changed from `tail -n 50` to `head -n 50` since the log file is sorted in descending order (newest entries at the top)
- Added header line filtering: Skip comment lines (starting with `#`) when collecting logs
- Updated documentation: Added comments explaining the log file format (descending order, newest first)

**Impact:**
- Bug reports now correctly include the 50 most recent log entries instead of the 50 oldest entries
- This ensures developers receive relevant, recent context when debugging issues
- The fix improves the quality and usefulness of automated bug reports
