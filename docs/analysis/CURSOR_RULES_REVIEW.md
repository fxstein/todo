# Cursor Rules Review for ai-todo v3.0

**Date:** 2026-01-26
**Task:** #238.3 / #235
**Status:** PENDING REVIEW

---

## Executive Summary

The ai-todo project has **two overlapping sets** of Cursor rules that need consolidation:

1. **Repository rules** (5 files) - Manually maintained, MCP-focused
2. **Generated rules** (6 files) - Created by legacy shell script, shell-focused

**Critical Finding:** The Python package does NOT install any Cursor rules. Only the legacy shell script's `init_cursor_rules()` function creates rules.

---

## Current State Inventory

### Repository Rules (`.cursor/rules/`)

| File | Purpose | Status |
|------|---------|--------|
| `todo-ai-interaction.mdc` | MCP-first interaction rules | ✅ Good - Modern |
| `commit-standards.mdc` | Commit prefixes, task# format | ✅ Good |
| `development-workflow.mdc` | Python dev guidelines | ✅ Good |
| `release-workflow.mdc` | Release process | ✅ Good |
| `cursor-rules-guidelines.mdc` | Meta-rules for writing rules | ✅ Good |

### Generated Rules (created by shell script)

| File | Purpose | Status |
|------|---------|--------|
| `todo.ai-task-management.mdc` | Basic task rules | ⚠️ Outdated - references `.todo.ai/` |
| `todo.ai-installation.mdc` | Install instructions | ❌ **OBSOLETE** - curl download only |
| `todo.ai-bug-reporting.mdc` | Bug report workflow | ⚠️ Outdated - `./todo.ai report-bug` |
| `todo.ai-uninstall.mdc` | Uninstall workflow | ⚠️ Outdated - `./todo.ai uninstall` |
| `todo.ai-commit-format.mdc` | task# format | ✅ Good - duplicates commit-standards |
| `todo.ai-task-notes.mdc` | Note guidelines | ⚠️ Outdated - `./todo.ai note` |

---

## Issues Identified

### Issue 1: Python Package Does NOT Install Rules

**Problem:** When users install via `uv tool install ai-todo` and use the MCP server, no Cursor rules are installed.

**Impact:** AI agents won't know how to use ai-todo properly without manual rule setup.

**Evidence:**
```bash
# Search for rule installation in Python code
grep -r "cursor\|\.mdc\|rules" ai_todo/
# Only finds uninstall references, no installation
```

### Issue 2: Legacy Shell Script Auto-Generates Obsolete Rules

**Problem:** The shell script runs `init_cursor_rules` on every execution (line 7135), which creates/updates rules with outdated content.

**Impact:** If user runs the shell script, it overwrites manual MCP-focused rules with shell-focused rules.

**Evidence:**
- `todo.ai-installation.mdc` still references `curl -o todo.ai https://...`
- `todo.ai-bug-reporting.mdc` references `./todo.ai report-bug` instead of MCP tools
- `todo.ai-task-notes.mdc` references `./todo.ai note` instead of MCP tools

### Issue 3: Naming Inconsistency

**Problem:** Mixed naming across rules:
- Some files: `todo.ai-*.mdc` (old naming)
- Some files: `todo-ai-*.mdc` (transitional)
- Package name: `ai-todo` (PyPI)
- Data directory: `.ai-todo/` (new) vs `.todo.ai/` (old reference in rules)

### Issue 4: Duplicate/Overlapping Rules

**Problem:** Two rules cover commit format:
- `commit-standards.mdc` (repo rule)
- `todo.ai-commit-format.mdc` (generated)

Both have similar content about `task#` format.

### Issue 5: MCP Server Not Referenced

**Problem:** Generated rules don't mention MCP tools at all. They only reference CLI commands.

---

## Recommendations

### Decision 1: Should Python Package Install Cursor Rules?

**Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. Yes - Auto-install** | Add `init_cursor_rules()` to Python setup/serve | Seamless UX | May overwrite user rules |
| **B. Yes - On-demand** | Add `ai-todo init-rules` command | User control | Extra step required |
| **C. No - MCP handles it** | Rely on MCP server's embedded instructions | Simpler codebase | Rules not in `.cursor/rules/` |
| **D. No - Manual only** | Document rules, user copies them | Full control | Poor UX |

