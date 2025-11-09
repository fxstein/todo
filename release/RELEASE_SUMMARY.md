# Release Summary

This release focuses on improving code quality, fixing a critical bug, and enhancing developer experience with better task documentation practices.

## Key Improvements

**Bug Fix - Task Notes Now Move with Archived Tasks**

Fixed a significant bug ([#32](https://github.com/fxstein/todo.ai/issues/32)) where task notes (blockquotes) were not moved when archiving tasks. Notes would remain in the active section and become orphaned, attaching to unrelated tasks. The archive function now properly collects and moves all notes with their parent tasks and subtasks, ensuring data integrity and preventing confusion. This fix includes comprehensive test coverage for single tasks, tasks with subtasks, and nested subtasks with notes at multiple levels ([70c9123](https://github.com/fxstein/todo.ai/commit/70c9123)).

**New Feature - Task Notes Cursor Rule**

Added a new Cursor rule (`todo.ai-task-notes.mdc`) that encourages AI agents to add implementation notes to tasks. The rule provides clear examples of good notes (specific file locations, dependencies, technical context) versus vague notes, promoting better task documentation and making it easier for developers to understand implementation details. Notes should be used for actionable context, not status updates on parent tasks ([b195b08](https://github.com/fxstein/todo.ai/commit/b195b08)).

**Code Optimization - Migration Cleanup**

Removed 333 lines of obsolete migration code (v1.3.5 section order fix and v1.6.0 cursor rules migration) that are no longer needed for current installations. The migration framework infrastructure remains intact for future use. This cleanup reduces file size by 4.2% while maintaining full functionality. Legacy installations requiring old migrations can reference git history at commit bd028a2 and earlier ([0200788](https://github.com/fxstein/todo.ai/commit/0200788)).

## Additional Changes

- Added comprehensive code size analysis documentation analyzing the 6,741-line codebase and identifying optimization opportunities
- Updated README to remove outdated single-user mode limitations
- Improved task management practices by discouraging redundant status notes on parent tasks
