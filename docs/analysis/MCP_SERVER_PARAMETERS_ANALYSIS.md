# MCP Server Default Parameters Investigation

## Overview
This document analyzes the standard parameters and configuration options that a well-behaved MCP server should support, particularly when integrated into a CLI tool via a `serve` command. This investigation supports Task #192.1.

## Standard MCP Server Parameters

Based on the official MCP SDK (`mcp` package) and common practices, MCP servers typically support the following configuration options:

### 1. Transport Configuration
MCP servers communicate via a transport layer. The most common for local tools is `stdio`.

- **stdio (Standard Input/Output):**
  - Default for local integration (Cursor, Claude Desktop).
  - No specific arguments needed usually, but some servers allow explicit selection.
  - **Recommendation:** Default to `stdio` when running `ai-todo serve`.

- **SSE (Server-Sent Events):**
  - Used for remote or HTTP-based servers.
  - **Decision:** We will **NOT** support SSE for the foreseeable future. `ai-todo` is a local developer tool that requires direct access to the local filesystem (`TODO.md`). A remote server implementation would complicate file access and is out of scope.
  - **Recommendation:** Stick strictly to `stdio` transport.

### 2. Logging and Debugging
Debugging MCP servers can be difficult since stdout is used for protocol communication.

- **Log Level:** `--log-level [DEBUG|INFO|WARNING|ERROR]`
  - Controls verbosity of logs.
- **Log File:** `--log-file <path>`
  - Redirects logs to a file instead of stderr (since stdout is reserved).
  - **Critical:** Ensure logs do NOT pollute stdout, as that breaks the JSON-RPC protocol.

### 3. Root/Context Configuration
This is the primary requirement for `ai-todo`.

- **Root Directory:** `--root <path>`
  - Specifies the workspace or repository root.
  - For `ai-todo`, this determines where `TODO.md` is located.
  - Should default to current working directory (`CWD`) if not specified.

### 4. File Path Overrides
Specific to `ai-todo`, we might want to override the filename itself.

- **Todo File:** `--todo-file <filename>`
  - Defaults to `TODO.md`.
  - Allows using `TASKS.md` or other names.

## Proposed `serve` Command Interface

Based on the investigation, the `ai-todo serve` command should support the following signature:

```bash
ai-todo serve [OPTIONS]
```

### Options:

| Option | Default | Description |
|--------|---------|-------------|
| `--root <path>` | `CWD` | Path to the project root directory. |
| `--todo-file <name>` | `TODO.md` | Name of the todo file (relative to root). |
| `--log-level <level>` | `INFO` | Logging verbosity. |
| `--log-file <path>` | `stderr` | Path to log file (useful for debugging). |

## Implementation Strategy

1. **Click Command:** Implement `serve` as a `click` command in `todo_ai/cli/main.py`.
2. **Argument Parsing:** Use `click` options to parse arguments.
3. **Server Initialization:**
   - Pass parsed arguments to `MCPServer` constructor.
   - Update `MCPServer.__init__` to accept `root_path` and `todo_filename`.
4. **Stdio Protection:**
   - Ensure all logging within the server execution context is directed to stderr or a file.
   - Prevent any `print()` calls to stdout (except protocol messages).

## Comparison with Existing `todo-ai-mcp`
The current `todo-ai-mcp` entry point (`todo_ai/mcp/__main__.py`) takes no arguments and hardcodes the path. The new `serve` command will replace this with a flexible, configurable entry point.

## Conclusion
We should implement `ai-todo serve` with support for `--root`, `--todo-file`, and logging options. This aligns with MCP best practices and solves the portability issues identified in Task #191.
