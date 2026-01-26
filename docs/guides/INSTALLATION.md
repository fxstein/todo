# Installation

## Quick Install (Recommended)

For most users, install via `uv`:

```bash
# Install uv first (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install ai-todo
uv tool install ai-todo
```

**Verify installation:**

```bash
ai-todo version
```

## Installation Methods

### Method 1: Zero-Install MCP (Best for Cursor users)

No permanent installation needed. Add this to your project's `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "ai-todo": {
      "command": "uvx",
      "args": ["--from", "ai-todo", "ai-todo", "serve", "--root", "${workspaceFolder}"]
    }
  }
}
```

Your AI agent can now manage tasks directly.

**Requirement:** [uv](https://docs.astral.sh/uv/) must be installed.

### Method 2: Global CLI Installation

For command-line usage:

```bash
# Using uv (recommended - faster, more reliable)
uv tool install ai-todo

# Or with pipx
pipx install ai-todo
```

**Requirement:** Python 3.10+

### Method 3: pipx

```bash
# Install pipx first
brew install pipx  # macOS
# or: python -m pip install --user pipx

pipx ensurepath
pipx install ai-todo
```

## Requirements

| Method | Requirements |
|--------|--------------|
| **Zero-Install MCP** | uv, Cursor IDE |
| **uv tool install** | uv, Python 3.10+ |
| **pipx install** | pipx, Python 3.10+ |

## Troubleshooting

### "Command not found: ai-todo"

Ensure your tool directory is in PATH:

```bash
# For uv
echo $PATH | grep -q ".local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# For pipx
pipx ensurepath
```

Restart your terminal after updating PATH.

### "Python version too old"

ai-todo requires Python 3.10+. Check your version:

```bash
python --version
```

Install a newer version via:

- **macOS:** `brew install python@3.12`
- **Linux:** Use pyenv or your package manager
- **Windows:** Download from python.org

### "uv not found"

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### MCP Server Not Connecting

1. Verify uv is installed: `which uv`
2. Check Cursor settings for MCP server status
3. Restart Cursor after adding mcp.json

## Upgrading

```bash
# uv
uv tool upgrade ai-todo

# pipx
pipx upgrade ai-todo
```

## Uninstalling

```bash
# uv
uv tool uninstall ai-todo

# pipx
pipx uninstall ai-todo
```

Your `TODO.md` and `.ai-todo/` data are preserved.
