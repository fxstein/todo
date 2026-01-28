# ai-todo

**AI-native task management for coding agents**

Simple, persistent, version-controlled TODO tracking that works naturally with AI agents like Cursor, Claude, and Copilot.

---

## Quick Start

Add this to your project's `.cursor/mcp.json`:

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

Then enable the server in Cursor Settings → MCP Servers → toggle **ai-todo** on.

That's it! Your AI agent can now manage tasks directly. No installation required.

**Try it:** Ask your agent to *"create a task for implementing user authentication"*

---

## Why ai-todo?

AI agents track tasks internally, but this creates a closed system that gets lost after sessions end. ai-todo provides a **permanent, version-controlled record** in your Git repository.

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
    "ai-todo": {
      "command": "uvx",
      "args": ["ai-todo", "serve", "--root", "${workspaceFolder}"]
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

**CLI Usage:** `ai-todo [command]` (e.g., `ai-todo add "My task"`, `ai-todo list`)

**MCP Server:** `ai-todo serve` (for Cursor integration)

---

## For Humans

With ai-todo, you simply tell your AI agent what you want in plain English:

- *"Create a task for implementing user authentication"*
- *"Break down the auth feature into subtasks"*
- *"Mark task 1 as complete"*
- *"Show me all tasks tagged with #bug"*
- *"Archive completed tasks"*
- *"Prune archived tasks older than 30 days"* — Keep TODO.md clean
- *"Fix the issue from #123"* — Reference GitHub Issues in tasks

Your agent handles the technical details. All tasks are stored in `TODO.md` in your repository.

---

## See It In Action

This repository uses ai-todo for its own development! Check [`TODO.md`](./TODO.md) to see:

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
