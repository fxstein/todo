# Migration Guide: Shell Script to Python (v3.0)

This guide explains how to upgrade from the legacy `todo.ai` shell script (v2.x) to the new Python-based version (v3.0).

## Overview

Version 3.0 is a complete rewrite in Python, offering:

- **MCP Integration:** AI agents interact directly with your task list
- **Dual Interfaces:** MCP Server + Standard CLI
- **Cross-Platform:** Native support for macOS, Linux, and Windows
- **Zero-Data Migration:** Fully compatible with existing `TODO.md` and `.todo.ai/`

## Recommended: Zero-Install MCP Setup

The easiest migration path is to skip CLI installation entirely and use MCP with `uvx`:

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

**Prerequisite:** Install [uv](https://docs.astral.sh/uv/) first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**That's it!** Your AI agent can now manage tasks. The shell script can remain as a fallback.

## Alternative: CLI Installation

If you prefer command-line access, install the CLI globally:

```bash
# Using uv (recommended)
uv tool install ai-todo

# Or with pipx
pipx install ai-todo
```

**Prerequisite:** Python 3.10+

### Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installing pipx (alternative)

**macOS:**

```bash
brew install pipx
pipx ensurepath
```

**Linux/Windows:** Follow the [pipx installation guide](https://pypa.github.io/pipx/).

## Migration Steps

Since v3.0 uses the exact same file formats (`TODO.md`, `.todo.ai/config.yaml`), **no data migration is required**.

### 1. Verify Installation

```bash
todo-ai version
```

### 2. Replace Shell Script (Optional)

If you want to remove the legacy script:

```bash
git rm todo.ai
```

### 3. Update Your Workflow

| Old (Shell) | New (CLI) |
|-------------|-----------|
| `./todo.ai list` | `todo-ai list` |
| `./todo.ai add "Task"` | `todo-ai add "Task"` |
| `./todo.ai complete 1` | `todo-ai complete 1` |

Core command syntax is preserved.

## Setting Up MCP (Cursor Integration)

See [MCP_SETUP.md](MCP_SETUP.md) for detailed Cursor integration instructions.

## Troubleshooting

**"Command not found: todo-ai"**

Ensure your tool directory is in PATH:

```bash
# For uv
echo $PATH | grep -q ".local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# For pipx
pipx ensurepath
```

Restart your terminal after updating PATH.

**"Config/Data Issues"**

Run `todo-ai list` to verify your existing `TODO.md` parses correctly. The tool preserves all existing data.

## Need Help?

- **FAQ:** [Common questions](../FAQ.md)
- **MCP Setup:** [Cursor integration](MCP_SETUP.md)
- **Issues:** https://github.com/fxstein/todo.ai/issues
