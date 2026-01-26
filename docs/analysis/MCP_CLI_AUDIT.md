# MCP/CLI Tools Audit for ai-todo v3.0

**Date:** 2026-01-26
**Task:** #238.4 / #234
**Status:** PENDING REVIEW

---

## Executive Summary

Audit of all MCP tools and CLI commands to identify:
- Parity gaps between MCP and CLI
- Obsolete/deprecated tools
- Missing functionality
- Naming inconsistencies

**Current Counts:**
- MCP Tools: 32
- CLI Commands: 46
- Aliases: ~8 (CLI only, most being removed)

**Proposed Changes:**
- Remove 6 MCP tools (non-core functionality)
- Remove 12 CLI commands (non-core functionality)
- Rename 3 MCP tools for consistency
- Add 1 MCP tool (`version`)
- Keep focus on core task management

---

## MCP Tools Inventory (32 tools)

| Tool | Description | CLI Equivalent |
|------|-------------|----------------|
| `accept_tamper` | Accept external TODO.md changes | `tamper accept` |
| `add_note` | Add note to task | `note` |
| `add_subtask` | Add subtask to parent | `add-subtask` |
| `add_task` | Add new task | `add` |
| `archive_task` | Archive task(s) | `archive` |
| `complete_task` | Mark task complete | `complete` |
| `delete_note` | Delete notes from task | `delete-note` |
| `delete_task` | Delete task(s) | `delete` |
| `detect_coordination` | Detect coordination options | `detect-coordination` |
| `get_active_tasks` | Get in-progress tasks | ❌ No equivalent |
| `lint_todo` | Check for formatting issues | `lint` |
| `list_backups` | List backups | `backups` |
| `list_tasks` | List all tasks | `list` |
| `modify_task` | Modify task | `modify` |
| `reformat_todo` | Apply formatting fixes | `reformat` |
| `relate_task` | Add relationship | `relate` |
| `reorder_todo` | Reorder subtasks | `reorder` |
| `report_bug` | Report bug to GitHub | `report-bug` |
| `resolve_conflicts` | Fix duplicate IDs | `resolve-conflicts` |
| `restore_task` | Restore deleted/archived | `restore` |
| `rollback` | Rollback to backup | `rollback` |
| `setup_coordination` | Setup coordination | `setup-coordination` |
| `show_config` | Show configuration | `config` |
| `show_task` | Show task details | `show` |
| `start_task` | Mark as in-progress | `start` |
| `stop_task` | Stop progress | `stop` |
| `switch_mode` | Change numbering mode | `switch-mode` |
| `undo_task` | Reopen completed task | `undo` |
| `uninstall_tool` | Uninstall ai-todo | `uninstall` |
| `update_note` | Replace notes | `update-note` |
| `update_tool` | Update ai-todo | `update` |
| `view_log` | View operation log | `log` |

---

## CLI Commands Inventory (46 commands)

### Core Task Operations

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `add` | `add_task` | ✅ Parity |
| `add-subtask` | `add_subtask` | ✅ Parity |
| `complete` | `complete_task` | ✅ Parity |
| `delete` | `delete_task` | ✅ Parity |
| `modify` | `modify_task` | ✅ Parity |
| `archive` | `archive_task` | ✅ Parity |
| `restore` | `restore_task` | ✅ Parity |
| `undo` | `undo_task` | ✅ Parity |
| `start` | `start_task` | ✅ Parity |
| `stop` | `stop_task` | ✅ Parity |

### Task Display

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `list` | `list_tasks` | ✅ Parity |
| `show` | `show_task` | ✅ Parity |
| `get-active-tasks` | `get_active_tasks` | ⚠️ **ADD** - new command |

### Notes

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `note` | `add_note` | ✅ Parity |
| `delete-note` | `delete_note` | ✅ Parity |
| `update-note` | `update_note` | ✅ Parity |

### Relationships

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `relate` | `relate_task` | ✅ Parity |

### File Operations

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `lint` | `lint_todo` | ✅ Parity |
| `reformat` | `reformat_todo` | ✅ Parity |
| `reorder` | `reorder_todo` | ✅ Parity |
| `resolve-conflicts` | `resolve_conflicts` | ✅ Parity |
| `edit` | ❌ None | ⚠️ **REMOVE** - use `$EDITOR TODO.md` |

### Configuration & Setup

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `config` | `show_config` | ✅ Parity |
| `show-config` | `show_config` | Alias for config |
| `setup` | ❌ None | Interactive wizard - CLI only |
| `setup-wizard` | ❌ None | ⚠️ **REMOVE** - alias for setup |
| `setup-coordination` | `setup_coordination` | ✅ Parity |
| `detect-coordination` | `detect_coordination` | ✅ Parity |
| `detect-options` | `detect_coordination` | Alias |
| `switch-mode` | `switch_mode` | ✅ Parity |

