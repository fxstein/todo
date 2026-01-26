# Migration Guide: Shell Script to Python (v3.0)

This guide explains how to upgrade from the legacy shell script (v2.x) to the new Python-based version (v3.0).

## Overview

Version 3.0 is a complete rewrite in Python, offering:

- **MCP Integration:** AI agents interact directly with your task list
- **Dual Interfaces:** MCP Server + Standard CLI
- **Cross-Platform:** Native support for macOS, Linux, and Windows
- **Zero-Data Migration:** Fully compatible with existing `TODO.md` and `.ai-todo/`

## Recommended: Zero-Install MCP Setup

The easiest migration path is to skip CLI installation entirely and use MCP with `uvx`:

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

**Prerequisite:** Install [uv](https://docs.astral.sh/uv/) first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**That's it!** Your AI agent can now manage tasks directly.

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

Since v3.0 uses the exact same file formats (`TODO.md`, `.ai-todo/config.yaml`), **no data migration is required**.

> **Note:** If you have an existing `.todo.ai/` directory, it will be automatically migrated to `.ai-todo/` on first use.

### 1. Verify Installation

```bash
ai-todo version
```

### 2. Remove Legacy Shell Script (Optional)

If you want to remove the legacy script:

```bash
git rm todo.ai todo.bash  # if present
```

### 3. Update Your Workflow

| Old (Shell) | New (CLI) |
|-------------|-----------|
| `./todo.ai list` | `ai-todo list` |
| `./todo.ai add "Task"` | `ai-todo add "Task"` |
| `./todo.ai complete 1` | `ai-todo complete 1` |

Core command syntax is preserved.

## Setting Up MCP (Cursor Integration)

See [MCP_SETUP.md](MCP_SETUP.md) for detailed Cursor integration instructions.

## Troubleshooting

**"Command not found: ai-todo"**

Ensure your tool directory is in PATH:

```bash
# For uv
echo $PATH | grep -q ".local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# For pipx
pipx ensurepath
```

Restart your terminal after updating PATH.

**"Config/Data Issues"**

Run `ai-todo list` to verify your existing `TODO.md` parses correctly. The tool preserves all existing data.

## Need Help?

- **FAQ:** [Common questions](../FAQ.md)
- **MCP Setup:** [Cursor integration](MCP_SETUP.md)
- **Issues:** https://github.com/fxstein/ai-todo/issues
