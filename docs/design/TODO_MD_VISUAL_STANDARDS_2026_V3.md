# TODO.md Visual Standards

**Status**: Approved
**Task**: #200.2
**Date**: 2026-01-25

## 1. Introduction
This document defines the strict visual and formatting standards for `TODO.md`. These standards must be enforced by the linter, the reformatter, and all mutation commands to ensure consistency, readability, and parsing reliability.

## 2. File Structure

### 2.1. Header
The file **MUST** start with the following header block:
```markdown
# todo.ai ToDo List

> ⚠️ **MANAGED FILE**: Do not edit manually. Use `todo-ai` (CLI/MCP) or `todo.ai` to manage tasks.
```
* **H1**: `# todo.ai ToDo List`
* **Warning**: A blockquote warning users against manual edits, referencing the v3.0 tools (MCP/CLI).
* **Spacing**: One blank line between H1 and the warning blockquote.

### 2.2. Sections
The file is divided into three main sections:
[0-9]. `## Tasks`
[0-9]. `## Archived Tasks`
[0-9]. `## Deleted Tasks`

* **Spacing**:
    * **Before Section Header**: Two blank lines followed by a horizontal separator `---` and another two blank lines (except for the first section if it follows the header immediately, then just one blank line and no separator).
    * **After Section Header**: No blank lines (tasks start immediately).

    Example:
    ```markdown
    ## Tasks
    ...

    ---

    ## Archived Tasks
    ...

    ---

    ## Deleted Tasks
    ```

### 2.3. Footer
The file **MUST** end with a footer section containing metadata.
```markdown
---
**todo-ai (mcp)** v3.0.0 | Last Updated: YYYY-MM-DD HH:MM:SS
```
* **Separator**: `---` (horizontal rule).
* **Content**: Tool variant (e.g., `todo.ai`, `todo-ai (cli)`, `todo-ai (mcp)`), version, and last update timestamp.
* **Spacing**: Two blank lines before the separator.

## 3. Task Formatting

### 3.1. Syntax
All tasks must follow this regex-compatible format:
```regex
^(\s*)- \[([ xD])\] \*\*#(task_id)\*\* (.*?) (#.*)?(\s+\(.*\))?$
```
* **Indent**: 0, 2, or 4 spaces (strictly enforced).
* **Marker**: `- [ ]` (active), `- [x]` (completed), `- [D]` (deleted).
* **ID**: `**#ID**` (bolded, starts with `#`).
* **Description**: Plain text.
* **Tags**: Optional, space-separated, starting with `#` and wrapped in backticks (e.g., `#tag`).
* **Metadata**: Optional, in parentheses at the end (e.g., completion date).

### 3.2. Indentation Levels
* **Level 0 (Root)**: 0 spaces.
* **Level 1 (Subtask)**: 2 spaces.
* **Level 2 (Sub-subtask)**: 4 spaces.
* **Max Depth**: Level 2 (3 levels total). Deeper nesting is not supported.

### 3.3. Spacing Rules
* **Root Tasks**:
    * Must be separated by **one blank line** from the preceding task.
    * This applies to ALL root tasks, regardless of whether they have children or notes, to ensure consistency.
* **Subtasks**:
    * **No blank lines** between subtasks of the same parent.
    * This applies even if subtasks have notes.

### 3.4. Task States
* **Active**: `- [ ] **#123** Description` `#tag`
* **Completed**: `- [x] **#123** Description` `#tag` `(YYYY-MM-DD)`
    * Date is required.
    * Space between tags and date.
* **Deleted**: `- [D] **#123** Description` `#tag` `(deleted YYYY-MM-DD, expires YYYY-MM-DD)`
    * Moved to `## Deleted Tasks` section.

### 3.5. Positioning & Movement
* **New Tasks**:
    * **Root Tasks**: Prepended to the **top** of the `## Tasks` section.
    * **Subtasks**: Prepended to the **top** of their parent's subtask list.
* **Completion**:
    * **Strict In-Place Update**: Marking a task as complete (`[x]`) **MUST NOT** change its position or the position of its subtasks.
    * **No Sorting**: Do not re-sort the `## Tasks` section to group active/completed tasks. This preserves context and minimizes git diffs.
* **Archival**:
    * Moves completed root tasks (and their subtasks) to the `## Archived Tasks` section.
    * Prepended to the **top** of the section.
* **Deletion**:
    * Moves tasks to the `## Deleted Tasks` section.
    * Prepended to the **top** of the section.

## 4. Note Formatting

### 4.1. Syntax
Notes **MUST** use the blockquote syntax with specific indentation relative to their parent task.
```markdown
[indent]  > [content]
```
* **Indent**: Parent task's indent + 2 spaces.
* **Marker**: `>` (greater than) + space.
* **Content**: Text.

### 4.2. Examples
* **Root Task Note**:
    ```markdown
    - [ ] **#1** Task
      > Note content
    ```
* **Level 1 Subtask Note**:
    ```markdown
      - [ ] **#1.1** Subtask
        > Note content
    ```
* **Multi-line Notes**:
    Every line of the note must include the indentation and marker.
    ```markdown
    - [ ] **#1** Task
      > First line of note
      > Second line of note
    ```

## 5. Implementation Requirements

### 5.1. Mutation Commands
All commands that modify `TODO.md` (`add`, `modify`, `complete`, `delete`, `archive`, `move`) **MUST** generate output that strictly adheres to these standards.
* **No "Fix-up"**: The linter/reformatter should not be relied upon to fix output from standard commands.
* **Verification**: Unit tests for these commands must verify exact string matching against these standards.

### 5.2. Linter (`lint`)
The linter must:
1. Validate strict 2-space indentation.
2. Validate blank line rules (1 blank line between root tasks).
3. Validate note formatting (indent + `>` marker).
4. Validate header/footer presence and format.
5. Report violations with specific line numbers and error codes.

### 5.3. Reformatter (`reformat`)
The reformatter must:
1. Fix indentation (snap to 0, 2, 4 spaces).
2. Insert missing blank lines between root tasks.
3. Fix note formatting (add missing `>` marker or fix indentation).
4. Regenerate Header and Footer if missing or malformed.
5. **Preserve Data**: Never modify task IDs, descriptions, tags, or dates during reformatting.

## 6. Migration Plan
[0-9]. **Update Tooling**: Implement standards in `FileOps` class (Python).
[0-9]. **Update Commands**: Ensure `add`, `modify`, etc., use the updated `FileOps`.
[0-9]. **One-Time Migration**: Run `reformat` on existing `TODO.md` files to bring them up to spec.
