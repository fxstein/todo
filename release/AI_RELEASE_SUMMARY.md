# Release Summary: v4.0.0

## Breaking Changes

This release includes **API terminology standardization** (task#253) that aligns ai-todo with industry conventions. The MCP tools and CLI commands have been updated:

- `add_task(description)` → `add_task(title, description?, tags?)`
- `add_subtask(parent_id, description)` → `add_subtask(parent_id, title, description?, tags?)`
- `modify_task(task_id, description)` → `modify_task(task_id, title, description?, tags?)`
- `add_note`, `update_note`, `delete_note` → `set_description(task_id, description)`
- New: `set_tags(task_id, tags)` for dedicated tag management

Legacy shell scripts have been frozen with a FROZEN header for backward compatibility but are no longer actively maintained.

## New Features

**MCP Resources** (task#262, GitHub Issue #48): AI agents can now access task data via MCP resources - `tasks://open` for pending tasks, `tasks://active` for in-progress work, `tasks://{id}` for individual task details, and `config://settings` for configuration. This enables IDE integrations to display real-time task status without explicit tool calls.

**Task Metadata Persistence** (task#263): Task timestamps (`created_at`, `updated_at`) are now persisted across sessions via hidden HTML comments in TODO.md. Timestamps are lazily backfilled when tasks are modified, ensuring accurate tracking without migration scripts. Completion dates continue to appear inline for human readability.

**Batch Operations** (task#261, GitHub Issue #31): The `complete`, `delete`, `archive`, and `restore` commands now accept multiple task IDs in a single call, reducing round-trips when managing multiple tasks. Both MCP tools and CLI support this batch interface.

## Security & Reliability

**.cursorignore Protection** (task#260, GitHub Issue #29): Added `.cursorignore` patterns to prevent AI agents from directly accessing tamper detection state files. Security best practices documentation added at `docs/guides/SECURITY_BEST_PRACTICES.md`.

**Bug Fixes**: Fixed TASK_METADATA being incorrectly captured as interleaved content, causing subtask display issues. Resolved archive/delete task ordering bug where parent tasks were processed before subtasks (task#242). Restored GitHub task number coordination posting (task#247).
