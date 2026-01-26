# Cursor Rules Audit (Task #212.1)

**Date:** 2026-01-26
**Status:** Audit In Progress

## Overview

This audit identifies `.cursor/rules/*.mdc` files that contain references to the legacy shell script (`./todo.ai`) or CLI (`todo-ai`) and need updating to mandate MCP tool usage.

## Findings

### 1. `commit-prefixes.mdc`
- **Status:** ✅ Mostly OK
- **Issues:**
  - Mentions `feat: Add task filtering command` (generic example)
  - Mentions `fix: Correct task modification logic` (generic example)
- **Action:** Minor tweaks to ensure examples reflect MCP-first mindset if needed, but largely tool-agnostic.

### 2. `cursor-rules-guidelines.mdc`
- **Status:** ✅ OK
- **Issues:** None. Meta-rule about writing rules.

### 3. `releases.mdc`
- **Status:** ⚠️ Needs Update
- **Issues:**
  - Heavily shell-script focused (`./release/release.sh`).
  - This might be acceptable as releases are a CI/DevOps process, not an agent coding task.
- **Action:** Review if agents should trigger releases via MCP or if shell is fine here.

### 4. `repository-context.mdc`
- **Status:** ⚠️ Needs Update
- **Issues:**
  - Explicitly mentions "The `todo.ai` script in the root directory is the active development version".
  - Mentions `todo.ai` (zsh) vs `todo.bash`.
- **Action:** Clarify that while `todo.ai` is the dev artifact, agents should interact via MCP when possible.

## Proposed Consolidation

1. **`todo-ai-interaction.mdc`** (New):
   - **Rule:** ALWAYS use MCP tools (`add_task`, `list_tasks`, etc.) for task management.
   - **Rule:** NEVER use shell commands (`./todo.ai`, `todo-ai`) for task operations.
   - **Rule:** NEVER edit `TODO.md` manually (enforce tamper detection awareness).

2. **`development-workflow.mdc`** (New):
   - Consolidate `repository-context` and general dev guidelines.
   - Define the Python-first nature of the project.
   - Mandate `FileOps` class usage for all file I/O.

3. **`releases.mdc`** (Keep/Update):
   - **Keep:** The beta release process is critical and working.
   - **Update:** Ensure it references Python/MCP context where applicable, but keep the shell script execution flow (`./release/release.sh`) as that is the CI entry point.

4. **`commit-standards.mdc`** (Rename from `commit-prefixes`):
   - Keep strict commit format rules.
   - Ensure examples use MCP-relevant context.

## Deleted Rules (Reference)

### `bug-review-workflow.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Contained legacy CLI/shell fallbacks. Replaced by `todo-ai-interaction.mdc`.

### `commit-prefixes.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Replaced by `commit-standards.mdc`.

### `installation-migration-workflow.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Heavily tied to legacy shell/CLI installation logic. Replaced by `development-workflow.mdc`.

### `releases.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Merged into `release-workflow.mdc`.

### `repository-context.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Replaced by `development-workflow.mdc`.

### `todo.ai-beta-releases.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Renamed to `release-workflow.mdc`.

### `todo.ai-bug-reporting.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Replaced by `todo-ai-interaction.mdc`.

### `todo.ai-commit-format.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Merged into `commit-standards.mdc`.

### `todo.ai-installation.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Replaced by `development-workflow.mdc`.

### `todo.ai-task-management.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Replaced by `todo-ai-interaction.mdc`.

### `todo.ai-task-notes.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Replaced by `todo-ai-interaction.mdc`.

### `todo.ai-uninstall.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Replaced by `todo-ai-interaction.mdc`.

### `zsh-first-development.mdc`
- **Status:** 🗑️ DELETED
- **Reason:** Obsolete with the shift to Python/MCP as the primary development focus.

## New/Consolidated Rules

1. **`todo-ai-interaction.mdc`**: Master rule for MCP-first interaction.
2. **`development-workflow.mdc`**: Python-first development guidelines.
3. **`commit-standards.mdc`**: Consolidated commit formatting rules.
4. **`release-workflow.mdc`**: Definitive release process (beta + stable).
5. **`cursor-rules-guidelines.mdc`**: Meta-rules (kept as is).

## Next Steps

1. **Verify**: Ensure all new rules are active and effective.
2. **Cleanup**: Delete any remaining legacy rule files if found.
