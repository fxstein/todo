## Release 3.0.0b17

## Summary

This release introduces the **Tamper Detection System**, a significant new feature that protects TODO.md integrity by detecting external modifications. When enabled, todo.ai maintains a shadow copy and checksum of TODO.md, alerting users if the file is modified outside of todo.ai tools. This is an opt-in feature that helps maintain task consistency in collaborative or automated environments.

Several important bug fixes improve the overall experience. Subtask sorting now uses numerical comparison instead of alphabetical, ensuring task#10 appears after task#9 rather than after task#1. The restore command has been fixed to correctly position both root tasks and subtasks. A whitespace conflict between todo.ai and pre-commit hooks has been resolved, and UTF-8 encoding is now explicitly specified for Windows compatibility.

Documentation and developer experience have been enhanced with simplified Cursor rules that are more concise and actionable. The TODO.md visual standards have been implemented to ensure consistent formatting, and the tamper detection documentation clearly explains the feature as an optional integrity tool rather than a security mechanism.

---

### ✨ Features

- Complete Task #210 - Tamper Detection System ([147cc67](https://github.com/fxstein/todo.ai/commit/147cc672c3eebffe2ad726ecaae4b2c4a610bdea))
- Implement dual logging strategy (shared + local audit log) ([8c62862](https://github.com/fxstein/todo.ai/commit/8c628623403c6d1927ae6b418a25f90c65c0c51a))
- Implement Tamper Detection System (task#210.4, task#210.5) ([b1fb0bd](https://github.com/fxstein/todo.ai/commit/b1fb0bd866708d04e4007dee6377f80cfe91da64))
- Add task#211 to fix subtask alphabetical sorting bug ([0bef627](https://github.com/fxstein/todo.ai/commit/0bef6274d8be111a5d61b645d4e278fd57186b80))
- Add task#210 for TODO.md tamper detection (task#210) ([b53eb33](https://github.com/fxstein/todo.ai/commit/b53eb33f13ed548254e2a001a7e2b3c0dcc14a49))
- Implement TODO.md visual standards (task#200) ([08ab23c](https://github.com/fxstein/todo.ai/commit/08ab23ca4870c73ac64a84b996581aee77a173f8))

### 🐛 Bug Fixes

- Skip cursor rules auto-generation in development repository (task#218) ([999c1ed](https://github.com/fxstein/todo.ai/commit/999c1ed79b3630bf8e65e2232ac73f6298247884))
- Add explicit UTF-8 encoding to read_text() calls for Windows (task#217) ([44ef639](https://github.com/fxstein/todo.ai/commit/44ef6392faaefef73e8d911fbf09f39d19cf67f6))
- Normalize date and section header differences in parity tests (task#217) ([8df5d1e](https://github.com/fxstein/todo.ai/commit/8df5d1e29019a8868dc4c4b1c8352bb610150fe2))
- Restore file structure preservation logic (Task #216) ([a310b17](https://github.com/fxstein/todo.ai/commit/a310b17b8b7a9480b30de07fb699b0dd5628c00b))
- Restore Task #213 and verify whitespace fix ([c2d5703](https://github.com/fxstein/todo.ai/commit/c2d57039eda04818f89e8bfdcceaf792eae67a07))
- Resolve whitespace conflict between todo.ai and pre-commit hooks (Task #213) ([a9c5b92](https://github.com/fxstein/todo.ai/commit/a9c5b92dd3e4128139de99a83d1bde404bbfe28e))
- Fix subtask sorting to use numerical comparison instead of alphabetical (task#211) ([723fb4e](https://github.com/fxstein/todo.ai/commit/723fb4ece2dd586078d3b486a49da6f993b9405c))
- Resolve orphaned subtasks by restoring and re-archiving parent tasks ([0edd165](https://github.com/fxstein/todo.ai/commit/0edd165ad1bfa5945dbc902debfb0ca3fe263805))
- Remove outdated 'Remaining' note from completed task#200 ([4632752](https://github.com/fxstein/todo.ai/commit/4632752182e9f8f04b99f12d058ffd0e996c6f65))
- Fix restore command positioning for root tasks and subtasks (task#200) ([622d48f](https://github.com/fxstein/todo.ai/commit/622d48f41a34072c949ba2ba0802d854b5cded99))
- Enforce strict spacing and fix date duplication in TODO.md ([665863b](https://github.com/fxstein/todo.ai/commit/665863b4836137f8de1510f0f64d3c87ef35b348))

### 🔧 Other Changes

- chore: Update TODO.md state ([1faffcd](https://github.com/fxstein/todo.ai/commit/1faffcdf8d2c2d2fc7f5dd12aaa32241e7bd6b5c))
- docs: Add AI release summary for v3.0.0b17 ([b2d64e9](https://github.com/fxstein/todo.ai/commit/b2d64e955cf5402bed7215fe6e6f403eabc9ad2b))
- docs: Simplify cursor-rules-guidelines.mdc (task#218) ([0af93c4](https://github.com/fxstein/todo.ai/commit/0af93c48127cf53e1ac25778325d2a1aebe817d6))
- docs: Simplify todo-ai-interaction.mdc Cursor rule (task#218) ([6bdea0a](https://github.com/fxstein/todo.ai/commit/6bdea0aa985acca7bc81c9d3be9ff51fdf66f7e2))
- docs: Simplify release-workflow.mdc Cursor rule (task#218) ([5992767](https://github.com/fxstein/todo.ai/commit/5992767645ccf2b3fea7682ee92a7ba6d91804f7))
- docs: Add AI release summary for v3.0.0b17 ([8506858](https://github.com/fxstein/todo.ai/commit/8506858f85ec7da9948342bff39467d60a062c48))
- test: Update parity tests to ignore header/footer differences (Task #217) ([d954d98](https://github.com/fxstein/todo.ai/commit/d954d988870cd28f98a3aefa97d7973414f9365e))
- chore: Archive Task #213 (Whitespace conflict resolution) ([8452d9e](https://github.com/fxstein/todo.ai/commit/8452d9e3ad554d439d1ef2af532c10b65446d169))
- chore: Complete Task #213 (Whitespace conflict resolution) ([ea5f5c8](https://github.com/fxstein/todo.ai/commit/ea5f5c81ab468f3d1f2fe0af2ff6885e0ee2a313))
- chore: Delete Task #215 (Jokes collection) ([2be81ab](https://github.com/fxstein/todo.ai/commit/2be81ab927175d6c8d23dd9765f5cfae35a67827))
- chore: Update Task #213 subtasks to completed ([e7aa5b0](https://github.com/fxstein/todo.ai/commit/e7aa5b0785655b630bed97ed4ca3f57cc4f9c7d6))
- docs: Add analysis for whitespace conflict and track Task #213 ([de93752](https://github.com/fxstein/todo.ai/commit/de937529c2ef4f26a86c1b3ac9a82a5e27e7502b))
- chore: Archive completed task #212 ([8e3d7bf](https://github.com/fxstein/todo.ai/commit/8e3d7bff479fc7334b5f1a11c53b8ca948bc60fc))
- chore: Complete Task #212 and add .cursorignore ([b6cfec6](https://github.com/fxstein/todo.ai/commit/b6cfec66695ab56fc86ea06bb40dc648a39f6495))
- chore: Consolidate and update Cursor rules for MCP-first workflow (Task #212) ([472423d](https://github.com/fxstein/todo.ai/commit/472423d7434a7f7fd7e8a962a08c94b70958e206))
- Archive completed task #210 (Tamper Detection System) ([3c84eab](https://github.com/fxstein/todo.ai/commit/3c84eabc75921e252ddf8287edd621e172c1166d))
- docs: Tone down tamper detection description in dev guidelines ([7bbdcb1](https://github.com/fxstein/todo.ai/commit/7bbdcb1728adc07b8a69d023916ad9baf1a04f43))
- docs: Remove reference to todo-ai edit command ([158be11](https://github.com/fxstein/todo.ai/commit/158be11f67d291352b02ef7d0f38caf180a11600))
- docs: Emphasize tamper detection is optional and passive by default ([66f496b](https://github.com/fxstein/todo.ai/commit/66f496b6530849bce3d261037156c98e86ee9906))
- docs: Clarify tamper detection is for integrity not security ([86550b3](https://github.com/fxstein/todo.ai/commit/86550b3eeba9d39e129076f3520606ef2af95518))
- docs: Tone down tamper detection description ([96e897c](https://github.com/fxstein/todo.ai/commit/96e897c9e7ec3c6962cf23e90b8f8da2ab436297))
- docs: Document Tamper Detection feature (Task #210.6) ([9a744de](https://github.com/fxstein/todo.ai/commit/9a744de78d2f255487d3dfa542fa57e0242449b0))
- chore: Protect integrity files from manual edits in VS Code ([e69987b](https://github.com/fxstein/todo.ai/commit/e69987b9980cc32abd5f35b4e5c389430b4910b6))
- chore: Configure IDE read-only mode and finalize state directory refactor ([e2a0fa3](https://github.com/fxstein/todo.ai/commit/e2a0fa3b6dce434f59d2bd69bc2d69ef12c9a6c4))
- refactor: Move tamper detection state to .todo.ai/state/ ([c793321](https://github.com/fxstein/todo.ai/commit/c793321d4c62e7dc6e474322819aa8e79d2bfbc3))
- docs: Complete research and design for tamper detection (task#210.2, task#210.3) ([30ce4f6](https://github.com/fxstein/todo.ai/commit/30ce4f659f3190998c64dcf1c0d54a16822ff638))
- Archive completed tasks #211, #125, #126, #161 ([8bfd633](https://github.com/fxstein/todo.ai/commit/8bfd63343880bc989fd73bba4845ddfc82f69341))
- docs: Complete task#210.1 - Analyze TODO.md tamper detection ([2805473](https://github.com/fxstein/todo.ai/commit/280547356ce52ccb60630da859d6ecc8e3ea12c4))
- chore: Archive completed task#200 (visual standards) ([dee09ec](https://github.com/fxstein/todo.ai/commit/dee09ec9502151c35e82055113f84ae4968a8bbd))
- chore: Update task serial for task#210 ([5c2b3bd](https://github.com/fxstein/todo.ai/commit/5c2b3bde83652251c11956c646092466f5bc00fe))
- docs: Complete task#200 - TODO.md visual standards implementation ([4e7ca8e](https://github.com/fxstein/todo.ai/commit/4e7ca8e163ba0f8e387c92978a80fbc2f0e9173e))
- docs: Complete task#200.6 - Document TODO.md visual standards ([0f3b361](https://github.com/fxstein/todo.ai/commit/0f3b3619807fc68c90b55ad3994ff67c3058643c))
- docs: Simplify task#200 notes to concise summary ([fccd7bb](https://github.com/fxstein/todo.ai/commit/fccd7bbda6db55e41acde29bb580cf63a479cdc0))
- docs: Add test subtasks for visual standards validation (task#200) ([b3d5624](https://github.com/fxstein/todo.ai/commit/b3d56247bbb71276898c4a1ca9e00ca153e68b91))
- docs: Update TODO.md with refined task#200 subtasks ([7be709c](https://github.com/fxstein/todo.ai/commit/7be709c7bb1d04164829a51b38b2cf8d79328161))
- docs: Create TODO.md visual standards design document (task#200.2) ([a4c5417](https://github.com/fxstein/todo.ai/commit/a4c5417b867850afd0f879c5b13a8fabddbc697b))

## Previous Beta Release Notes

## Release 3.0.0b16

This beta release brings significant improvements to task workflow management and cross-version compatibility. The headline feature is the new `start` and `stop` commands, which allow you to mark tasks as in-progress and track active work across sessions. When you start a task, it automatically gets tagged with `#inprogress`, and AI agents using the MCP server can now see which tasks are actively being worked on through a dedicated status prompt. This makes it easier to maintain context across multiple coding sessions and prevents duplicate work on the same tasks.

The Python CLI has been upgraded to support Python 3.14 while maintaining full backward compatibility with Python 3.10 through 3.13, ensuring the tool works across a wide range of environments. We've also fixed several important bugs that improve reliability: the `restore` command now correctly restores subtasks in the proper order and preserves their completion status, the `--root` parameter now works correctly in the Python CLI (it was previously being ignored), and test isolation has been significantly improved to prevent cross-test contamination.

Behind the scenes, we've enhanced the development infrastructure with integrated `todo-ai lint` checks in pre-commit hooks and CI/CD pipelines, ensuring consistent TODO.md formatting across all contributions. The test suite now includes comprehensive parity validation between the shell script and Python CLI, with better environment isolation and more robust path resolution. These improvements make todo.ai more reliable and maintainable for both users and contributors.

---

### ✨ Features

- Implement 'start' and 'stop' commands with MCP support (task#201) ([066bb60](https://github.com/fxstein/todo.ai/commit/066bb605d278ceaaf06c545951f3d7fec9ca8e7a))
- Design 'start' command architecture (task#201) ([813e36f](https://github.com/fxstein/todo.ai/commit/813e36f021d3e861790ff9ae3fa638f170bf007e))
- Enhance task management with ordering fixes and linting tools ([e595b0e](https://github.com/fxstein/todo.ai/commit/e595b0e32e793dede2e5c46db1be0d7accc6b548))

### 🐛 Bug Fixes

- Make Python CLI respect --root parameter and fix test isolation (task#207) ([e747422](https://github.com/fxstein/todo.ai/commit/e747422367235e27c6aa0dfa0875c7bfdc40dc1d))
- Clear TODO_FILE environment variable in parity tests (task#206) ([ed3649b](https://github.com/fxstein/todo.ai/commit/ed3649b6d62e7ad5d655fd7924c0067729b893b3))
- Suppress cursor rules initialization and mode display during tests (task#206) ([851545e](https://github.com/fxstein/todo.ai/commit/851545eacd853c2b07fb03681c638e7d66cf3228))
- Populate completed_at for archived tasks in FileOps (task#204) ([a1be429](https://github.com/fxstein/todo.ai/commit/a1be429388397d699e92b5d0fed9cd4619afb8c8))
- Preserve completion status when restoring tasks (task#204) ([2fe9881](https://github.com/fxstein/todo.ai/commit/2fe98818df926ab382095fe23937a6a648a63e87))
- Restore subtasks in reverse-chronological order (task#204) ([1994bfe](https://github.com/fxstein/todo.ai/commit/1994bfe434f7b170a9c1e5b9a300b786ce72f360))
- Restore subtasks recursively and idempotently (task#204) ([6ba67bf](https://github.com/fxstein/todo.ai/commit/6ba67bf4dea036b96f21c02de3b0bc3a20e7448a))
- Update archive_task MCP tool signature to match CLI default (with_subtasks=True) ([99240d6](https://github.com/fxstein/todo.ai/commit/99240d6a40bb4ab3c529b5a110be4b648d456208))

### 🔧 Other Changes

- Archive completed tasks #202, #206, #207 ([716410b](https://github.com/fxstein/todo.ai/commit/716410b466fab03ff8b18c5469af05b9b91bd033))
- docs: Add task#207 to fix newly discovered parity issues ([6254488](https://github.com/fxstein/todo.ai/commit/6254488aa957b8ec1ff1deaa4d11f128754c3205))
- docs: Complete task#206 (shell script test failures fix) ([8e0477b](https://github.com/fxstein/todo.ai/commit/8e0477b510d2b18993ff5f9bb44c86edfb786074))
- docs: Complete investigation subtasks for task#206 ([e6dffb4](https://github.com/fxstein/todo.ai/commit/e6dffb4fe137d27ae00e3390ac09ac92ea2ceeee))
- docs: Add task#206 to fix shell script test failures ([09330fd](https://github.com/fxstein/todo.ai/commit/09330fd6fb09538f6c82c4fc421053e4ec4344ed))
- docs: Complete task#202 (Python 3.14 upgrade with legacy support) ([4ac8da3](https://github.com/fxstein/todo.ai/commit/4ac8da3e5ef8f176f563d2c2928ad3c11c30670c))
- docs: Archive completed task#204 ([68b74c9](https://github.com/fxstein/todo.ai/commit/68b74c9835a18b9820c67d37e90794602234a112))
- docs: Add task#205 to prevent premature task archiving ([8db76bb](https://github.com/fxstein/todo.ai/commit/8db76bb3f7c69abb4f077a9334ecada5fca71bd6))
- docs: Mark completed subtasks for task#204 ([6b0c491](https://github.com/fxstein/todo.ai/commit/6b0c49132292321fc46becf98c20f7873e618287))
- docs: Add commentary to pre-commit config explaining local execution ([64d3268](https://github.com/fxstein/todo.ai/commit/64d326818363b1472a8f7f581edabc9ac3c8ebb8))
- infra: Use direct module execution for pre-commit lint hook ([97be314](https://github.com/fxstein/todo.ai/commit/97be314ef5ef4573fc2eadb4c29d850fc6fb44d1))
- style: Reorder subtasks for task#204 ([2705757](https://github.com/fxstein/todo.ai/commit/2705757a4cd295165d20990812e9c920ab9dcb75))
- chore: Reopen task#204 to fix restore behavior (preserve completion status) ([18162a9](https://github.com/fxstein/todo.ai/commit/18162a982d0d73ae349423178425cb0fb5ee14a7))
- chore: Start task#204 (Fix restore ordering bug) ([e74017c](https://github.com/fxstein/todo.ai/commit/e74017ccc8195200ba3d2277fa902f8ce870bc09))
- chore: Reopen task#204 to fix subtask ordering bug ([ea91213](https://github.com/fxstein/todo.ai/commit/ea9121359988cebd5b811e3192c06d723392bb4b))
- style: Reorder subtasks for task#202 ([59be33b](https://github.com/fxstein/todo.ai/commit/59be33ba18682250402f9c441da54b185e4539e3))
- chore: Restore task#202 to pending state ([7fb0489](https://github.com/fxstein/todo.ai/commit/7fb048993c5e832efac76bb92e6974864b4e909d))
- chore: Start task#204 (Fix restore subtasks bug) ([de685cd](https://github.com/fxstein/todo.ai/commit/de685cdd4e13b49b244bf25bbb31a5eda4671133))
- docs: Add requirement for idempotent/self-healing restore (task#204) ([86e0aaf](https://github.com/fxstein/todo.ai/commit/86e0aaf0849dac9ce196762a38a7e90ad376381c))
- docs: Add task#204 to fix restore subtasks bug ([b9a0fa0](https://github.com/fxstein/todo.ai/commit/b9a0fa084c6333c24f184dee1de2ee5ef30d12c3))
- infra: Restore legacy Python support (3.10-3.13) while keeping 3.14 preferred (task#202) ([7e54e29](https://github.com/fxstein/todo.ai/commit/7e54e29341cb449a2c8aa2691c8039d928fabce2))
- docs: Archive completed task#202 ([a51b0d8](https://github.com/fxstein/todo.ai/commit/a51b0d814887d2c7e22be0cb4f03ba46c96d243a))
- infra: Upgrade to Python 3.14 and update dependencies (task#202) ([a559e71](https://github.com/fxstein/todo.ai/commit/a559e71f7b8ee4d2d9294c6ecb7ef7a62bbde0f0))
- chore: Start task#202 (Python 3.14 upgrade) ([8b09b16](https://github.com/fxstein/todo.ai/commit/8b09b1670db519013aef12457a9ce52b5d2c62f3))
- docs: Archive completed task#201 ([5f1c4bf](https://github.com/fxstein/todo.ai/commit/5f1c4bf1684241a29a9a70d118542fdbffa0f1d2))
- docs: Add task#203 for README.md redesign (v3.0 migration) ([79709cc](https://github.com/fxstein/todo.ai/commit/79709cc870686d574edc92a7e80549a440ff8212))
- docs: Clarify that 'stop' command is optional (task#201) ([d0b0fe9](https://github.com/fxstein/todo.ai/commit/d0b0fe9cf59fdfeaac35280e33c532cdf8268449))
- docs: Document 'start' and 'stop' commands (task#201) ([a379d8b](https://github.com/fxstein/todo.ai/commit/a379d8b99becc99423e9d9c20bcde9de0a05d456))
- docs: Add 'stop' command to design and task list (task#201) ([0628794](https://github.com/fxstein/todo.ai/commit/0628794858bc550efe10624861bc43e7e368bae1))
- docs: Update 'start' command design with dedicated status tool (task#201) ([b6c7207](https://github.com/fxstein/todo.ai/commit/b6c7207e901f811a1348c1cc8df3505bc7f56c7f))
- docs: Update 'start' command design with MCP Prompts (task#201) ([0cfa53b](https://github.com/fxstein/todo.ai/commit/0cfa53be8d04694b3a2c94b8781c59a19a8b7491))
- docs: Merge task#193 into task#201 ([ecd0fe5](https://github.com/fxstein/todo.ai/commit/ecd0fe5470599009d66eb13f7bd35a1ec8107a06))
- docs: Add task#202 for Python 3.14 upgrade and dependency updates ([96612dd](https://github.com/fxstein/todo.ai/commit/96612dd552185af3542ceca04fd4a0cfdd868ec4))
- docs: Archive completed task#196 ([4925514](https://github.com/fxstein/todo.ai/commit/492551465065ba7ed4f6beeb49b942252863df9b))
- infra: Enhance Pre-commit and CI/CD with todo-ai linting (task#196) ([6f96c18](https://github.com/fxstein/todo.ai/commit/6f96c18b1fb2093028d0c3cfa668f950559c4d12))
- docs: Add task#201 for start command design and implementation ([4b37121](https://github.com/fxstein/todo.ai/commit/4b37121329b5dcd469e3789624788517fed8fca5))
- docs: Archive completed task#188 ([9bd1941](https://github.com/fxstein/todo.ai/commit/9bd1941576c157fe48354a10c856bdc7f6d32f73))
- docs: Archive completed task#195 ([8d3e843](https://github.com/fxstein/todo.ai/commit/8d3e843759eb23ec5a44202821a5fecf6d394112))
- docs: Archive completed tasks and update README with new commands ([a553801](https://github.com/fxstein/todo.ai/commit/a553801471a432083646d042e0b70cd42548a974))
- docs: Update task status for recent completions ([d518f1f](https://github.com/fxstein/todo.ai/commit/d518f1f157ba62bc0c20d62e78e3a7d6cb84c3ff))
- docs: Update task status and documentation for linting features ([7ab6856](https://github.com/fxstein/todo.ai/commit/7ab6856a58f36f3b29fb9c272aece0ff9966af58))
- docs: Update task status for unified executable release ([a2fcb61](https://github.com/fxstein/todo.ai/commit/a2fcb61311b917881d4cd00cc4b4a3ffde879945))

## Previous Beta Release Notes

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
