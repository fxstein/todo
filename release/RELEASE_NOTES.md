## Release 3.0.0b15

This release introduces a major architectural unification, combining the CLI and MCP server into a single `todo-ai` executable. The MCP server has been completely rewritten using the modern FastMCP framework, significantly improving maintainability and performance. A new `serve` command (`todo-ai serve`) has been added to launch the MCP server, with support for a `--root` argument to ensure correct project context awareness.

Documentation and Cursor rules have been updated to reflect these changes, guiding AI agents to prefer the MCP interface over CLI commands. The release also includes comprehensive updates to the installation guides and design documentation.

Key changes include:
- Unification of CLI and MCP server into `todo-ai`
- FastMCP integration for the MCP server
- New `serve` command with `--root` support
- Updated Cursor rules and documentation
- Various bug fixes and linting improvements
- Removed obsolete integration tests to resolve CI failures

---
