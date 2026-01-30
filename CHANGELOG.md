# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0](https://github.com/fxstein/ai-todo/compare/v4.0.0...v4.0.0) (2026-01-30)


### ✨ Features

* Add automated release workflow rule with Linear tracking ([bc37eb1](https://github.com/fxstein/ai-todo/commit/bc37eb114a08c9e4d5687dd8edaf704703cc80ec))
* Add commit guideline to ai-todo Cursor rule (task[#265](https://github.com/fxstein/ai-todo/issues/265)) ([6867af4](https://github.com/fxstein/ai-todo/commit/6867af46d15b2085d46b5dbff3f0f4ecb91f10ac))
* Add Linear–ai-todo integration Cursor rule ([d69d409](https://github.com/fxstein/ai-todo/commit/d69d4093ff5d7eae044a264012988b5a1a23adc1))
* Add Release Please configuration (task[#269](https://github.com/fxstein/ai-todo/issues/269).3, Phase 1) ([f2404c6](https://github.com/fxstein/ai-todo/commit/f2404c610c6ef01f4333a712279b8d5baef7ae71))
* Add Release Please Phase 1 (task[#269](https://github.com/fxstein/ai-todo/issues/269).3) ([6b22cd1](https://github.com/fxstein/ai-todo/commit/6b22cd11a9b04d077e91215fbe937411228fd2df))
* Enable beta prerelease mode for 4.0.0 cycle (task[#269](https://github.com/fxstein/ai-todo/issues/269).3) ([25628d4](https://github.com/fxstein/ai-todo/commit/25628d4774e3f96a6b11a0220b1d1087bb3890de))
* Enable beta release workflow (task[#269](https://github.com/fxstein/ai-todo/issues/269).3) ([f5312ec](https://github.com/fxstein/ai-todo/commit/f5312ecad09da89e3f3fb7b51f25c4705d8055ad))
* Enhance linear-release-workflow rule with feedback loop ([aa87f80](https://github.com/fxstein/ai-todo/commit/aa87f80b86f8a31a2506fc253ce5506d5bc41c21))
* Implement core prune functionality (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([7195206](https://github.com/fxstein/ai-todo/commit/7195206143ab5d05c223785239bd250428f7d59b))
* Implement empty trash functionality (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([dae88da](https://github.com/fxstein/ai-todo/commit/dae88dae43020f45d0a451ae2c0518d134738e76))
* Linear integration implementation and review fixes (task[#266](https://github.com/fxstein/ai-todo/issues/266)) ([aa6d373](https://github.com/fxstein/ai-todo/commit/aa6d37399ec07d1609a861d506337b6e6a2759f4))


### 🐛 Bug Fixes

* Change extra-files type from python to generic (task[#269](https://github.com/fxstein/ai-todo/issues/269).3) ([ad7df4c](https://github.com/fxstein/ai-todo/commit/ad7df4c746a77e33aebf46891fa93d221e8d5b23))
* Correct backup header to reflect actual prune criteria (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([ede65b3](https://github.com/fxstein/ai-todo/commit/ede65b3b53b9059f8d4d05a0b33e5dc29130797a))
* Correct Release Please extra-files config (task[#269](https://github.com/fxstein/ai-todo/issues/269).3) ([6d1cf13](https://github.com/fxstein/ai-todo/commit/6d1cf139bf4a8ef8d5f1f941ee116f135d53ccf7))
* Correct username logic for Linear integration (task[#266](https://github.com/fxstein/ai-todo/issues/266)) ([bb10c31](https://github.com/fxstein/ai-todo/commit/bb10c31d9f0d070b693b4587271a75807115b9ec))
* Disable prerelease config to use Release-As for beta versions ([5d8f82e](https://github.com/fxstein/ai-todo/commit/5d8f82eed05175087c9222bba299411d4e202629))
* Escape regex metacharacters in task IDs for git grep (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([58d9b25](https://github.com/fxstein/ai-todo/commit/58d9b25a6b8269de09fed74d464ee78c5441eecf))
* Exclude .ai-todo directory from CI markdown linting (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([2b1bc6e](https://github.com/fxstein/ai-todo/commit/2b1bc6e0aacc6c589599070ef41b13a7b7191d32))
* Handle timezone comparison in prune date filtering (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([50176d6](https://github.com/fxstein/ai-todo/commit/50176d69b04e58821d55702d139451d1d6a682d6))
* Include TASK_METADATA in prune backup archives (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([3183eee](https://github.com/fxstein/ai-todo/commit/3183eee22171f73e96c194c5bec261d8bae31d8a))
* Make days parameter optional to respect filter precedence (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([e099fec](https://github.com/fxstein/ai-todo/commit/e099fec558566f3ec8f87f8b88684727be12cbc5))
* Prevent duplicate subtasks in task range pruning (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([63f91a4](https://github.com/fxstein/ai-todo/commit/63f91a4208186ad381e4725650ec16115fae668a))
* Use numeric sorting for task IDs in archive backups (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([0e5e2ce](https://github.com/fxstein/ai-todo/commit/0e5e2ce96f8f6620987a66ee3d26f9dfc888ed53))
* Use OR logic for git grep patterns in archive date detection (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([d2acfc9](https://github.com/fxstein/ai-todo/commit/d2acfc989d6543b4263cefc1df4ad9347a30bc34))
* Use timezone-aware datetimes for prune age comparisons (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([20a42ed](https://github.com/fxstein/ai-todo/commit/20a42edb8d0596c9e3128716bf7a0796d8262c92))


### ♻️ Refactoring

* Always construct branch names, never use Linear's gitBranchName ([2cf15f6](https://github.com/fxstein/ai-todo/commit/2cf15f626c1a5727c4167585aeec2e4a19eb025e))
* Enhance closing workflow with PR creation and cleanup steps ([4bcbe71](https://github.com/fxstein/ai-todo/commit/4bcbe717bf599dd885de1078eeecc493d5d634c6))
* Remove fragile string parsing in archive backup footer (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([f8dad72](https://github.com/fxstein/ai-todo/commit/f8dad729a8f7b85a8c8537b9ff6eb831d56f25a4))
* Remove redundant step in branch construction ([6c68888](https://github.com/fxstein/ai-todo/commit/6c68888818da30b042ef2a120e4b716536006680))
* Rename release-automation.mdc to linear-release-workflow.mdc ([b37b147](https://github.com/fxstein/ai-todo/commit/b37b14749c6e3cd9e3ed27039a118ec94bc89715))
* Simplify branch naming in Linear integration rule ([22db187](https://github.com/fxstein/ai-todo/commit/22db18753d83e96d9dbb2509f28ee7c02f273af7))
* Standardize branch naming to always use userid prefix ([7685d2e](https://github.com/fxstein/ai-todo/commit/7685d2ed5a83485f20868b7c5c88cb5aaed4ebf4))


### 📚 Documentation

* Add auto empty trash after delete command (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([b7aa75d](https://github.com/fxstein/ai-todo/commit/b7aa75d6642b5d4b846015036235c6cab8a1a4bf))
* Add empty trash analysis document (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([ac9287e](https://github.com/fxstein/ai-todo/commit/ac9287e12369ff153b306a58d0e8bc4900b30369))
* Add empty trash design document (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([8d61043](https://github.com/fxstein/ai-todo/commit/8d61043041c06c3955791c85e44d3e112e364810))
* Add empty trash documentation (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([48ef24c](https://github.com/fxstein/ai-todo/commit/48ef24c35f95f92faf21969be26c2b649ecaf791))
* Add Issue Investigation workflow to linear-document-workflow rule ([6aec0c0](https://github.com/fxstein/ai-todo/commit/6aec0c08fc90e14127d376ab39d4c2ff583bf660))
* add Linear document & task workflow rule (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([f2cc740](https://github.com/fxstein/ai-todo/commit/f2cc740435c7e16d9fc1884442c1cf13f7f34dc2))
* Add Linear integration assessment (task[#266](https://github.com/fxstein/ai-todo/issues/266)) ([f39bdac](https://github.com/fxstein/ai-todo/commit/f39bdac74a4e1fba87077e49267372c0d2173063))
* Add Phase 1 completion summary (task[#269](https://github.com/fxstein/ai-todo/issues/269).3) ([027dcba](https://github.com/fxstein/ai-todo/commit/027dcbabb8288fdf1457f42193166b48641dff67))
* Add prune command documentation and examples (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([5573f31](https://github.com/fxstein/ai-todo/commit/5573f31c8d579c400d445a1a75cb9012146d24c3))
* Add prune function analysis and design documents (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([bcc513a](https://github.com/fxstein/ai-todo/commit/bcc513a0d243050ccd9840f56502236fe340732a))
* Address design feedback from Linear (task[#269](https://github.com/fxstein/ai-todo/issues/269).2) ([b7c921a](https://github.com/fxstein/ai-todo/commit/b7c921a6d7ecc14570e38252b209053434311081))
* Complete Release Please analysis (task[#269](https://github.com/fxstein/ai-todo/issues/269).1) ([6e55843](https://github.com/fxstein/ai-todo/commit/6e55843e2aae454307288c1263fee45adb7eb8c5))
* Complete Release Please design document (task[#269](https://github.com/fxstein/ai-todo/issues/269).2) ([5813ec3](https://github.com/fxstein/ai-todo/commit/5813ec36b8914d1f6f265dcfbf095b32d671b6e6))
* Linear integration design and assessment (task[#266](https://github.com/fxstein/ai-todo/issues/266)) ([7b40cb1](https://github.com/fxstein/ai-todo/commit/7b40cb1eedba6737da7c315bae5a45b71a145446))
* Mark 265.1 complete and fix Linear rule tool names (task[#265](https://github.com/fxstein/ai-todo/issues/265)) ([f461b07](https://github.com/fxstein/ai-todo/commit/f461b07c4c3cadce913e21e667e363f88c906395))
* Remove all backup functionality from empty trash design (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([e128694](https://github.com/fxstein/ai-todo/commit/e128694b2960c3ffc21ce9d09565d7186036ca10))
* Remove legacy bash code from analysis document (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([cce3764](https://github.com/fxstein/ai-todo/commit/cce376417cf4e53cd2af49e1a234249c7dbbf632))
* Remove Pionizer references from OSS project ([f514206](https://github.com/fxstein/ai-todo/commit/f5142066269bd8b48fc3782816bbe2ad1ff7352c))
* Resolve open questions in analysis document (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([3d7b1c3](https://github.com/fxstein/ai-todo/commit/3d7b1c3c28b94ee77901a78a7d617554dab8e9e8))
* Specify PR body format in Linear integration rule ([e815419](https://github.com/fxstein/ai-todo/commit/e8154191ff410e98ae82dfc7d9e38dc8ec2311c2))
* Update design with approved decisions (task[#269](https://github.com/fxstein/ai-todo/issues/269).2) ([3ec0467](https://github.com/fxstein/ai-todo/commit/3ec046734e8e07ca261d3fafe411b618ba96db4e))
* Update empty trash analysis - change retention from 7 to 30 days (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([6f61ddb](https://github.com/fxstein/ai-todo/commit/6f61ddb543e70fdb60f46310fdabac7f57ee57ca))
* Update task[#268](https://github.com/fxstein/ai-todo/issues/268) description with 30-day retention change ([b7677c7](https://github.com/fxstein/ai-todo/commit/b7677c7723dbe55617f49acd7b3c97d9799c351e))


### 🔧 Maintenance

* Archive task[#268](https://github.com/fxstein/ai-todo/issues/268) - Empty Trash implementation complete ([c10f6ca](https://github.com/fxstein/ai-todo/commit/c10f6caf8956f58184a96b644d813109a94fd5a2))
* Complete task[#268](https://github.com/fxstein/ai-todo/issues/268) and all subtasks ([48b97a5](https://github.com/fxstein/ai-todo/commit/48b97a552dbdcb4d043a7f17a187f3e2859c5115))
* release 4.0.0b3 ([da32853](https://github.com/fxstein/ai-todo/commit/da328534917f401c83e7ee0700e9f9469ac528f3))
* release 4.0.0b3 ([33a92eb](https://github.com/fxstein/ai-todo/commit/33a92eb0418e2caad5ef64ac503c523f25aa24b3))


### 🧪 Tests

* Add comprehensive prune integration tests (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([09a6b08](https://github.com/fxstein/ai-todo/commit/09a6b0808570a98a7bff64591ab1bd8423ce2584))
* Add comprehensive tests for empty trash (task[#268](https://github.com/fxstein/ai-todo/issues/268)) ([2909ed5](https://github.com/fxstein/ai-todo/commit/2909ed5e29d153189c95aaaff6c3adb2ada9cb91))
* Add comprehensive unit tests for prune functionality (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([300b002](https://github.com/fxstein/ai-todo/commit/300b0022c41a899821c643578192af49ef2e209e))
* Execute prune operations and add TASK_METADATA to backups (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([990fce8](https://github.com/fxstein/ai-todo/commit/990fce8ce1b6f961e4d8118f33b0d904d465f5ff))
* Verify TASK_METADATA preservation in prune backups (task[#267](https://github.com/fxstein/ai-todo/issues/267)) ([9df4d05](https://github.com/fxstein/ai-todo/commit/9df4d05c1c34f979fda8da30b580cc575767ac8e))

## [Unreleased]

### Added

- **Empty Trash Command**: Permanently remove expired deleted tasks with 30-day retention (GitHub Issue #52, Linear AIT-3, task#268)
  - CLI: `ai-todo empty-trash` (remove deleted tasks older than 30 days)
  - CLI: `ai-todo empty-trash --dry-run` (preview what would be removed)
  - MCP: `empty_trash(dry_run=False)` tool with same functionality
  - Auto-run on MCP server startup (silent, keeps Deleted Tasks section clean)
  - Auto-run after `ai-todo delete` command (silent, immediate cleanup)
  - Uses existing `expires_at` field for simple date comparison
  - No backup functionality (permanent deletion, true "Empty Trash" semantics)
  - Dry-run mode for safe preview before removal

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
