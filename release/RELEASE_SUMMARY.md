This major release transforms todo.ai from a shell script into a modern Python-based tool with dual interfaces: a command-line tool and an MCP server for AI agent integration. The Python implementation provides 100% feature parity with the shell version while adding significant improvements in performance, reliability, and extensibility.

The new architecture includes a `todo-ai` CLI command that maintains full compatibility with existing workflows, plus a `todo-ai-mcp` server that enables seamless integration with AI agents like Cursor. The tool is now installable via modern package managers (uv, pipx, pip) and includes comprehensive test coverage (150+ automated tests), migration support for shell version users, and improved error handling throughout.

Key improvements include 10x faster performance for large TODO files, comprehensive validation and error messages, automated migration system for upgrades, GitHub Issues coordination support, and cross-platform compatibility (macOS, Linux, Windows WSL2). The implementation uses modern Python tooling with uv for package management, includes pre-commit hooks for code quality, and maintains backward compatibility with existing TODO.md files.

**What's new in Beta 2:** This release includes infrastructure hardening discovered during initial beta testing - improved release automation, enhanced quality gates, and stricter safety checks to ensure stable releases.

This is a beta release to gather feedback on the Python refactor before stable release. The shell script (v2.x) remains available but is now legacy. Install with `uv tool install --prerelease=allow ai-todo` and report any issues via `todo-ai report-bug`.

**Documentation:**
- [Getting Started Guide](https://github.com/fxstein/todo.ai/blob/main/docs/guides/GETTING_STARTED.md) - Quick start and basic usage
- [Python Migration Guide](https://github.com/fxstein/todo.ai/blob/main/docs/user/PYTHON_MIGRATION_GUIDE.md) - Upgrade from v2.x shell version
- [MCP Setup Guide](https://github.com/fxstein/todo.ai/blob/main/docs/user/MCP_SETUP.md) - Configure Cursor AI integration
- [Full Documentation](https://github.com/fxstein/todo.ai/tree/main/docs) - Complete docs index
