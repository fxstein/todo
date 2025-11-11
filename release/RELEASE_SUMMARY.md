# Release Summary

This release brings significant improvements to the release workflow and task management features, making todo.ai more robust and AI-agent friendly.

## Major Features

**Redesigned Release Workflow**

The release process has been completely redesigned with a two-step prepare/execute workflow that eliminates all interactive prompts ([a5315cf](https://github.com/fxstein/todo.ai/commit/a5315cf)). The new workflow is fully automated and suitable for AI agents:
- **Prepare step** (default): Analyzes commits, determines version bump type, generates release notes, and saves state
- **Execute step**: Updates version, commits, tags, pushes to GitHub, and creates the release without any prompts
- No more manual confirmations or input required during release execution

**Enhanced Show Command**

The `show` command now provides complete context by displaying notes for parent tasks, all subtasks, and all sub-subtasks ([6024770](https://github.com/fxstein/todo.ai/commit/6024770)). This makes it much easier to understand task implementation details at a glance.

**Improved Note Command**

Fixed the `note` command to work correctly with nested sub-subtasks ([28a7fad](https://github.com/fxstein/todo.ai/commit/28a7fad)), ensuring notes can be added at any nesting level.

## Bug Fixes

**Release Script Robustness**

Multiple fixes to the release execution process ensure reliable automated releases:
- Fixed version verification when version already updated from failed attempts
- Added proper error handling for commit status detection
- Added GitHub issue references to version bump commits to pass pre-commit validation
- Improved state management between prepare and execute steps

## Additional Improvements

- Added `.prepare_state` to gitignore for cleaner git status
- Documented new release workflow in Cursor rules
- Enhanced release logging and error messages
