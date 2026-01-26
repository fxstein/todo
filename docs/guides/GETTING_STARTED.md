# Getting Started with todo.ai

This guide will help you set up `todo.ai` for your development workflow. Choose the setup that matches your needs.

> **Related Documentation:**
> - [FAQ](../FAQ.md) - Common questions answered
> - [MCP Setup Guide](../user/MCP_SETUP.md) - Detailed Cursor integration
> - [Migration Guide](../user/PYTHON_MIGRATION_GUIDE.md) - Upgrading from v2.x shell script

---

## Quick Start: MCP Integration (Recommended)

For AI agent integration with Cursor or similar IDEs, add this to your project's `.cursor/mcp.json`:

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

**That's it!** Your AI agent can now manage tasks directly. No installation required.

> **Prerequisite:** [uv](https://docs.astral.sh/uv/) must be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

**Try it:** Ask your agent to *"create a task for implementing user authentication"*

---

## Alternative: CLI Installation

For command-line usage or permanent setup. Requires Python 3.10+.

```bash
# Install globally (recommended)
uv tool install ai-todo

# Or with pipx
pipx install ai-todo
```

**Usage:**

```bash
todo-ai add "Implement feature X" "#feature"
todo-ai list
todo-ai complete 1
```

---

## Legacy: Shell Script

For environments without Python 3.10+:

```bash
# Smart installer (auto-detects your shell)
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh

# Initialize
./todo.ai init
```

**Usage:** `./todo.ai [command]`

> **Note:** The shell script lacks MCP integration. We recommend Python v3.0+ when possible.

---

## Common Workflows

### Individual Developer

```bash
# MCP: Just add mcp.json config (see Quick Start above)

# CLI alternative:
uv tool install ai-todo
todo-ai add "Fix authentication bug" "#bug"
todo-ai complete 1
todo-ai list
```

### Team Collaboration

For teams, configure multi-user mode to prevent ID conflicts:

```bash
# Using CLI
todo-ai switch-mode multi-user

# Each team member gets their own prefix:
# Creates: #alice-50, #bob-51, etc.
```

### Feature Branch Development

Track tasks per branch:

```bash
todo-ai switch-mode branch

# On branch: feature/auth
todo-ai add "Add login page" "#frontend"
# Creates: #feature-50
```

---

## Numbering Modes

todo.ai supports four numbering modes:

| Mode | Format | Best For |
|------|--------|----------|
| **single-user** | `#1`, `#2` | Individual developers |
| **multi-user** | `#alice-50` | Teams without coordination |
| **branch** | `#feature-50` | Feature branch workflows |
| **enhanced** | `#alice-50` (atomic) | Large teams with coordination |

Switch modes:

```bash
todo-ai switch-mode <mode>
```

See [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md) for details.

---

## TODO.md Format

The `TODO.md` file is a **managed file** — don't edit it manually. Use todo-ai commands to ensure consistent formatting.

**Check formatting:**

```bash
todo-ai lint
```

**Fix formatting:**

```bash
todo-ai reformat
```

---

## Quick Reference

### Task Management

```bash
todo-ai add "Task description" "#tags"
todo-ai add-subtask 1 "Subtask description"
todo-ai start 1
todo-ai complete 1
todo-ai list
todo-ai show 1
todo-ai archive 1
```

### Configuration

```bash
todo-ai config                    # View configuration
todo-ai switch-mode <mode>        # Change numbering mode
todo-ai setup-coordination <type> # Configure coordination
```

### Information

```bash
todo-ai version
todo-ai --help
todo-ai log
```

---

## Next Steps

1. **Set up MCP** — Add `.cursor/mcp.json` for AI agent integration
2. **Try basic commands** — `add`, `list`, `complete`
3. **Configure for your team** — Choose a numbering mode
4. **Read the docs:**
   - [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md)
   - [Usage Patterns](USAGE_PATTERNS.md)
   - [FAQ](../FAQ.md)

---

## Need Help?

- **Documentation:** See the [docs index](../README.md)
- **FAQ:** [Common questions](../FAQ.md)
- **GitHub:** https://github.com/fxstein/todo.ai
- **Issues:** https://github.com/fxstein/todo.ai/issues
