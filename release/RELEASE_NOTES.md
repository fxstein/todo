## Release 3.0.0b2

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

---

### 🐛 Bug Fixes

- Add explicit test dependencies for release job (task#179) ([6525bf7](https://github.com/fxstein/todo.ai/commit/6525bf737344f5c0e1b7ae68cbb003a56e968fe3))
- Use sed for beta version extraction (zsh compatibility) ([2299757](https://github.com/fxstein/todo.ai/commit/229975728782397c8050ea9897aa98fb91100698))
- Prevent version bumps during beta cycles (task#178) ([bb7ff08](https://github.com/fxstein/todo.ai/commit/bb7ff08537c30562b74a468d744b34431e0733e7))

### 🔧 Other Changes

- chore: Auto-commit changes before release ([29e373c](https://github.com/fxstein/todo.ai/commit/29e373c89c496a45853a124651c98d881125f80f))
