# API Terminology Standardization

**Task:** #253
**Date:** 2026-01-27
**Status:** Design approved

## Summary

Rename parameters to follow industry conventions (GitHub, Linear, Jira) and simplify the API.

## Before → After

### MCP Tools

| Before | After |
|--------|-------|
| `add_task(description, tags?)` | `add_task(title, description?, tags?)` |
| `add_subtask(parent_id, description, tags?)` | `add_subtask(parent_id, title, description?, tags?)` |
| `modify_task(task_id, description, tags?)` | `modify_task(task_id, title, description?, tags?)` |
| `add_note(task_id, note_text)` | `set_description(task_id, description)` |
| `update_note(task_id, new_note_text)` | *removed* |
| `delete_note(task_id)` | *removed* - use `set_description(task_id, "")` |
| - | `set_tags(task_id, tags)` *new* |

### CLI Commands

| Before | After |
|--------|-------|
| `add DESCRIPTION [TAGS...]` | `add-task TITLE [--description TEXT] [TAGS...]` |
| `add-subtask PARENT_ID DESCRIPTION [TAGS...]` | `add-subtask PARENT_ID TITLE [--description TEXT] [TAGS...]` |
| `modify TASK_ID DESCRIPTION [TAGS...]` | `modify-task TASK_ID TITLE [--description TEXT] [TAGS...]` |
| `note TASK_ID NOTE_TEXT` | `set-description TASK_ID DESCRIPTION` |
| `update-note TASK_ID NEW_NOTE_TEXT` | *removed* |
| `delete-note TASK_ID` | *removed* - use `set-description TASK_ID ""` |
| - | `set-tags TASK_ID [TAGS...]` *new* |

## Key Changes

1. **`description` → `title`** for task headlines (matches GitHub/Linear)
2. **`note_text` → `description`** for detailed notes (matches industry standard)
3. **Merged note tools** into single idempotent `set_description`
4. **Added `set_tags`** for idempotent tag management
5. **Optional description** - `add_task`, `add_subtask`, `modify_task` accept optional `description`
6. **CLI command renames** - `add` → `add-task`, `modify` → `modify-task`

## Breaking Changes

- All parameter names change
- `add_note`, `update_note`, `delete_note` removed
- CLI command names change (`add` → `add-task`, `modify` → `modify-task`)
- CLI argument names change

No backward compatibility - clean break.
