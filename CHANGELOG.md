# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Breaking Changes (API Terminology Standardization)

This release standardizes API terminology to follow industry conventions (GitHub, Linear, Jira).

#### MCP Tools
- `add_task(description)` → `add_task(title, description?, tags?)`
- `add_subtask(parent_id, description)` → `add_subtask(parent_id, title, description?, tags?)`
- `modify_task(task_id, description)` → `modify_task(task_id, title, description?, tags?)`
- `add_note`, `update_note`, `delete_note` → replaced by `set_description(task_id, description)` (use `""` to clear)
- New: `set_tags(task_id, tags)` for idempotent tag management (use `[]` to clear)
- Removed: `restart` tool (use `update` with `restart=True`)

#### CLI Commands
- `add` → `add-task`
- `modify` → `modify-task`
- `note`, `update-note`, `delete-note` → `set-description`
- New: `set-tags`

See `docs/api-terminology-analysis.md` for full details.

---

## Release Channels

- **Stable:** Production-ready releases (e.g., `3.0.0`)
- **Beta:** Pre-release testing versions (e.g., `3.0.0b1`, `3.0.0b2`)

### Installing Releases

```bash
# Stable (recommended)
uv tool install todo-ai

# Beta (help us test)
uv tool install --prerelease=allow todo-ai
```

---

## Version Examples

### [3.0.1] - 2025-01-15 (Stable)

Patch release with bug fixes and improvements.

#### Fixed
- Corrected task deletion order in archive command
- Fixed footer placement in TODO.md formatting
- Resolved coordinate auto-increment issues

#### Changed
- Improved error handling in MCP server
- Enhanced logging for debugging

---

### [3.0.0] - 2025-01-10 (Stable)

Major release: Python-based implementation with MCP server support.

#### Added
- Full Python implementation with `uv` package management
- MCP server for AI agent integration (Cursor)
- CLI interface with `todo-ai` command
- 150+ automated tests with comprehensive coverage
- Migration system for upgrading between versions
- GitHub Issues coordination support
- Beta/pre-release release strategy

#### Changed
- **BREAKING:** Requires Python 3.10+
- **BREAKING:** Install via `uv tool install todo-ai` instead of curl
- Improved performance (10x faster for large TODO files)
- Enhanced error messages with clear remediation steps

#### Deprecated
- Legacy shell script (v2.x) - still available but not recommended

---

### [3.0.0b2] - 2025-01-05 (Beta)

Second beta for version 3.0.0 with bug fixes from b1 feedback.

#### Fixed
- Migration command now preserves task relationships correctly
- MCP server connection stability improvements
- Tag preservation in modify command

#### Changed
- Improved pre-flight validation checks
- Enhanced beta maturity warnings

#### Known Issues
- None reported

**How to install:**
```bash
uv tool install --prerelease=allow todo-ai
# or: pipx install --pre todo-ai
```

**Feedback:** Report issues via `todo-ai report-bug` or GitHub Issues

---

### [3.0.0b1] - 2024-12-20 (Beta)

First beta release of Python version - help us test!

#### Added
- Python implementation with full command parity
- MCP server for AI agent integration
- All core commands implemented
- Migration path from shell version

#### Known Issues
- Migration may not preserve all task relationships (fixed in b2)

**How to install:**
```bash
uv tool install --prerelease=allow todo-ai
# or: pipx install --pre todo-ai
```

**Feedback:** Report issues via `todo-ai report-bug` or GitHub Issues

---

## Version Numbering

### Stable Releases

- **Major (X.0.0):** Breaking changes, significant rework
- **Minor (X.Y.0):** New features, backward compatible
- **Patch (X.Y.Z):** Bug fixes, backward compatible

### Beta Releases

- **Format:** `X.Y.ZbN` (e.g., `1.0.0b1`, `1.0.0b2`)
- **Numbering:** Beta number increments for each iteration
- **Duration:** 7+ days for major releases, 2-3 days for minor
- **Required:** All major releases MUST have at least one beta first

## Links

- **GitHub Repository:** https://github.com/fxstein/todo.ai
- **PyPI Package:** https://pypi.org/project/todo-ai/
- **Documentation:** https://github.com/fxstein/todo.ai/tree/main/docs
- **Issue Tracker:** https://github.com/fxstein/todo.ai/issues
- **Discussions:** https://github.com/fxstein/todo.ai/discussions

[Unreleased]: https://github.com/fxstein/todo.ai/compare/v3.0.1...HEAD
[3.0.1]: https://github.com/fxstein/todo.ai/releases/tag/v3.0.1
[3.0.0]: https://github.com/fxstein/todo.ai/releases/tag/v3.0.0
[3.0.0b2]: https://github.com/fxstein/todo.ai/releases/tag/v3.0.0b2
[3.0.0b1]: https://github.com/fxstein/todo.ai/releases/tag/v3.0.0b1
