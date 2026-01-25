# Start Command Design

## Overview

The `start` command allows users (and agents) to explicitly mark a task as "in progress". This helps track active work and provides context to the AI agent about what the user is currently focused on.

## Requirements

1. **Start Command:**
   * **CLI:** `todo-ai start <task_id>`
   * **MCP:** `start_task(task_id)`
   * **Action:** Appends the `#inprogress` tag to the task description.
   * **Validation:**
     * Task must exist.
     * Task status must be `PENDING`. (Cannot start a completed or archived task without restoring it first).
     * If task already has `#inprogress` tag, operation is idempotent (success, no change).

2. **Stop Command (Optional/Future):**
   * **CLI:** `todo-ai stop <task_id>`
   * **MCP:** `stop_task(task_id)`
   * **Action:** Removes the `#inprogress` tag.

3. **Tag Lifecycle (Automatic Removal):**
   * The `#inprogress` tag represents *current* activity. It should be removed when the task transitions to a non-active state.
   * **Completion:** `complete_task` MUST remove `#inprogress`.
   * **Archiving:** `archive_task` MUST remove `#inprogress`.
   * **Deletion:** `delete_task` SHOULD remove `#inprogress` (clean up before moving to deleted state).

4. **MCP Context Surfacing:**
   * The MCP server needs to make in-progress tasks visible to the agent.
   * **Strategy:**
     * When `list_tasks` is called, tasks with `#inprogress` should be highlighted or filtered easily.
     * (Future) System prompt injection of active tasks? (Out of scope for this task, but `list_tasks` support is in scope).

## Implementation Plan

### 1. Core Logic (`todo_ai/core/task.py` / `todo_ai/core/file_ops.py`)

* **`start_task(task_id)` function:**
  * Load task.
  * Check status.
  * Add `#inprogress` tag if missing.
  * Save.

* **Lifecycle Hooks:**
  * Modify `complete_task`, `archive_task`, `delete_task` to strip `#inprogress` tag before state change.

### 2. CLI Implementation (`todo_ai/cli/commands/task.py`)

* Add `start_command` using `click`.
* Calls core `start_task` logic.

### 3. MCP Implementation (`todo_ai/mcp/server.py`)

* Add `start_task` tool.
* Expose via MCP protocol.

### 4. Tests

* Unit tests for `start_task` logic.
* Integration tests for lifecycle (start -> complete -> verify tag removed).
