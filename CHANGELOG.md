# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Prune Command**: Remove old archived tasks from TODO.md based on retention period or task ID range (GitHub Issue #51, task#267)
  - CLI: `ai-todo prune --days 30` (remove tasks older than 30 days)
  - CLI: `ai-todo prune --from-task 100` (remove tasks #1 to #100)
  - MCP: `prune_tasks(days=30)` tool with same functionality
  - Automatic backup creation in `.ai-todo/archives/` with complete TASK_METADATA
  - Git history analysis to determine accurate archive dates
  - Dry-run mode for safe preview before pruning

## Release Channels

- **Stable:** Production-ready releases (e.g., `4.0.0`)
- **Beta:** Pre-release testing versions (e.g., `4.0.0b1`)

### Installing Releases

```bash
# Stable (recommended)
uv tool install todo-ai

# Beta (help us test)
uv tool install --prerelease=allow todo-ai
```

---

## [4.0.0b1] - 2026-01-27 (Beta)

First beta for version 4.0.0 with breaking API changes and major new features.

### Breaking Changes

This release standardizes API terminology to follow industry conventions (GitHub, Linear, Jira).

#### MCP Tools

- `add_task(description)` → `add_task(title, description?, tags?)`
- `add_subtask(parent_id, description)` → `add_subtask(parent_id, title, description?, tags?)`
- `modify_task(task_id, description)` → `modify_task(task_id, title, description?, tags?)`
- `add_note`, `update_note`, `delete_note` → replaced by `set_description(task_id, description)`
- New: `set_tags(task_id, tags)` for idempotent tag management

#### CLI Commands

- `add` → `add-task`
- `modify` → `modify-task`
- `note`, `update-note`, `delete-note` → `set-description`
- New: `set-tags`

#### Legacy Scripts

- Legacy shell scripts (todo.ai, todo.bash) are now frozen and no longer maintained

### Added

- **MCP Resources**: `tasks://open`, `tasks://active`, `tasks://{id}`, `config://settings` for IDE integration (GitHub Issue #48)
- **Task Metadata Persistence**: Timestamps (`created_at`, `updated_at`) persisted via hidden HTML comments
- **Batch Operations**: `complete`, `delete`, `archive`, `restore` accept multiple task IDs (GitHub Issue #31)
- **.cursorignore Protection**: State files protected from AI agents (GitHub Issue #29)
- **Self-update**: `update` command with version pinning and constraints
- **Restart MCP Tool**: Dev mode quick-reload capability

### Fixed

- TASK_METADATA being incorrectly captured as interleaved content
- Archive/delete task ordering bug (parent before subtasks)
- GitHub task number coordination posting
- Windows CI failure in test_default_path

---

## [3.0.2] - 2026-01-27 (Stable)

Patch release fixing malformed TODO.md files.

### Fixed

- Malformed TODO.md when adding subtasks via MCP on fresh repositories (GitHub Issue #47)
- Footer timestamps properly handled and regenerated cleanly
- Updated branding from "todo.ai" to "ai-todo" in default headers

### Added

- FastMCP 3.x compatibility testing in CI
- Cursor rule documentation for reverse chronological task ordering

---

## [3.0.1] - 2026-01-26 (Stable)

Patch release with bug fixes and improvements.

### Fixed

- Corrected task deletion order in archive command
- Fixed footer placement in TODO.md formatting
- Resolved coordinate auto-increment issues

### Changed

- Improved error handling in MCP server
- Enhanced logging for debugging

---

## [3.0.0] - 2026-01-25 (Stable)

Major release: Python-based implementation with MCP server support.

### Added

- Full Python implementation with `uv` package management
- MCP server for AI agent integration (Cursor)
- CLI interface with `todo-ai` command
- 150+ automated tests with comprehensive coverage
- Migration system for upgrading between versions
- GitHub Issues coordination support
- Beta/pre-release release strategy

### Changed

- **BREAKING:** Requires Python 3.10+
- **BREAKING:** Install via `uv tool install todo-ai` instead of curl
- Improved performance (10x faster for large TODO files)
- Enhanced error messages with clear remediation steps

### Deprecated

- Legacy shell script (v2.x) - still available but not recommended

---

## Version Numbering

### Stable Releases

- **Major (X.0.0):** Breaking changes, significant rework
- **Minor (X.Y.0):** New features, backward compatible
- **Patch (X.Y.Z):** Bug fixes, backward compatible

### Beta Releases

- **Format:** `X.Y.ZbN` (e.g., `4.0.0b1`, `4.0.0b2`)
- **Numbering:** Beta number increments for each iteration
- **Duration:** 7+ days for major releases, 2-3 days for minor
- **Required:** All major releases MUST have at least one beta first

## Links

- **GitHub Repository:** https://github.com/fxstein/ai-todo
- **PyPI Package:** https://pypi.org/project/todo-ai/
- **Documentation:** https://github.com/fxstein/ai-todo/tree/main/docs
- **Issue Tracker:** https://github.com/fxstein/ai-todo/issues
- **Discussions:** https://github.com/fxstein/ai-todo/discussions

[Unreleased]: https://github.com/fxstein/ai-todo/compare/v4.0.0b1...HEAD
[4.0.0b1]: https://github.com/fxstein/ai-todo/releases/tag/v4.0.0b1
[3.0.2]: https://github.com/fxstein/ai-todo/releases/tag/v3.0.2
[3.0.1]: https://github.com/fxstein/ai-todo/releases/tag/v3.0.1
[3.0.0]: https://github.com/fxstein/ai-todo/releases/tag/v3.0.0
