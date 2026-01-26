# Unified Executable Architecture Design

## Overview
This document outlines the architecture for combining the `ai-todo` CLI and `todo-ai-mcp` server into a single executable. This unification simplifies distribution, installation, and usage while providing a cleaner developer experience. This design supports Task #192.2.

## Goals
1. **Single Entry Point:** Users install and run one command (`ai-todo`).
2. **Unified Codebase:** Shared logic for argument parsing and configuration.
3. **Backward Compatibility:** Maintain existing CLI commands (`add`, `list`, etc.).
4. **MCP Integration:** Expose the MCP server via a `serve` subcommand.
5. **Context Awareness:** Support `--root` to pin the tool to a specific repository.

## Architecture

### 1. Command Structure
The `ai-todo` command will serve as the unified entry point.

```
todo-ai [GLOBAL_OPTIONS] [COMMAND] [ARGS]
```

**New Command:**
- `serve`: Launches the MCP server over stdio.

**Global Options:**
- `--root <path>`: Sets the working directory/context for the command.

### 2. Entry Point Refactoring (`todo_ai/cli/main.py`)
Currently, `main.py` defines the `cli` group and commands. We will extend this to include `serve`.

```python
@click.group()
@click.option("--root", help="Override repo root")
@click.pass_context
def cli(ctx, root):
    # Resolve root logic here
    # ...
```

### 3. The `serve` Command
The `serve` command will initialize and run the MCP server.

```python
@cli.command()
@click.option("--log-level", default="INFO", help="Logging verbosity")
@click.option("--log-file", type=click.Path(), help="Log file path")
@click.pass_context
def serve(ctx, log_level, log_file):
    """Start the MCP server over stdio."""
    root = ctx.obj.get("root") or os.getcwd()

    # Configure logging (CRITICAL: must not log to stdout)
    setup_logging(level=log_level, file=log_file, stream=sys.stderr)

    # Initialize and run server
    # Note: We need to ensure the server uses the 'root' for file operations
    from todo_ai.mcp.server import run_server
    asyncio.run(run_server(root))
```

### 4. MCP Server Updates (`todo_ai/mcp/server.py`)
We will rewrite the MCP server using **FastMCP** to reduce boilerplate and improve maintainability.

**Current (Standard SDK):**
- Manual tool definitions and schema generation.
- Manual request dispatching.
- ~540 lines of code.

**Proposed (FastMCP):**
- Use decorators (`@mcp.tool`) to define tools.
- Automatic schema generation from type hints.
- Automatic request routing.
- Estimated size: ~150 lines.

**Implementation:**
```python
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("todo-ai")

@mcp.tool()
def add_task(description: str, tags: list[str] = []) -> str:
    """Add a new task to TODO.md"""
    # ... call add_command ...
    return output

# ... define other tools ...

def run_server(root_path: str):
    """Run the MCP server with the specified root."""
    # Configure root context (e.g. via global var or dependency injection)
    # ...
    mcp.run(transport="stdio")
```

### 5. `pyproject.toml` Updates
We will add `fastmcp` dependency and deprecate the `todo-ai-mcp` script.

**Current:**
```toml
dependencies = [
    "mcp>=0.1.0",
    # ...
]
```

**Proposed:**
```toml
dependencies = [
    "fastmcp>=2.14.0,<3.0.0",  # Pin to v2.14.x
    # ...
]

[project.scripts]
todo-ai = "todo_ai.cli.main:cli"
# todo-ai-mcp kept for backward compatibility or removed?
# Recommendation: Keep for one version cycle with a deprecation warning, then remove.
```

## Implementation Plan

1. **Add Dependency:** Add `fastmcp` (pinned to v2.14.x) to `pyproject.toml`.
2. **Rewrite `server.py`:** Re-implement the server using FastMCP decorators.
3. **Refactor `main.py`:** Add `--root` global option handling.
4. **Implement `serve` command:** Add the command to `main.py` to run the FastMCP server.
5. **Update `mcp.json`:** Update documentation and examples to use `ai-todo serve`.
6. **Tests:** Add integration tests for `ai-todo serve` and `--root` behavior.

## Migration for Users
No user migration required as there are no active users of the MCP server yet.


## Security Considerations
- **Stdio Isolation:** Ensure no `print()` calls leak into stdout during `serve` mode, as this breaks the MCP protocol.
- **Path Traversal:** Validate `--root` path to ensure it's a valid directory.