### Backup & Recovery

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `backups` | `list_backups` | ✅ Parity |
| `list-backups` | `list_backups` | Alias |
| `rollback` | `rollback` | ✅ Parity |
| `list-mode-backups` | ❌ None | ⚠️ Missing in MCP |
| `rollback-mode` | ❌ None | ⚠️ Missing in MCP |

### Tamper Detection

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `tamper` | `accept_tamper` | Partial - CLI has subcommands |

### System Operations

| Command | MCP Equivalent | Notes |
|---------|----------------|-------|
| `log` | `view_log` | ✅ Parity |
| `update` | `update_tool` | ✅ Parity |
| `uninstall` | `uninstall_tool` | ✅ Parity |
| `report-bug` | `report_bug` | ✅ Parity |
| `version` | ❌ None | ⚠️ Missing in MCP |
| `show-root` | ❌ None | Debug only - CLI only |
| `serve` | N/A | Starts MCP server |

---

## Parity Analysis

### MCP Tools with No CLI Equivalent (0 after cleanup)

| MCP Tool | Purpose | Recommendation |
|----------|---------|----------------|
| `get_active_tasks` | Returns in-progress tasks | ✅ **Add CLI `get-active-tasks`** |

### CLI Commands with No MCP Equivalent (3 after cleanup)

| CLI Command | Purpose | Recommendation |
|-------------|---------|----------------|
| `setup` | Interactive wizard | ❌ CLI-only (interactive) |
| `show-root` | Debug: show root path | ❌ CLI-only (debug) |
| `serve` | Start MCP server | N/A (is the MCP server) |

### CLI Aliases (kept)

| Alias | Points To |
|-------|-----------|
| `show-config` | `config` |

**Aliases removed:** `list-backups`, `setup-wizard`, `detect-options`

---

## Naming Consistency Review

### Current Naming Patterns

**MCP Tools:** `snake_case` (e.g., `add_task`, `complete_task`)
**CLI Commands:** `kebab-case` (e.g., `add-subtask`, `delete-note`)

This is standard convention and should be kept.

### Inconsistencies Found

| Issue | Current | Recommended |
|-------|---------|-------------|
| MCP `uninstall_tool` | Includes `_tool` suffix | Consider `uninstall` |
| MCP `update_tool` | Includes `_tool` suffix | Consider `update` |
| MCP `view_log` | Different from CLI `log` | Consider `show_log` |
| MCP `lint_todo` | Includes `_todo` suffix | Consider `lint` |
| MCP `reformat_todo` | Includes `_todo` suffix | Consider `reformat` |
| MCP `reorder_todo` | Includes `_todo` suffix | Consider `reorder` |

**Note:** Renaming MCP tools is a **breaking change** for existing MCP configurations.

---

## Proposed Eliminations

### Philosophy

Focus ai-todo on **core task management** only. Remove system administration, backup/recovery, and debugging tools that:
- Are not needed for day-to-day task management
- Add complexity without clear value for AI agents
- Can be handled by standard system tools (pip, git, etc.)

### MCP Tools to Remove (6)

| Tool | Category | Reason |
|------|----------|--------|
| `update_tool` | System Admin | Use `pip install --upgrade ai-todo` instead |
| `uninstall_tool` | System Admin | Use `pip uninstall ai-todo` instead |
| `rollback` | Backup/Recovery | Use git for version control |
| `list_backups` | Backup/Recovery | Use git for version control |
| `view_log` | Debugging | Not needed for task management |
| `report_bug` | Support | Use GitHub Issues directly |

**MCP tools after changes: 27** (32 - 6 removed + 1 added)

### CLI Commands to Remove (12)

| Command | Category | Reason |
|---------|----------|--------|
| `update` | System Admin | Use `pip install --upgrade ai-todo` |
| `uninstall` | System Admin | Use `pip uninstall ai-todo` |
| `rollback` | Backup/Recovery | Use git for version control |
| `backups` | Backup/Recovery | Use git for version control |
| `list-backups` | Backup/Recovery | Alias for backups |
| `list-mode-backups` | Backup/Recovery | Use git for version control |
| `rollback-mode` | Backup/Recovery | Use git for version control |
| `log` | Debugging | Not needed for task management |
| `report-bug` | Support | Use GitHub Issues directly |
| `detect-options` | Alias | Unnecessary alias for `detect-coordination` |
| `setup-wizard` | Alias | Unnecessary alias for `setup` |
| `edit` | Convenience | Users can run `$EDITOR TODO.md` directly |

