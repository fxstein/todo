# Migration Guide: Shell Script to Python (v3.0)

This guide explains how to upgrade from the legacy `todo.ai` shell script (v2.x) to the new Python-based version (v3.0).

## Overview

Version 3.0 is a complete rewrite in Python, offering:
- **Dual Interfaces:** Standard CLI + AI-native MCP (Model Context Protocol) Server.
- **Improved Performance:** Faster parsing and task management.
- **Cross-Platform Support:** Native support for macOS, Linux, and Windows.
- **Zero-Data Migration:** Fully compatible with your existing `TODO.md` and `.todo.ai/` configuration.

## Prerequisites

- **Python 3.8+** installed on your system.
- **pipx** (recommended): A tool for installing and running Python applications in isolated environments.

### Installing pipx (if not installed)

**macOS:**
```bash
brew install pipx
pipx ensurepath
```

**Linux/Windows:**
Follow the official [pipx installation guide](https://pypa.github.io/pipx/).

## Installation

We recommend installing `todo-ai` globally using `pipx`. This ensures it doesn't conflict with other Python packages.

```bash
pipx install todo-ai
```

This will expose two commands globally:
1. `todo-ai`: The CLI tool (replaces `./todo.ai`).
2. `todo-ai-mcp`: The MCP server for AI agents.

## Migrating from Shell Script

Since v3.0 uses the exact same file formats (`TODO.md`, `.todo.ai/config.yaml`, `.todo.ai/.todo.ai.serial`), **no data migration is required**. You can simply start using the new command in your existing repositories.

### 1. Verify Installation

Check the version:
```bash
todo-ai --version
```

### 2. Replace Local Script (Optional but Recommended)

If you have the `todo.ai` shell script committed in your repository root:

1. **Remove the shell script:**
    ```bash
    git rm todo.ai
    ```

2. **Update your workflow:**
    Instead of running `./todo.ai [command]`, now run `todo-ai [command]`.

    *Example:*
    ```bash
    # Old
    ./todo.ai list

    # New
    todo-ai list
    ```

### 3. Usage

The command syntax is preserved for core operations:

- `todo-ai list`
- `todo-ai add "My task" "#tag"`
- `todo-ai complete <id>`

## Setting up AI Agent Integration (MCP)

The major new feature in v3.0 is the MCP Server, which allows AI agents (like Cursor) to directly read and manipulate your task list safely and structuredly.

See [MCP_SETUP.md](MCP_SETUP.md) for detailed setup instructions for Cursor.

## Troubleshooting

**"Command not found: todo-ai"**
Ensure your `pipx` binary directory is in your PATH. Run `pipx ensurepath` and restart your terminal.

**Config/Data Issues**
If you encounter issues reading your existing `TODO.md`:
1. Run `todo-ai list` to see if it parses correctly.
2. The tool automatically attempts to preserve custom headers/footers in `TODO.md`.
