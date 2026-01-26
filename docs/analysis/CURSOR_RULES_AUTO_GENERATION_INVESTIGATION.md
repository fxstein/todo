# Cursor Rules Auto-Generation Investigation

**Task:** #218
**Date:** 2026-01-26
**Status:** Investigation Complete - Awaiting Review

## Problem Statement

Legacy Cursor rules keep reappearing after being cleaned up, interfering with the consolidated MCP-first workflow rules established in Task #212.

## Findings

### 1. Source of Auto-Generation

The `init_cursor_rules()` function in **`todo.bash`** (lines 1472-1740) automatically generates Cursor rules on every script execution.

**Trigger Location:** Line 7129 in `todo.bash`:

```bash
# Initialize Cursor rules if needed (check on every run, add if missing)
init_cursor_rules
```

### 2. Auto-Generated Files (6 files)

The shell script generates these files in `.cursor/rules/`:

| File | Purpose |
|------|---------|
| `todo.ai-task-management.mdc` | Basic task management rules |
| `todo.ai-installation.mdc` | Installation instructions |
| `todo.ai-bug-reporting.mdc` | Bug reporting workflow |
| `todo.ai-uninstall.mdc` | Uninstall procedure |
| `todo.ai-commit-format.mdc` | Commit message format |
| `todo.ai-task-notes.mdc` | Task notes usage |

### 3. Manually Maintained Files (5 files)

These rules are committed to git and manually maintained:

| File | Purpose |
|------|---------|
| `commit-standards.mdc` | Commit prefixes and task references |
| `cursor-rules-guidelines.mdc` | Rules for creating Cursor rules |
| `development-workflow.mdc` | Python-first development rules |
| `release-workflow.mdc` | Release process workflow |
| `todo-ai-interaction.mdc` | MCP-first interaction rules |

### 4. Current Safeguards

- Auto-generated files ARE in `.gitignore` (line 23: `.cursor/rules/todo.ai-*.mdc`)
- They are NOT committed to the repository
- The `TODO_AI_TESTING` environment variable skips generation during tests

### 5. Why This Is a Problem

1. **Conflicting Rules:** Auto-generated rules overlap with manually maintained ones:
   - `todo.ai-commit-format.mdc` vs `commit-standards.mdc`
   - `todo.ai-task-management.mdc` vs `todo-ai-interaction.mdc`

2. **Outdated Content:** Auto-generated rules reference shell script commands (`./todo.ai`) instead of Python CLI (`todo-ai`) or MCP tools

3. **Every Execution:** Running any `./todo.bash` command regenerates these files

4. **Design Intent Mismatch:** The auto-generation was designed for END USERS installing todo.ai as a tool, not for DEVELOPERS working on the codebase

## Root Cause

The shell script `todo.bash` is primarily meant for end-users who install todo.ai in their projects. For them, auto-generating helpful Cursor rules makes sense. However, in the **development repository** itself:

- We have manually curated, MCP-first rules
- The shell script runs frequently during development/testing
- Auto-generated rules override the developer experience

## Proposed Solutions

### Option A: Environment Variable Guard (Recommended)

Add a check for a `TODO_AI_DEV` environment variable to skip rule generation in development:

```bash
init_cursor_rules() {
    # Skip in tests OR in development mode
    if [[ -n "$TODO_AI_TESTING" ]] || [[ -n "$TODO_AI_DEV" ]]; then
        return 0
    fi
    # ... rest of function
}
```

**Pros:** Minimal change, explicit control
**Cons:** Developers must set env var

### Option B: Detect Development Repository

Check if we're in the todo.ai development repository and skip:

```bash
init_cursor_rules() {
    # Skip in tests
    if [[ -n "$TODO_AI_TESTING" ]]; then
        return 0
    fi

    # Skip in development repository (has todo_ai/ Python package)
    if [[ -d "${ROOT_DIR}/todo_ai" ]] && [[ -f "${ROOT_DIR}/pyproject.toml" ]]; then
        return 0
    fi
    # ... rest of function
}
```

**Pros:** Automatic detection, no env var needed
**Cons:** Could break if user has similar directory structure

### Option C: Delete Auto-Generated Files (Manual Cleanup)

Simply delete the auto-generated files and don't run `./todo.bash` directly:

```bash
rm -f .cursor/rules/todo.ai-*.mdc
```

**Pros:** Immediate fix
**Cons:** Files reappear on next shell script execution

### Option D: Remove Auto-Generation Entirely

Remove `init_cursor_rules()` call from the script since:
- Python CLI doesn't auto-generate rules
- MCP server doesn't auto-generate rules
- End users can use the Python package instead

**Pros:** Cleanest solution, aligns with Python-first direction
**Cons:** Breaks shell-script-only users who relied on this feature

## Recommendation

**Option B (Detect Development Repository)** is recommended because:

1. It's automatic - no manual setup required
2. It only affects the development repository
3. End users still get auto-generated rules
4. It aligns with the Python-first development workflow

## Files to Modify

1. `todo.bash` - Add development repository detection in `init_cursor_rules()`

## Testing Plan

1. Verify detection works in development repo
2. Verify rules still generate in a fresh user project
3. Verify `TODO_AI_TESTING` still works for tests
