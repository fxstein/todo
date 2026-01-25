# Setting Up todo.ai with Cursor (MCP)

`todo.ai` v3.0+ includes a built-in **Model Context Protocol (MCP)** server. This allows Cursor's AI agent to directly interact with your task list—reading tasks, adding items, and marking them complete—without you needing to type CLI commands or paste file contents.

## Prerequisites

- `todo-ai` installed via `uv` (recommended) or `pipx` (v3.0+).
    ```bash
    # Using uv (recommended - faster, more reliable)
    uv tool install ai-todo

    # Alternative: pipx
    pipx install ai-todo
    ```
- Cursor IDE (latest version).

## Configuration

### Project-Specific Configuration (Recommended)

To ensure `todo-ai` uses the correct `TODO.md` file for your project, create a `.cursor/mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "todo-ai": {
      "command": "uvx",
      "args": [
        "todo-ai",
        "serve",
        "--root",
        "${workspaceFolder}"
      ]
    }
  }
}
```

This configuration:
1. Uses `uvx` to run `todo-ai` without permanent installation (or uses installed version if available).
2. Runs the `serve` command to start the MCP server.
3. Sets the `--root` to the current workspace folder, ensuring the correct `TODO.md` is used.

### Global Configuration

If you prefer a global setup (not recommended for multiple projects), you can configure it in Cursor Settings:

1. **Locate the Command:** `which todo-ai`
2. **Configure Cursor:**
   - **Name:** `todo-ai`
   - **Type:** `stdio`
   - **Command:** `todo-ai` (or full path)
   - **Arguments:** `serve`

   *Note: Without the `--root` argument, the global server will look for `TODO.md` in the directory where Cursor was launched.*

3. **Verify Connection:**

    Once added, the status indicator next to `todo-ai` should turn green.

## Usage in Cursor

Once connected, you can ask Cursor's AI (Composer or Chat) to manage your tasks naturally.

**Examples:**

- "Add a task to check the logs for errors."
- "What are my high priority tasks?"
- "Mark task #15 as complete."
- "Create a subtask under #10 for writing tests."

Cursor will automatically call the appropriate `todo-ai` tools (`add_task`, `list_tasks`, `complete_task`) to perform the action.

## Security & Privacy

- The MCP server runs locally on your machine.
- It only accesses the `TODO.md` file in the directory where the MCP server was started.
    *Note: Currently, the global `todo-ai-mcp` command typically targets the `TODO.md` in the directory where Cursor launched the server process, or defaults to the current working directory.*
