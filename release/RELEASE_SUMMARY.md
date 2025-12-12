# Release v3.0.0: The AI-Native Python Rewrite

This is a milestone release that transforms `todo.ai` from a shell script into a robust, AI-native Python application. Version 3.0 introduces a dual-interface architecture: a standard CLI for humans and a Model Context Protocol (MCP) server for AI agents.

## 🌟 Major Features

### 🤖 Built-in MCP Server
`todo.ai` now includes a native MCP (Model Context Protocol) server, allowing AI coding assistants like Cursor to directly interact with your task list. Agents can now:
-   Read your todo list contextually.
-   Add, complete, and modify tasks without shell commands.
-   Understand your project's priorities instantly.

### 🐍 Python Refactor
The core logic has been completely rewritten in Python, providing:
-   **Installation via pipx:** Easy, isolated system-wide installation (`pipx install todo-ai`).
-   **Robust Parsing:** More reliable handling of `TODO.md` formats and edge cases.
-   **Cross-Platform:** Native support for macOS, Linux, and Windows.

### 🔄 Seamless Compatibility
Despite the rewrite, v3.0 maintains **100% data compatibility** with v2.x:
-   Uses the same `TODO.md` format.
-   Preserves your existing `.todo.ai/` configuration and serial numbers.
-   Respects custom file headers and footers (like Repository links).
-   No migration required—just install and go.

## 🛠️ Infrastructure & Improvements

-   **Dual Interfaces:** CLI and MCP interfaces share the same core logic, ensuring consistent behavior.
-   **Enhanced CLI Output:** CLI output now perfectly matches the familiar Markdown style of the shell script.
-   **Comprehensive Testing:** A full suite of unit, integration, and end-to-end tests ensures reliability.
-   **GitHub Integration:** Verified support for GitHub Issue coordination in numbering modes.

## 📦 Installation

Upgrade to the new Python version:

```bash
pipx install todo-ai
```

This installs:
-   `todo-ai` (CLI)
-   `todo-ai-mcp` (MCP Server)

Legacy shell script users can continue using v2.x, but v3.0 is recommended for all new features.

---
**Full Changelog**: [v2.7.3...v3.0.0](https://github.com/fxstein/todo.ai/compare/v2.7.3...v3.0.0)