**CLI commands after removal: 34** (down from 46)

### MCP Tool to Add (1)

| Tool | CLI Equivalent | Reason |
|------|----------------|--------|
| `version` | `version` | Useful for agents to report version info |

### CLI Commands to Keep (CLI-only, no MCP equivalent needed)

| Command | Reason |
|---------|--------|
| `setup` | Interactive wizard with prompts - CLI-only |
| `serve` | Starts the MCP server - CLI-only by nature |
| `show-root` | Debug command - useful for troubleshooting |

---

## Tools to Keep

### MCP Tools (27 after cleanup)

| Category | Tools |
|----------|-------|
| **Core Tasks** | `add_task`, `add_subtask`, `complete_task`, `delete_task`, `modify_task`, `archive_task`, `restore_task`, `undo_task` |
| **Progress** | `start_task`, `stop_task`, `get_active_tasks` |
| **Display** | `list_tasks`, `show_task` |
| **Notes** | `add_note`, `delete_note`, `update_note` |
| **Relationships** | `relate_task` |
| **File Ops** | `lint`, `reformat`, `reorder`, `resolve_conflicts` |
| **Config** | `show_config`, `switch_mode`, `setup_coordination`, `detect_coordination` |
| **Tamper** | `accept_tamper` |
| **Info** | `version` |

### CLI Commands (35 after cleanup)

| Category | Commands |
|----------|----------|
| **Core Tasks** | `add`, `add-subtask`, `complete`, `delete`, `modify`, `archive`, `restore`, `undo` |
| **Progress** | `start`, `stop`, `get-active-tasks` |
| **Display** | `list`, `show` |
| **Notes** | `note`, `delete-note`, `update-note` |
| **Relationships** | `relate` |
| **File Ops** | `lint`, `reformat`, `reorder`, `resolve-conflicts` |
| **Config** | `config`, `show-config`, `switch-mode`, `setup-coordination`, `detect-coordination`, `setup` |
| **Tamper** | `tamper` |
| **Server** | `serve` |
| **Info** | `version`, `show-root` |

---

## Naming Changes (v3.0)

The following MCP tools will be renamed to match CLI command names:

| Current Name | New Name | CLI Equivalent |
|--------------|----------|----------------|
| `lint_todo` | `lint` | `lint` |
| `reformat_todo` | `reformat` | `reformat` |
| `reorder_todo` | `reorder` | `reorder` |

**Note:** This is a breaking change for existing MCP configurations referencing the old names.

---

## Decision Log

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| 1 | Remove non-core MCP tools | **YES - Remove 6** | Focus on task management | 2026-01-26 |
| 2 | Remove non-core CLI commands | **YES - Remove 12** | Focus on task management | 2026-01-26 |
| 3 | Add `version` MCP tool | **YES** | Useful for agents | 2026-01-26 |
| 4 | Rename `lint_todo` → `lint` | **YES** | Match CLI | 2026-01-26 |
| 5 | Rename `reformat_todo` → `reformat` | **YES** | Match CLI | 2026-01-26 |
| 6 | Rename `reorder_todo` → `reorder` | **YES** | Match CLI | 2026-01-26 |
| 7 | Remove `setup-wizard` CLI | **YES** | Unnecessary alias | 2026-01-26 |
| 8 | Remove `edit` CLI | **YES** | Use `$EDITOR TODO.md` | 2026-01-26 |
| 9 | Add `get-active-tasks` CLI | **YES** | Match MCP parity | 2026-01-26 |

---

## Summary

**Before:**
- MCP Tools: 32
- CLI Commands: 46

**After:**
- MCP Tools: 27 (-6 removed, +1 added = -5 net, -16%)
- CLI Commands: 35 (-12 removed, +1 added = -11 net, -24%)

**Removed:**
- MCP: `update_tool`, `uninstall_tool`, `rollback`, `list_backups`, `view_log`, `report_bug`
- CLI: `update`, `uninstall`, `rollback`, `backups`, `list-backups`, `list-mode-backups`, `rollback-mode`, `log`, `report-bug`, `detect-options`, `setup-wizard`, `edit`

**Added:**
- MCP: `version`
- CLI: `get-active-tasks`

**Renamed:**
- MCP: `lint_todo` → `lint`, `reformat_todo` → `reformat`, `reorder_todo` → `reorder`

**Benefits:**
- Simpler, more focused API
- Less maintenance burden
- Clearer purpose for AI agents
- Users can use standard tools for system admin (pip, git)

---

**Next Steps:** Review decisions, then implement removals.
