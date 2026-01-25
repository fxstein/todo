# Cursor Rules MCP Migration Analysis

## Overview
This document analyzes the current state of Cursor rules and outlines the changes required to support the three-version hierarchy of todo.ai, prioritizing the MCP server for AI agents.

## Version Hierarchy & Preference Order
1. **MCP Server (`todo-ai-mcp`)**: v3.0+
   - Preferred interface for AI agents
   - Zero-latency, structured data exchange
   - Running as background process in Cursor

2. **Python CLI (`todo-ai`)**: v3.0+
   - Modern CLI interface
   - Fallback if MCP server is unavailable
   - Recommended for manual user interaction in v3.0+

3. **Shell Script (`./todo.ai`)**: v2.x+ (including v3.0)
   - Legacy/Universal interface
   - Fallback for users without Python/pipx/uv
   - Maintained for backward compatibility

## Current State Analysis
A grep search of `.cursor/rules/*.mdc` revealed widespread hardcoded references to the shell script version (`./todo.ai`).

### Files Requiring Updates

| File | Current Usage | Required Change |
|------|---------------|-----------------|
| `todo.ai-task-management.mdc` | Generic "use todo.ai" | Explicitly prefer MCP tools (`add_task`, `list_tasks`, etc.) |
| `bug-review-workflow.mdc` | `./todo.ai add`, `./todo.ai add-subtask` | Use MCP tools `add_task`, `add_subtask` |
| `todo.ai-task-notes.mdc` | `./todo.ai note` | Use MCP tool `add_note` (or equivalent) |
| `todo.ai-bug-reporting.mdc` | `./todo.ai report-bug` | Use MCP tool `report_bug` |
| `todo.ai-uninstall.mdc` | `./todo.ai uninstall` | Use MCP tool `uninstall_tool` |
| `.cursorrules` (root) | `./todo.ai` references | Update to mention MCP preference |

### Files to Preserve (No Changes or Minor Updates)
- `todo.ai-installation.mdc`: Installation instructions likely still need `curl` or `uv` commands, but should mention `uv tool install ai-todo` for v3.0+.
- `repository-context.mdc`: Correctly identifies the repo context.
- `commit-prefixes.mdc`: Rules about commit messages apply regardless of the tool used.

## Migration Strategy

### 1. Detection Logic
Rules should instruct the agent to check for available tools in this order:
1. Is the MCP server active? (Try using it)
2. Is `todo-ai` in the PATH?
3. Is `./todo.ai` in the root?

### 2. Rule Updates
Each rule file will be updated to:
- List the MCP tool name as the primary method.
- List `todo-ai` CLI as the secondary method.
- List `./todo.ai` as the legacy fallback.

### 3. Example Format
**Before:**
```markdown
Command: `./todo.ai note <task-id> "Your note here"`
```

**After:**
```markdown
**Preferred:** Use MCP tool `add_note` with arguments `task_id` and `note`.
**Fallback:** `todo-ai note <task-id> "note"` (CLI) or `./todo.ai note ...` (Shell)
```

## Next Steps
1. Update `todo.ai-task-management.mdc` (Task #187.2)
2. Update `bug-review-workflow.mdc` (Task #187.3)
3. Update `todo.ai-task-notes.mdc` (Task #187.4)
4. Update `.cursorrules` (Task #187.5)
5. Add detection logic guidance (Task #187.6)
