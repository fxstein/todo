# Release Summary: v3.0.0b18

## Major Naming Unification

This release completes a comprehensive rename from `todo.ai` to `ai-todo` across the entire project. The unified naming eliminates confusion between the various component names (repository, PyPI package, CLI command) by standardizing on `ai-todo` everywhere.

**Key changes:**
- **CLI command:** `todo-ai` → `ai-todo`
- **Data directory:** `.todo.ai/` → `.ai-todo/` (automatic migration on startup)
- **Python package:** `todo_ai/` → `ai_todo/`
- **GitHub repository:** Renamed to `ai-todo`
- **Shell scripts:** Moved to `legacy/` directory (deprecated)

The migration is transparent for existing users - the tool automatically detects and migrates old `.todo.ai/` directories to the new `.ai-todo/` format on first run.

## Additional Improvements

- **3-level task nesting:** Tasks can now have sub-subtasks (e.g., #1.2.3)
- **Cursor rules enhancement:** Added guidance for "task list" (hierarchical) vs "tasks" (flat) terminology
- **Documentation overhaul:** All user-facing docs updated with MCP-first approach and new naming
