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
   * **Strategy 1: MCP Prompt (Recommended):**
     * Implement an MCP Prompt named `active_context` (or `current_status`).
     * When invoked, this prompt returns a formatted list of all tasks marked `#inprogress`.
     * This allows the user/agent to explicitly "load" the active context at the start of a session.
   * **Strategy 2: Tool Description Engineering:**
     * Update the `list_tasks` tool description.
     * Add explicit instruction: "Use this tool at the start of a conversation to check for #inprogress tasks."
   * **Strategy 3: List Filtering:**
     * Ensure `list_tasks` supports filtering by tag (already exists, but verify `#inprogress` works seamlessly).

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

* **Tools:**
  * Add `start_task` tool.
  * Update `list_tasks` tool description to encourage checking `#inprogress`.
* **Prompts:**
  * Add `active_context` prompt that returns currently in-progress tasks.

### 4. Tests

* Unit tests for `start_task` logic.
* Integration tests for lifecycle (start -> complete -> verify tag removed).
* Verify MCP Prompt returns correct tasks.