**Recommendation:** Option B (on-demand command) with fallback to MCP embedded instructions

### Decision 2: What Should Happen to Generated Rules?

**Options:**

| Option | Description |
|--------|-------------|
| **A. Delete all** | Remove all `todo.ai-*.mdc` files, rely on repo rules |
| **B. Migrate content** | Move useful content to repo rules, delete generated |
| **C. Update content** | Update generated rules to reference MCP tools |
| **D. Keep both** | Keep generated for shell users, repo for MCP users |

**Recommendation:** Option B - Migrate useful content, delete obsolete

### Decision 3: What Rules Should Be Embedded in MCP Server?

The MCP server can provide guidance through tool descriptions. Current approach:
- Tool descriptions guide basic usage
- No explicit rules installed

**Recommendation:** Enhance tool descriptions + provide optional `init-rules` command

### Decision 4: Naming Convention Going Forward

**Options:**

| Option | Pattern | Example |
|--------|---------|---------|
| **A. ai-todo-*** | Match PyPI name | `ai-todo-task-management.mdc` |
| **B. Keep todo.ai-*** | Legacy compat | `todo.ai-task-management.mdc` |
| **C. Generic** | No prefix | `task-management.mdc` |

**Recommendation:** Option A - `ai-todo-*.mdc` to match the official package name

---

## Proposed Actions

### Phase 1: Clean Up This Repository

1. [ ] Delete obsolete generated rules from this repo:
   - `todo.ai-installation.mdc` (obsolete - curl install)
   - `todo.ai-task-management.mdc` (duplicated by `todo-ai-interaction.mdc`)
   - `todo.ai-commit-format.mdc` (duplicated by `commit-standards.mdc`)

2. [ ] Update remaining generated rules for MCP:
   - `todo.ai-bug-reporting.mdc` → Update to reference MCP `report_bug` tool
   - `todo.ai-uninstall.mdc` → Update to reference `ai-todo uninstall` CLI
   - `todo.ai-task-notes.mdc` → Update to reference MCP `add_note` tool

3. [ ] Rename files to `ai-todo-*.mdc` pattern

### Phase 2: Update Shell Script (Optional)

1. [ ] Disable `init_cursor_rules` auto-run for dev repo (check `IS_DEV_REPO`)
2. [ ] Update embedded rule templates in shell script for MCP-first approach
3. [ ] Or: Remove rule generation entirely from shell script

### Phase 3: Add Python Rule Installation (Optional)

1. [ ] Add `ai-todo init-rules` command to install/update rules
2. [ ] Include MCP-focused rule templates in Python package

---

## Decision Log

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| 1 | Python rule installation | **A - Auto-install** | MCP server creates rule on startup if missing | 2026-01-26 |
| 2 | Generated rules handling | **A - Delete all** | Single minimal rule replaces 7 legacy files | 2026-01-26 |
| 3 | MCP embedded rules | **Embedded in server** | Rule content in `server.py`, auto-created | 2026-01-26 |
| 4 | Naming convention | **A - ai-todo-*** | Matches PyPI package name | 2026-01-26 |

---

## Files to Review

### Good (Keep As-Is)
- `.cursor/rules/todo-ai-interaction.mdc` - MCP-first, well-written
- `.cursor/rules/commit-standards.mdc` - Clear, useful
- `.cursor/rules/development-workflow.mdc` - Dev-focused
- `.cursor/rules/release-workflow.mdc` - Release process
- `.cursor/rules/cursor-rules-guidelines.mdc` - Meta-rules

### Obsolete (Delete)
- `.cursor/rules/todo.ai-installation.mdc` - Curl install is legacy

### Update Required
- `.cursor/rules/todo.ai-bug-reporting.mdc` - Change to MCP tools
- `.cursor/rules/todo.ai-uninstall.mdc` - Change to CLI command
- `.cursor/rules/todo.ai-task-notes.mdc` - Change to MCP tools
- `.cursor/rules/todo.ai-task-management.mdc` - Merge with interaction.mdc

---

**Next Steps:** Review this document, make decisions, then implement.
