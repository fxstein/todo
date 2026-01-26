# todo.ai

**AI-native task management for coding agents**

Simple, persistent, version-controlled TODO tracking that works naturally with AI agents like Cursor, Claude, and Copilot.

---

## Quick Start

Add this to your project's `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "todo-ai": {
      "command": "uvx",
      "args": ["--from", "ai-todo", "todo-ai", "serve", "--root", "${workspaceFolder}"]
    }
  }
}
```

That's it! Your AI agent can now manage tasks directly. No installation required.

**Try it:** Ask your agent to *"create a task for implementing user authentication"*

---

## Why todo.ai?

AI agents track tasks internally, but this creates a closed system that gets lost after sessions end. todo.ai provides a **permanent, version-controlled record** in your Git repository.

- **Persistent** — Tasks survive across sessions, restarts, and time
- **Version Controlled** — Tracked in Git alongside your code
- **AI-Native** — MCP integration for direct agent interaction
- **Human Readable** — Plain Markdown in standard TODO.md format
- **Zero Config** — Works immediately, no setup required
- **Instant & Local** — No API calls, authentication, or rate limits

---

## Installation Options

### Option A: Zero-Install MCP (Recommended)

For AI agent integration via Cursor or similar IDEs. Uses `uvx` to run on-demand without permanent installation.

**Project-specific setup** (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "todo-ai": {
      "command": "uvx",
      "args": ["--from", "ai-todo", "todo-ai", "serve", "--root", "${workspaceFolder}"]
    }
  }
}
```

Requires [uv](https://docs.astral.sh/uv/) to be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

### Option B: System Installation

For CLI usage or permanent MCP server setup. Requires Python 3.10+.

```bash
# Install globally (recommended)
uv tool install ai-todo

# Or with pipx
pipx install ai-todo
```

**CLI Usage:** `todo-ai [command]` (e.g., `todo-ai add "My task"`, `todo-ai list`)

**MCP Server:** `todo-ai serve` (for Cursor integration)

### Option C: Legacy Shell Script

For environments without Python 3.10+:

```bash
# Smart installer (detects your shell)
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

**Usage:** `./todo.ai [command]`

> **Note:** The shell script provides core functionality but lacks MCP integration. We recommend upgrading to Python v3.0+ when possible.

---

## For Humans

With todo.ai, you simply tell your AI agent what you want in plain English:

- *"Create a task for implementing user authentication"*
- *"Break down the auth feature into subtasks"*
- *"Mark task 1 as complete"*
- *"Show me all tasks tagged with #bug"*
- *"Archive completed tasks"*
- *"Fix the issue from #123"* — Reference GitHub Issues in tasks

Your agent handles the technical details. All tasks are stored in `TODO.md` in your repository.

---

## See It In Action

This repository uses todo.ai for its own development! Check [`TODO.md`](./TODO.md) to see:

- Task hierarchies with subtasks
- Tag-based organization (`#feature`, `#bug`, `#documentation`)
- Completion tracking and archiving
- Real development workflow in action

---

## Documentation

- **[MCP Setup Guide](docs/user/MCP_SETUP.md)** — Detailed Cursor integration
- **[Migration Guide](docs/user/PYTHON_MIGRATION_GUIDE.md)** — Upgrading from v2.x shell script
- **[Getting Started](docs/guides/GETTING_STARTED.md)** — Complete setup walkthrough
- **[FAQ](docs/FAQ.md)** — Common questions answered
- **[Full Documentation](docs/README.md)** — All guides and references

---

## License

Apache License 2.0 — See [LICENSE](LICENSE)
