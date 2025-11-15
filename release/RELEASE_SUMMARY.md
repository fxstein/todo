# todo.ai v2.5.1 Hotfix Release

## Critical Bug Fix

This hotfix addresses a critical data integrity bug discovered in v2.4.0 and v2.5.0 where duplicate task IDs could be assigned in single-user mode.

**Issue Fixed:** get_highest_task_number() was incorrectly scanning ALL lines in TODO.md, including documentation examples in blockquote notes. This caused the function to find task IDs that weren't real tasks, leading to potential duplicate ID assignments.

**Example:** A documentation note containing `> **#42.1** Example task` would be counted as a real task, interfering with ID assignment logic.

**Solution:** Updated get_highest_task_number() to skip blockquote lines (starting with `>`), ensuring only actual task lines are scanned for ID extraction.

## Additional Improvements

**Universal Zsh-to-Bash Converter:** Created a dedicated conversion script (`release/convert_zsh_to_bash.sh`) that handles all bash compatibility transformations systematically. This improves reliability and makes the conversion process reusable for development and testing.

**Impact:** Users who experienced duplicate task ID assignments should see this issue completely resolved. The fix has been tested in both zsh and bash versions.
