# Setting Up todo.ai with Cursor (MCP)

`todo.ai` v3.0+ includes a built-in **Model Context Protocol (MCP)** server. This allows Cursor's AI agent to directly interact with your task list—reading tasks, adding items, and marking them complete—without you needing to type CLI commands or paste file contents.

## Prerequisites

-   `todo-ai` installed via pipx (v3.0+).
    ```bash
    pipx install todo-ai
    ```
-   Cursor IDE (latest version).

## Configuration

1.  **Locate the MCP Server Command:**
    
    If you installed via `pipx`, the command `todo-ai-mcp` should be available globally.
    Verify it by running:
    ```bash
    which todo-ai-mcp
    ```
    *(Copy the full path output, e.g., `/Users/username/.local/bin/todo-ai-mcp`)*

2.  **Configure Cursor:**

    -   Open **Cursor Settings** (Cmd+Shift+J or `Ctrl+Shift+J`).
    -   Navigate to **Features** > **MCP Servers**.
    -   Click **+ Add New MCP Server**.
    -   Enter the following details:
        -   **Name:** `todo-ai`
        -   **Type:** `stdio`
        -   **Command:** `todo-ai-mcp` (or the full path from step 1)
        -   **Arguments:** (Leave empty)

    *Note: If `todo-ai-mcp` is not in Cursor's PATH, explicitly use the full path found in step 1.*

3.  **Verify Connection:**
    
    Once added, the status indicator next to `todo-ai` should turn green.

## Usage in Cursor

Once connected, you can ask Cursor's AI (Composer or Chat) to manage your tasks naturally.

**Examples:**

-   "Add a task to check the logs for errors."
-   "What are my high priority tasks?"
-   "Mark task #15 as complete."
-   "Create a subtask under #10 for writing tests."

Cursor will automatically call the appropriate `todo-ai` tools (`add_task`, `list_tasks`, `complete_task`) to perform the action.

## Security & Privacy

-   The MCP server runs locally on your machine.
-   It only accesses the `TODO.md` file in the directory where the MCP server was started.
    *Note: Currently, the global `todo-ai-mcp` command typically targets the `TODO.md` in the directory where Cursor launched the server process, or defaults to the current working directory.*

