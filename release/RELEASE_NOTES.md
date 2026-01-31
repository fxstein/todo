# Release 4.0.0b3

This release introduces two powerful new commands for managing task lifecycle: prune and empty-trash. The prune command (task#267) allows users to permanently remove archived tasks from TODO.md with fine-grained control over retention periods using `--days`, or by targeting specific task ranges with `--from-task` and `--to-task` options. All pruned tasks are automatically backed up to timestamped archive files in the `.ai-todo/archives/` directory, preserving full task metadata and enabling recovery if needed. Comprehensive documentation and examples are available in [docs/examples/PRUNE_EXAMPLES.md](https://github.com/fxstein/ai-todo/blob/main/docs/examples/PRUNE_EXAMPLES.md).

The empty-trash command (task#268) complements the prune functionality by automatically removing deleted tasks that are older than 30 days on startup, helping keep your TODO.md clean without manual intervention. This automatic cleanup runs quietly in the background and includes comprehensive test coverage to ensure data safety. Users can also manually trigger empty-trash operations when needed.

Several critical bug fixes improve system reliability across different Python versions and edge cases. Python 3.10 compatibility has been restored by replacing `datetime.UTC` with `timezone.utc` throughout the codebase. Timezone-aware datetime comparisons in prune operations now work correctly across different system configurations. Regex metacharacter escaping for task IDs prevents errors when working with tasks that contain special characters, and duplicate prevention in subtask operations ensures data integrity during complex task manipulations.

---

## ✨ Features

- Filter chore commits from release notes (task#270) ([08a0861](https://github.com/fxstein/ai-todo/commit/08a086172dedc37418133e6777df9c939391a367))
- Commit AI summary before prepare & add release notes link (task#270) ([297b720](https://github.com/fxstein/ai-todo/commit/297b720e639f7467c11fa4c32840b869b691aa24))
- Add Linear issue tracking to release workflow (task#270) ([9661d3a](https://github.com/fxstein/ai-todo/commit/9661d3a84e7f0c61ce54f118f31fb6711cafe3d8))
- Add pre-flight checks to release workflow (task#270) ([5ebb21c](https://github.com/fxstein/ai-todo/commit/5ebb21c450903fb366e784673af91df1ddf59824))
- Add pre-validation of generated files (task#270) ([644e427](https://github.com/fxstein/ai-todo/commit/644e427c013537d14ea5c2b00d4a88015a2a3e46))
- Refactor release workflow to Cursor Skill (task#270) ([d828f5e](https://github.com/fxstein/ai-todo/commit/d828f5ef4e4b19bfee61a8b5bb4a3d19c6daa2b3))
- Add PEP 440 versioning strategy to release-please config ([c818c22](https://github.com/fxstein/ai-todo/commit/c818c224aa464dcfbbe45ba9af692204e6cd03ed))
- Enable beta prerelease mode for 4.0.0 cycle (task#269.3) ([25628d4](https://github.com/fxstein/ai-todo/commit/25628d4774e3f96a6b11a0220b1d1087bb3890de))
- Enable beta release workflow (task#269.3) ([f5312ec](https://github.com/fxstein/ai-todo/commit/f5312ecad09da89e3f3fb7b51f25c4705d8055ad))
- Add Release Please configuration (task#269.3, Phase 1) ([f2404c6](https://github.com/fxstein/ai-todo/commit/f2404c610c6ef01f4333a712279b8d5baef7ae71))
- Enhance linear-release-workflow rule with feedback loop ([aa87f80](https://github.com/fxstein/ai-todo/commit/aa87f80b86f8a31a2506fc253ce5506d5bc41c21))
- Add automated release workflow rule with Linear tracking ([bc37eb1](https://github.com/fxstein/ai-todo/commit/bc37eb114a08c9e4d5687dd8edaf704703cc80ec))
- Implement empty trash functionality (task#268) ([dae88da](https://github.com/fxstein/ai-todo/commit/dae88dae43020f45d0a451ae2c0518d134738e76))
- Implement core prune functionality (task#267) ([7195206](https://github.com/fxstein/ai-todo/commit/7195206143ab5d05c223785239bd250428f7d59b))
- Linear integration implementation and review fixes (task#266) ([aa6d373](https://github.com/fxstein/ai-todo/commit/aa6d37399ec07d1609a861d506337b6e6a2759f4))
- Add commit guideline to ai-todo Cursor rule (task#265) ([6867af4](https://github.com/fxstein/ai-todo/commit/6867af46d15b2085d46b5dbff3f0f4ecb91f10ac))
- Add Linear–ai-todo integration Cursor rule ([d69d409](https://github.com/fxstein/ai-todo/commit/d69d4093ff5d7eae044a264012988b5a1a23adc1))

## 🐛 Bug Fixes

- Use checksums to detect pre-commit auto-fixes (task#270) ([5534602](https://github.com/fxstein/ai-todo/commit/553460271b48d15d69e57ca720b84ac0b5c69532))
- Set Linear issue to Todo on release abort (task#270) ([7746135](https://github.com/fxstein/ai-todo/commit/774613528371b9da4ec3aedea7f33178728adf6c))
- Commit and push release log after abort (task#270) ([ae9fb0a](https://github.com/fxstein/ai-todo/commit/ae9fb0a4ea9d39a0d789554b0773f22c6f5749ec))
- Remove orphaned todo.bash references (task#270) ([92db8c8](https://github.com/fxstein/ai-todo/commit/92db8c8cba68908bc6b314d24d8cecc12961bb67))
- Address skill testing feedback (task#270) ([02ba6c7](https://github.com/fxstein/ai-todo/commit/02ba6c73101a568959958feab3a7f812ffadd8b6))
- Use PEP 440 format in release-please manifest ([03ed8f4](https://github.com/fxstein/ai-todo/commit/03ed8f4e2d0f7922d4addce592f659b38b185369))
- Replace UTC with timezone.utc in source files for Python 3.10 ([b2b02f9](https://github.com/fxstein/ai-todo/commit/b2b02f95ca997d652b5b054935a1b09cd124d0fc))
- Replace datetime.UTC with timezone.utc for Python 3.10 compatibility ([04465f4](https://github.com/fxstein/ai-todo/commit/04465f46bb2e1ef6e0a31ec0ef67b22a424f9b9c))
- Disable prerelease config to use Release-As for beta versions ([5d8f82e](https://github.com/fxstein/ai-todo/commit/5d8f82eed05175087c9222bba299411d4e202629))
- Change extra-files type from python to generic (task#269.3) ([ad7df4c](https://github.com/fxstein/ai-todo/commit/ad7df4c746a77e33aebf46891fa93d221e8d5b23))
- Exclude .ai-todo directory from CI markdown linting (task#268) ([2b1bc6e](https://github.com/fxstein/ai-todo/commit/2b1bc6e0aacc6c589599070ef41b13a7b7191d32))
- Use numeric sorting for task IDs in archive backups (task#267) ([0e5e2ce](https://github.com/fxstein/ai-todo/commit/0e5e2ce96f8f6620987a66ee3d26f9dfc888ed53))
- Prevent duplicate subtasks in task range pruning (task#267) ([63f91a4](https://github.com/fxstein/ai-todo/commit/63f91a4208186ad381e4725650ec16115fae668a))
- Use timezone-aware datetimes for prune age comparisons (task#267) ([20a42ed](https://github.com/fxstein/ai-todo/commit/20a42edb8d0596c9e3128716bf7a0796d8262c92))
- Make days parameter optional to respect filter precedence (task#267) ([e099fec](https://github.com/fxstein/ai-todo/commit/e099fec558566f3ec8f87f8b88684727be12cbc5))
- Escape regex metacharacters in task IDs for git grep (task#267) ([58d9b25](https://github.com/fxstein/ai-todo/commit/58d9b25a6b8269de09fed74d464ee78c5441eecf))
- Use OR logic for git grep patterns in archive date detection (task#267) ([d2acfc9](https://github.com/fxstein/ai-todo/commit/d2acfc989d6543b4263cefc1df4ad9347a30bc34))
- Correct backup header to reflect actual prune criteria (task#267) ([ede65b3](https://github.com/fxstein/ai-todo/commit/ede65b3b53b9059f8d4d05a0b33e5dc29130797a))
- Include TASK_METADATA in prune backup archives (task#267) ([3183eee](https://github.com/fxstein/ai-todo/commit/3183eee22171f73e96c194c5bec261d8bae31d8a))
- Handle timezone comparison in prune date filtering (task#267) ([50176d6](https://github.com/fxstein/ai-todo/commit/50176d69b04e58821d55702d139451d1d6a682d6))
- Correct username logic for Linear integration (task#266) ([bb10c31](https://github.com/fxstein/ai-todo/commit/bb10c31d9f0d070b693b4587271a75807115b9ec))

## 🔧 Other Changes

- Update release log for 4.0.0b3 abort ([c4d79f0](https://github.com/fxstein/ai-todo/commit/c4d79f046a44fca1d4375d80fbf616aae855f450))
- Update release log for 4.0.0b3 abort ([f5d3faa](https://github.com/fxstein/ai-todo/commit/f5d3faa0b110375d8f7c61f4948e5e19a46d8449))
- docs: Add release summary for v4.0.0b3 (task#270) ([4e06225](https://github.com/fxstein/ai-todo/commit/4e06225b53284f171933a1031de4278a1452e240))
- docs: Align summary paragraph count with prompt template (task#270) ([0b5f54b](https://github.com/fxstein/ai-todo/commit/0b5f54b4e735be5ecad8633858fd08c0a2d25294))
- docs: Add release summary prompt template to skill (task#270) ([5c2a79d](https://github.com/fxstein/ai-todo/commit/5c2a79d31c18e30e32d28dfc94a3672a318bfdcd))
- docs: Add release summary for 4.0.0b3 ([94c98cb](https://github.com/fxstein/ai-todo/commit/94c98cbb3acdf46d755d9f7444edfec0402e9f9f))
- docs: Add release summary for 4.0.0b3 ([68d7616](https://github.com/fxstein/ai-todo/commit/68d76163e95e32d3a8983150af91990072970141))
- Revert "feat: Enable beta release workflow (task#269.3)" ([65b922f](https://github.com/fxstein/ai-todo/commit/65b922f8372e2a520aafa3ae72f4d3624c181280))
- docs: Add Phase 1 completion summary (task#269.3) ([027dcba](https://github.com/fxstein/ai-todo/commit/027dcbabb8288fdf1457f42193166b48641dff67))
- docs: Update design with approved decisions (task#269.2) ([3ec0467](https://github.com/fxstein/ai-todo/commit/3ec046734e8e07ca261d3fafe411b618ba96db4e))
- docs: Address design feedback from Linear (task#269.2) ([b7c921a](https://github.com/fxstein/ai-todo/commit/b7c921a6d7ecc14570e38252b209053434311081))
- docs: Complete Release Please design document (task#269.2) ([5813ec3](https://github.com/fxstein/ai-todo/commit/5813ec36b8914d1f6f265dcfbf095b32d671b6e6))
- docs: Complete Release Please analysis (task#269.1) ([6e55843](https://github.com/fxstein/ai-todo/commit/6e55843e2aae454307288c1263fee45adb7eb8c5))
- refactor: Rename release-automation.mdc to linear-release-workflow.mdc ([b37b147](https://github.com/fxstein/ai-todo/commit/b37b14749c6e3cd9e3ed27039a118ec94bc89715))
- docs: Remove Pionizer references from OSS project ([f514206](https://github.com/fxstein/ai-todo/commit/f5142066269bd8b48fc3782816bbe2ad1ff7352c))
- docs: Add empty trash documentation (task#268) ([48ef24c](https://github.com/fxstein/ai-todo/commit/48ef24c35f95f92faf21969be26c2b649ecaf791))
- test: Add comprehensive tests for empty trash (task#268) ([2909ed5](https://github.com/fxstein/ai-todo/commit/2909ed5e29d153189c95aaaff6c3adb2ada9cb91))
- docs: Add auto empty trash after delete command (task#268) ([b7aa75d](https://github.com/fxstein/ai-todo/commit/b7aa75d6642b5d4b846015036235c6cab8a1a4bf))
- docs: Remove all backup functionality from empty trash design (task#268) ([e128694](https://github.com/fxstein/ai-todo/commit/e128694b2960c3ffc21ce9d09565d7186036ca10))
- docs: Add empty trash design document (task#268) ([8d61043](https://github.com/fxstein/ai-todo/commit/8d61043041c06c3955791c85e44d3e112e364810))
- docs: Resolve open questions in analysis document (task#268) ([3d7b1c3](https://github.com/fxstein/ai-todo/commit/3d7b1c3c28b94ee77901a78a7d617554dab8e9e8))
- docs: Remove legacy bash code from analysis document (task#268) ([cce3764](https://github.com/fxstein/ai-todo/commit/cce376417cf4e53cd2af49e1a234249c7dbbf632))
- docs: Update task#268 description with 30-day retention change ([b7677c7](https://github.com/fxstein/ai-todo/commit/b7677c7723dbe55617f49acd7b3c97d9799c351e))
- docs: Update empty trash analysis - change retention from 7 to 30 days (task#268) ([6f61ddb](https://github.com/fxstein/ai-todo/commit/6f61ddb543e70fdb60f46310fdabac7f57ee57ca))
- docs: Add empty trash analysis document (task#268) ([ac9287e](https://github.com/fxstein/ai-todo/commit/ac9287e12369ff153b306a58d0e8bc4900b30369))
- refactor: Remove redundant step in branch construction ([6c68888](https://github.com/fxstein/ai-todo/commit/6c68888818da30b042ef2a120e4b716536006680))
- refactor: Always construct branch names, never use Linear's gitBranchName ([2cf15f6](https://github.com/fxstein/ai-todo/commit/2cf15f626c1a5727c4167585aeec2e4a19eb025e))
- refactor: Standardize branch naming to always use userid prefix ([7685d2e](https://github.com/fxstein/ai-todo/commit/7685d2ed5a83485f20868b7c5c88cb5aaed4ebf4))
- docs: Specify PR body format in Linear integration rule ([e815419](https://github.com/fxstein/ai-todo/commit/e8154191ff410e98ae82dfc7d9e38dc8ec2311c2))
- refactor: Enhance closing workflow with PR creation and cleanup steps ([4bcbe71](https://github.com/fxstein/ai-todo/commit/4bcbe717bf599dd885de1078eeecc493d5d634c6))
- refactor: Simplify branch naming in Linear integration rule ([22db187](https://github.com/fxstein/ai-todo/commit/22db18753d83e96d9dbb2509f28ee7c02f273af7))
- docs: Add Issue Investigation workflow to linear-document-workflow rule ([6aec0c0](https://github.com/fxstein/ai-todo/commit/6aec0c08fc90e14127d376ab39d4c2ff583bf660))
- refactor: Remove fragile string parsing in archive backup footer (task#267) ([f8dad72](https://github.com/fxstein/ai-todo/commit/f8dad729a8f7b85a8c8537b9ff6eb831d56f25a4))
- docs: add Linear document & task workflow rule (task#267) ([f2cc740](https://github.com/fxstein/ai-todo/commit/f2cc740435c7e16d9fc1884442c1cf13f7f34dc2))
- task: Complete #267 - Prune function implementation (task#267) ([aca7b0c](https://github.com/fxstein/ai-todo/commit/aca7b0c692e623e3c3687e74e8b653acb3d64925))
- docs: Add prune command documentation and examples (task#267) ([5573f31](https://github.com/fxstein/ai-todo/commit/5573f31c8d579c400d445a1a75cb9012146d24c3))
- test: Add comprehensive prune integration tests (task#267) ([09a6b08](https://github.com/fxstein/ai-todo/commit/09a6b0808570a98a7bff64591ab1bd8423ce2584))
- test: Execute prune operations and add TASK_METADATA to backups (task#267) ([990fce8](https://github.com/fxstein/ai-todo/commit/990fce8ce1b6f961e4d8118f33b0d904d465f5ff))
- test: Verify TASK_METADATA preservation in prune backups (task#267) ([9df4d05](https://github.com/fxstein/ai-todo/commit/9df4d05c1c34f979fda8da30b580cc575767ac8e))
- test: Add comprehensive unit tests for prune functionality (task#267) ([300b002](https://github.com/fxstein/ai-todo/commit/300b0022c41a899821c643578192af49ef2e209e))
- docs: Add prune function analysis and design documents (task#267) ([bcc513a](https://github.com/fxstein/ai-todo/commit/bcc513a0d243050ccd9840f56502236fe340732a))
- docs: Linear integration design and assessment (task#266) ([7b40cb1](https://github.com/fxstein/ai-todo/commit/7b40cb1eedba6737da7c315bae5a45b71a145446))
- docs: Add Linear integration assessment (task#266) ([f39bdac](https://github.com/fxstein/ai-todo/commit/f39bdac74a4e1fba87077e49267372c0d2173063))
- docs: Mark 265.1 complete and fix Linear rule tool names (task#265) ([f461b07](https://github.com/fxstein/ai-todo/commit/f461b07c4c3cadce913e21e667e363f88c906395))

## Previous Beta Release Notes

### Release 4.0.0b2

This release addresses a critical bug (GitHub Issue #49) where archived tasks with incomplete subtasks would incorrectly reappear in the Tasks section when adding new tasks. The fix changes how task status is determined during parsing: section membership now takes precedence over checkbox state, ensuring that all tasks in "Recently Completed" or "Archived Tasks" sections are properly treated as archived regardless of their checkbox character.

Additionally, this release fixes the `config://settings` MCP resource to correctly report `coordination.enabled` status. Previously it was checking for a non-existent configuration key, causing it to always return `false`. The resource now properly derives the enabled state from the configured coordination type.

Both fixes include regression tests to prevent these issues from recurring. Users who experienced archived tasks unexpectedly appearing in their active task list should update to this version immediately.

---

### ✨ Features

- Add task#264 for GitHub Issue #49 - archived tasks reappearing bug ([bbc4468](https://github.com/fxstein/ai-todo/commit/bbc4468c2c3525056ed52e1ff976865340b9b0e6))

### 🐛 Bug Fixes

- Prevent orphan subtasks from leaking into Tasks section (task#264) ([2508033](https://github.com/fxstein/ai-todo/commit/25080333c4421afa2d49afcd52337ba052a62d8b))
- Derive coordination.enabled from type instead of non-existent key ([491842d](https://github.com/fxstein/ai-todo/commit/491842d0a5346704801bc25cbee75d7ac4406372))

### 🔧 Other Changes

- chore: Update release log for v4.0.0b2 ([0885f41](https://github.com/fxstein/ai-todo/commit/0885f41258cc3f89681f2a4b61978ca3c867cb12))
- docs: Prepare release notes for v4.0.0b2 ([5adbd23](https://github.com/fxstein/ai-todo/commit/5adbd23fbbcb9f79c53b25ca635cde185b8357e4))
- docs: Add AI release summary for v4.0.0b2 ([ceeea5c](https://github.com/fxstein/ai-todo/commit/ceeea5c40f0962d24c3f05a3191b792ac59ca69d))
- internal: Archive completed task#264 (GitHub Issue #49 fix) ([be5c9b8](https://github.com/fxstein/ai-todo/commit/be5c9b8e1dc02e7d47d5bf0d7d7ae39f539f8b0b))
- docs: Update CHANGELOG.md for v4.0.0b1 release ([401ed5b](https://github.com/fxstein/ai-todo/commit/401ed5bc5bcaa875eee70cae878f7d164e1c76d1))

### Previous Beta Release Notes

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
