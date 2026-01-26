# Setting Up ai-todo with Cursor (MCP)

ai-todo v3.0+ includes a built-in **Model Context Protocol (MCP)** server. This allows Cursor's AI agent to directly interact with your task list—reading tasks, adding items, and marking them complete—without you needing to type CLI commands or paste file contents.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Cursor IDE (latest version)

## Configuration

### Project-Specific Configuration (Recommended)

Create a `.cursor/mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "ai-todo": {
      "command": "uvx",
      "args": ["ai-todo", "serve", "--root", "${workspaceFolder}"]
    }
  }
}
```

This configuration:

1. Uses `uvx` to run `ai-todo` on-demand without permanent installation.
2. Runs the `serve` command to start the MCP server.
3. Sets the `--root` to the current workspace folder, ensuring the correct `TODO.md` is used.

### Global Configuration

If you prefer a global setup (not recommended for multiple projects), you can configure it in Cursor Settings:

1. **Install ai-todo:**

    ```bash
    uv tool install ai-todo
    ```

2. **Locate the Command:** `which ai-todo`

3. **Configure Cursor:**
   - **Name:** `ai-todo`
   - **Type:** `stdio`
   - **Command:** `ai-todo` (or full path)
   - **Arguments:** `serve`

   *Note: Without the `--root` argument, the global server will look for `TODO.md` in the directory where Cursor was launched.*

4. **Verify Connection:**

    Once added, the status indicator next to `ai-todo` should turn green.

## Usage in Cursor

Once connected, you can ask Cursor's AI (Composer or Chat) to manage your tasks naturally.

**Examples:**

- "Add a task to check the logs for errors."
- "What are my high priority tasks?"
- "Mark task #15 as complete."
- "Create a subtask under #10 for writing tests."

Cursor will automatically call the appropriate ai-todo tools (`add_task`, `list_tasks`, `complete_task`) to perform the action.

## Security & Privacy

- The MCP server runs locally on your machine.
- It only accesses the `TODO.md` file in the specified root directory.
- No data is sent to external servers.
