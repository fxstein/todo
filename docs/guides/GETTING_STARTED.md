# Getting Started with ai-todo

This guide will help you set up ai-todo for your development workflow. Choose the setup that matches your needs.

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
    "ai-todo": {
      "command": "uvx",
      "args": ["ai-todo", "serve", "--root", "${workspaceFolder}"]
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
ai-todo add "Implement feature X" "#feature"
ai-todo list
ai-todo complete 1
```

---

## Common Workflows

### Individual Developer

```bash
# MCP: Just add mcp.json config (see Quick Start above)

# CLI alternative:
uv tool install ai-todo
ai-todo add "Fix authentication bug" "#bug"
ai-todo complete 1
ai-todo list
```

### Team Collaboration

For teams, configure multi-user mode to prevent ID conflicts:

```bash
# Using CLI
ai-todo switch-mode multi-user

# Each team member gets their own prefix:
# Creates: #alice-50, #bob-51, etc.
```

### Feature Branch Development

Track tasks per branch:

```bash
ai-todo switch-mode branch

# On branch: feature/auth
ai-todo add "Add login page" "#frontend"
# Creates: #feature-50
```

---

## Numbering Modes

ai-todo supports four numbering modes:

| Mode | Format | Best For |
|------|--------|----------|
| **single-user** | `#1`, `#2` | Individual developers |
| **multi-user** | `#alice-50` | Teams without coordination |
| **branch** | `#feature-50` | Feature branch workflows |
| **enhanced** | `#alice-50` (atomic) | Large teams with coordination |

Switch modes:

```bash
ai-todo switch-mode <mode>
```

See [Numbering Modes Guide](NUMBERING_MODES_GUIDE.md) for details.

---

## TODO.md Format

The `TODO.md` file is a **managed file** — don't edit it manually. Use ai-todo commands to ensure consistent formatting.

**Check formatting:**

```bash
ai-todo lint
```

**Fix formatting:**

```bash
ai-todo reformat
```

---

## Quick Reference

### Task Management

```bash
ai-todo add "Task description" "#tags"
ai-todo add-subtask 1 "Subtask description"
ai-todo start 1
ai-todo complete 1
ai-todo list
ai-todo show 1
ai-todo archive 1
```

### Configuration

```bash
ai-todo config                    # View configuration
ai-todo switch-mode <mode>        # Change numbering mode
ai-todo setup-coordination <type> # Configure coordination
```

### Maintenance

```bash
# Prune old archived tasks
ai-todo prune                     # Remove archived tasks older than 30 days
ai-todo prune --days 60           # Custom retention period
ai-todo prune --from-task 100     # Remove tasks #1 to #100
ai-todo prune --dry-run           # Preview what would be pruned

# Empty trash (remove expired deleted tasks)
ai-todo empty-trash               # Remove deleted tasks older than 30 days
ai-todo empty-trash --dry-run     # Preview what would be removed
```

> **Note:** Pruning creates automatic backups in `.ai-todo/archives/` with complete restoration capability.
>
> **Note:** Empty trash permanently removes expired deleted tasks (30-day retention) with no backup. Tasks are auto-removed on MCP server startup and after `ai-todo delete` commands.

### Information

```bash
ai-todo version
ai-todo --help
ai-todo log
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
- **GitHub:** https://github.com/fxstein/ai-todo
- **Issues:** https://github.com/fxstein/ai-todo/issues
