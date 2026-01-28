# Release 4.0.0b2

This release addresses a critical bug (GitHub Issue #49) where archived tasks with incomplete subtasks would incorrectly reappear in the Tasks section when adding new tasks. The fix changes how task status is determined during parsing: section membership now takes precedence over checkbox state, ensuring that all tasks in "Recently Completed" or "Archived Tasks" sections are properly treated as archived regardless of their checkbox character.

Additionally, this release fixes the `config://settings` MCP resource to correctly report `coordination.enabled` status. Previously it was checking for a non-existent configuration key, causing it to always return `false`. The resource now properly derives the enabled state from the configured coordination type.

Both fixes include regression tests to prevent these issues from recurring. Users who experienced archived tasks unexpectedly appearing in their active task list should update to this version immediately.

---

## ✨ Features

- Add task#264 for GitHub Issue #49 - archived tasks reappearing bug ([bbc4468](https://github.com/fxstein/ai-todo/commit/bbc4468c2c3525056ed52e1ff976865340b9b0e6))

## 🐛 Bug Fixes

- Prevent orphan subtasks from leaking into Tasks section (task#264) ([2508033](https://github.com/fxstein/ai-todo/commit/25080333c4421afa2d49afcd52337ba052a62d8b))
- Derive coordination.enabled from type instead of non-existent key ([491842d](https://github.com/fxstein/ai-todo/commit/491842d0a5346704801bc25cbee75d7ac4406372))

## 🔧 Other Changes

- chore: Update release log for v4.0.0b2 ([0885f41](https://github.com/fxstein/ai-todo/commit/0885f41258cc3f89681f2a4b61978ca3c867cb12))
- docs: Prepare release notes for v4.0.0b2 ([5adbd23](https://github.com/fxstein/ai-todo/commit/5adbd23fbbcb9f79c53b25ca635cde185b8357e4))
- docs: Add AI release summary for v4.0.0b2 ([ceeea5c](https://github.com/fxstein/ai-todo/commit/ceeea5c40f0962d24c3f05a3191b792ac59ca69d))
- internal: Archive completed task#264 (GitHub Issue #49 fix) ([be5c9b8](https://github.com/fxstein/ai-todo/commit/be5c9b8e1dc02e7d47d5bf0d7d7ae39f539f8b0b))
- docs: Update CHANGELOG.md for v4.0.0b1 release ([401ed5b](https://github.com/fxstein/ai-todo/commit/401ed5bc5bcaa875eee70cae878f7d164e1c76d1))

## Previous Beta Release Notes

### Release 4.0.0b1

### Breaking Changes

This release includes **API terminology standardization** (task#253) that aligns ai-todo with industry conventions. The MCP tools and CLI commands have been updated:

- `add_task(description)` → `add_task(title, description?, tags?)`
- `add_subtask(parent_id, description)` → `add_subtask(parent_id, title, description?, tags?)`
- `modify_task(task_id, description)` → `modify_task(task_id, title, description?, tags?)`
- `add_note`, `update_note`, `delete_note` → `set_description(task_id, description)`
- New: `set_tags(task_id, tags)` for dedicated tag management

Legacy shell scripts have been frozen with a FROZEN header for backward compatibility but are no longer actively maintained.

### New Features

**MCP Resources** (task#262, GitHub Issue #48): AI agents can now access task data via MCP resources - `tasks://open` for pending tasks, `tasks://active` for in-progress work, `tasks://{id}` for individual task details, and `config://settings` for configuration. This enables IDE integrations to display real-time task status without explicit tool calls.

**Task Metadata Persistence** (task#263): Task timestamps (`created_at`, `updated_at`) are now persisted across sessions via hidden HTML comments in TODO.md. Timestamps are lazily backfilled when tasks are modified, ensuring accurate tracking without migration scripts. Completion dates continue to appear inline for human readability.

**Batch Operations** (task#261, GitHub Issue #31): The `complete`, `delete`, `archive`, and `restore` commands now accept multiple task IDs in a single call, reducing round-trips when managing multiple tasks. Both MCP tools and CLI support this batch interface.

### Security & Reliability

**.cursorignore Protection** (task#260, GitHub Issue #29): Added `.cursorignore` patterns to prevent AI agents from directly accessing tamper detection state files. Security best practices documentation added at `docs/guides/SECURITY_BEST_PRACTICES.md`.

**Bug Fixes**: Fixed TASK_METADATA being incorrectly captured as interleaved content, causing subtask display issues. Resolved archive/delete task ordering bug where parent tasks were processed before subtasks (task#242). Restored GitHub task number coordination posting (task#247).

---

### 🔴 Breaking Changes

- feat!: Implement API terminology standardization (task#253) ([338d0eb](https://github.com/fxstein/ai-todo/commit/338d0eb58dc700ffb0f24e8b8c2e945298a54f41))

### ✨ Features

- Implement task metadata persistence for timestamps (task#263) ([b9500b8](https://github.com/fxstein/ai-todo/commit/b9500b82851fb581fc6fc34b32d572190cc8cf66))
- Add MCP resources for task data and begin metadata design (task#262, task#263) ([b07b27c](https://github.com/fxstein/ai-todo/commit/b07b27c535faff1902b56e53395eac506d34b224))
- Implement .cursorignore security for ai-todo state files (task#260) ([d8552d3](https://github.com/fxstein/ai-todo/commit/d8552d346d4d8b5cdbaad3eea3f3a0d5dea38c2a))
- Implement batch operations for task state commands (task#261) ([1e1b0e2](https://github.com/fxstein/ai-todo/commit/1e1b0e2a250207377978473a2810dd7924bc6d1e))
- Add tasks for API terminology standardization and legacy freeze (task#253, task#254) ([3aa79c7](https://github.com/fxstein/ai-todo/commit/3aa79c7e07ed6453a68eca81926664aa1a9080bd))
- Add restart MCP tool for dev mode quick-reload (task#250) ([7957cbd](https://github.com/fxstein/ai-todo/commit/7957cbd5b29e7fcea43abacf1b1b1c02f64f536d))
- Add version pinning and constraints to self-update feature (task#245) ([c118e2d](https://github.com/fxstein/ai-todo/commit/c118e2d786959ba1bf526ff0f074c3fe7f7f3f86))
- Implement self-update feature with MCP and CLI support (task#241) ([4b59823](https://github.com/fxstein/ai-todo/commit/4b59823545d5b09e541a466f73ac93058650db85))
- Add task #242 to investigate `archive/delete` task ordering bug ([4f50342](https://github.com/fxstein/ai-todo/commit/4f50342a78fdd6b5755e79d67354886a887c12a6))
- Add task #241 for self-update feature via uv with MCP server shutdown ([090cd53](https://github.com/fxstein/ai-todo/commit/090cd5341f674d79677f798c8552989af76a66b8))

### 🐛 Bug Fixes

- Prevent TASK_METADATA from being captured as interleaved content ([d075259](https://github.com/fxstein/ai-todo/commit/d075259e0dd460f6e82bb4fd2b6dd1a1317d1196))
- Windows CI failure in test_default_path ([6b16b01](https://github.com/fxstein/ai-todo/commit/6b16b01d26a8949c1ddeb5db5d1d5fff588df28c))
- Restore GitHub task number coordination posting (task#247) ([78314b0](https://github.com/fxstein/ai-todo/commit/78314b0dc01a96787b89a6b28f84db6be7a43168))
- Resolve `archive/delete` task ordering bug - parent before subtasks (task#242) ([e7e4a82](https://github.com/fxstein/ai-todo/commit/e7e4a82369d147dafb4097dbbe31489e8dc3d9db))
- Update version comment to 3.0.2 in shell scripts ([d449997](https://github.com/fxstein/ai-todo/commit/d4499979300504222a896a3a8da412980c367826))

### 🔧 Other Changes

- docs: Add AI release summary for v4.0.0 ([6d34739](https://github.com/fxstein/ai-todo/commit/6d34739f787e6cc81d9a2b1dc4ecfd736ea3a0bf))
- chore: Archive task#262, task#263 (MCP resources and metadata persistence) ([4986bc0](https://github.com/fxstein/ai-todo/commit/4986bc06d3091b9b3d234ecac276b2bd6b50fc86))
- chore: Archive task#260, task#261 and clean up task#51 subtasks ([287c6b0](https://github.com/fxstein/ai-todo/commit/287c6b08cba49a7d67fb33dd3f97abd73f2e37d8))
- chore: Freeze legacy shell scripts and remove parity tests (task#254) ([ec714af](https://github.com/fxstein/ai-todo/commit/ec714af24ca1d7597a11d9e79850c36b2a20748c))
- chore: Archive completed tasks #239, #240, #241, #242, #245, #246 ([df65839](https://github.com/fxstein/ai-todo/commit/df6583949034ade6db7c729ecea778546a35bf68))
- test: Add unit test for archived task reordering (task#246) ([f63b013](https://github.com/fxstein/ai-todo/commit/f63b013263fa1c6bbe8dd52f69c81ab85a8d4782))

### Previous Release Notes

### Release 3.0.2

This release fixes a critical bug where TODO.md files became malformed when adding multiple subtasks via MCP on fresh repositories. The issue caused orphaned timestamp lines to accumulate in the file, breaking the expected format. The fix ensures footer timestamps are properly handled and always regenerated cleanly, while also updating the branding from legacy "todo.ai" to "ai-todo" in default headers.

The cursor rule generator that installs rules in new projects now documents that tasks are displayed in reverse chronological order (newest on top), helping prevent confusion about the intentional task ordering behavior.

---

### 🐛 Bug Fixes

- Resolve malformed TODO.md on fresh repos with multiple subtasks (task#240) ([cddfb9d](https://github.com/fxstein/ai-todo/commit/cddfb9df563d9830a4e702d3d916b831e55f04b9))

### 🔧 Infrastructure

- Add fastmcp 3.x compatibility testing in CI (task#239) ([661253b](https://github.com/fxstein/ai-todo/commit/661253b89d6ca9376204a95ec51e61d06e777e16))
