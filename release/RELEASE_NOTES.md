# Release 3.0.0

## ai-todo v3.0.0 Release Summary

**ai-todo v3.0.0** represents a complete rewrite of the project, evolving from a shell-based task management tool into a modern, production-ready Python package. The MCP server and CLI are now unified into a single executable (`ai-todo`), providing seamless integration with AI assistants like Cursor while maintaining a powerful command-line interface. Installation is as simple as `pip install ai-todo` or `uv tool install ai-todo`, and the package is published via PyPI with secure OIDC-based trusted publishing.

This major release introduces several key features for data integrity and workflow safety. A **tamper detection system** protects TODO.md from unintended external modifications, with configurable security modes and automatic recovery options. An **archive cooldown** (60-second default) prevents AI agents from prematurely archiving completed tasks, requiring human review for root tasks. The new **start/stop commands** allow marking tasks as in-progress with `#inprogress` tags. The **delete command** now removes subtasks by default, and deleted tasks display with `[D]` markers instead of confusing checkmarks.

The architecture has been significantly modernized. The Python implementation uses **FastMCP** for the MCP server with full async support. The CLI uses **Click** with rich help text. A comprehensive **CI/CD pipeline** on GitHub Actions handles testing across Python 3.13+ on Ubuntu, macOS, and Windows, with automated PyPI publishing on tagged releases. The data directory migrated from `.todo.ai/` to `.ai-todo/` with automatic migration for existing users. Legacy shell scripts remain available but are deprecated. The MCP/CLI tool set was audited and streamlined from 37 to 27 tools, removing redundant operations and standardizing naming conventions.

---

### ✨ Features

- Add beta-to-stable graduation logic for releases (task#238.11) ([a8fcd6e](https://github.com/fxstein/ai-todo/commit/a8fcd6e18937b8660155c9ba7014eb748bd0224f))
- Add archive cooldown protection for root tasks (task#205) ([aa54253](https://github.com/fxstein/ai-todo/commit/aa542531eb8e06d3f905371cb6a8938c9621d709))
- Implement MCP/CLI tools audit cleanup (task#238.4) ([d4b1969](https://github.com/fxstein/ai-todo/commit/d4b1969b40941cacc06e207248677e569de83b4a))

### 🐛 Bug Fixes

- Handle PermissionError in cursor rules init, fix PR tests CI ([2d83539](https://github.com/fxstein/ai-todo/commit/2d83539318c7096efb84b34d1d54706447779049))
- Improve archive cooldown to block entire operation and simplify message ([57e9a16](https://github.com/fxstein/ai-todo/commit/57e9a167bc3a92e358a01da742a46dbd6c000711))
- Prevent legacy shell script from creating Cursor rules in dev repo ([5ad5239](https://github.com/fxstein/ai-todo/commit/5ad523962537ae6b0e4e1e135bcf00442c68110b))
- Show deleted tasks with [D] instead of [x] (task#222) ([d7c3c9d](https://github.com/fxstein/ai-todo/commit/d7c3c9d24ca49954307bcca418eb18b4bc62286a))
- Delete task now removes subtasks by default (task#221) ([9819f0f](https://github.com/fxstein/ai-todo/commit/9819f0f5303518195fef9297c17e65d9460afac6))
- Update test fixtures with ai-todo GitHub URLs (task#219.11) ([a0c4868](https://github.com/fxstein/ai-todo/commit/a0c48687045aee8960901067bb532959e7703595))
- Update ai_todo/ source code with ai-todo naming (task#219.10) ([f68ecba](https://github.com/fxstein/ai-todo/commit/f68ecba547d80e2b12e4f47a69613d9797272386))

### 🔧 Other Changes

- docs: Update AI release summary for v3.0.0 stable (full beta cycle) ([ebc884e](https://github.com/fxstein/ai-todo/commit/ebc884e762b350304007f64f70368579a5416d5d))
- docs: Add AI release summary for v3.0.0 ([459af0a](https://github.com/fxstein/ai-todo/commit/459af0a4c769935b008ff339ddac69737a1fa45b))
- infra: Move commit counter to scripts/.run-full-tests-periodic ([ac21eae](https://github.com/fxstein/ai-todo/commit/ac21eae4091afa223213ffd1c74cf7a4fd71ff81))
- infra: Add periodic full test suite in pre-commit (every 10th commit) ([401ff77](https://github.com/fxstein/ai-todo/commit/401ff772c6c158a71c39867418004ba59d78e3c5))
- docs: Add MCP server enable step to Quick Start ([4ea73ee](https://github.com/fxstein/ai-todo/commit/4ea73eef2b173816117488253d33f925fd840a55))
- infra: Enable Dependabot for Python and GitHub Actions ([3cf93c3](https://github.com/fxstein/ai-todo/commit/3cf93c3f3ebedb56b902070d64407ade1ad3cb22))
- infra: Remove legacy .cursorrules, fix state directory path (task#238.6) ([be6e514](https://github.com/fxstein/ai-todo/commit/be6e514c97e628d53386a6d8e6351b6887fd712d))
- docs: Add MCP/CLI tools audit for v3.0 cleanup (task#238.4) ([a154076](https://github.com/fxstein/ai-todo/commit/a15407651a6825e2e68b4b98bd65a51b91f7a23d))
- test: Add tests for MCP server Cursor rules auto-installation ([1484f71](https://github.com/fxstein/ai-todo/commit/1484f71ae55305153659d02418d5903f618976bd))
- refactor: Consolidate Cursor rules to single MCP-focused file (task#235) ([e91b235](https://github.com/fxstein/ai-todo/commit/e91b235fff2b3b23bce070973177620028718952))
- test: Add tests for delete with subtasks behavior (task#221) ([7263b3e](https://github.com/fxstein/ai-todo/commit/7263b3e2275966cb7b1643d760535615d82e5042))
- chore: Create v3.0 release checklist and future backlog tasks ([87f1e0f](https://github.com/fxstein/ai-todo/commit/87f1e0fbc709693dcffef1dd7e05930049deca07))
- docs: Add Gemini integration design doc and MCP config cleanup ([9d158bc](https://github.com/fxstein/ai-todo/commit/9d158bc4dca68d56c463170013a29d44e75d8855))
- docs: Clarify audit document - all issues resolved ([72d86dc](https://github.com/fxstein/ai-todo/commit/72d86dc04b6bc4d2ea807e5f36a706ddb4c83ce2))
- chore: Mark cleanup subtasks complete (task#219) ([ad0c8ea](https://github.com/fxstein/ai-todo/commit/ad0c8eaa9e0e363b9df2c732dc1732d2fd338016))
- docs: Complete post-migration naming audit verification (task#219.13) ([420e502](https://github.com/fxstein/ai-todo/commit/420e50289508e63151075241eedd9d21c7e904f4))
- docs: Update documentation with ai-todo command references (task#219.12) ([01345c9](https://github.com/fxstein/ai-todo/commit/01345c94c6830df1fa4d11ed0552263a1bc9e28b))
- chore: Add post-migration cleanup subtasks to task#219 ([f4e2c3c](https://github.com/fxstein/ai-todo/commit/f4e2c3cdb4ca64c139890a6e9535734c2507e650))
- docs: Add post-migration naming audit (task#219.9) ([be65869](https://github.com/fxstein/ai-todo/commit/be65869c7d5e84022a2fe7eaa5feab337ebdea47))
