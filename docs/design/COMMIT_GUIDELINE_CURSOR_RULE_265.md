# Design: Add commit guideline to ai-todo–written Cursor rule (task #265)

## Goal

Add a managed-file notice and three bullets to the Cursor rule text that ai-todo writes to `.cursor/rules/ai-todo-task-management.mdc`:

1. **Managed-file header** – comment at the top stating the file is managed by ai-todo and new versions may override any changes.
2. **Commit guideline** – remind agents to stage and commit `TODO.md` and `.ai-todo/` together with other changes.
3. **Task tracking** – forbid built-in TodoWrite (and similar) for task tracking; require ai-todo.

## Wording

### Managed-file comment (after frontmatter)

Add an HTML comment as the first line of the rule file so it does not affect Cursor’s use of the rule:

- `<!-- This file is managed by ai-todo. New versions may override any changes. -->`

## Bullet wording

### Task-tracking rules (after “NEVER use Cursor's built-in TODO tools”)

- **NEVER** use the built-in TodoWrite or other tools for task tracking
- **ALWAYS** use ai-todo for task tracking

### Commit guideline (from task #265, last bullet before closing paragraph)

- **When committing:** If TODO.md or `.ai-todo/` have changes, always stage and commit them together (with other changes). They are versioned like the rest of the repo.

## Placement

- **Managed-file comment:** Immediately after the YAML frontmatter (after the closing `---`), before the first heading. Do not place before the frontmatter—parsers expect line 1 to be `---`.
- **Task-tracking bullets:** Immediately after “**NEVER** use Cursor's built-in TODO tools”, before “**NEVER** edit TODO.md directly”.
- **Commit guideline:** After “Tasks are displayed in **reverse chronological order** (newest on top)”, before the closing paragraph (“The MCP server name is typically…”).

Same style throughout for bullets: bold label + explanation.

## Implementation

- **Where:** `ai_todo/mcp/server.py`, constant `AI_TODO_CURSOR_RULE`, and `_init_cursor_rules()`.
- **Change:** Add the managed-file comment at the start of `AI_TODO_CURSOR_RULE` and the three bullets in the positions above.
- **Rule update behaviour:** Always update the Cursor rule when the content that ships with the tool has changed. If the rule file exists, compare its content to `AI_TODO_CURSOR_RULE`; if different, overwrite with the shipped content. If the file does not exist, create it. So existing installs get the new bullets on next run.

## Existing installs

- **Decision:** We always update the Cursor rule when the content that ships with the tool has changed. `_init_cursor_rules()` must write or overwrite the file whenever the current file content differs from `AI_TODO_CURSOR_RULE` (not only when the file is missing).
- **Effect:** All users get the updated rule (new bullets) after upgrading and running the tool again.

## Tests

- Extend `tests/unit/test_cursor_rules.py`: assert the written rule content contains:
  - Managed-file header: "managed by ai-todo", "may override" (or similar).
  - Commit guideline: "When committing", "TODO.md", ".ai-todo/", "stage and commit them together".
  - Task-tracking rules: "TodoWrite", "task tracking", "ALWAYS use ai-todo for task tracking".

## Verification

- Run `uv run pytest tests/unit/test_cursor_rules.py`.
- Optionally run the MCP server against a temp dir and confirm the generated `.mdc` file starts with the managed-file comment and contains all three new bullets.
