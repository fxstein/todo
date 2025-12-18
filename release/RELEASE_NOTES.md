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

### ✨ Features

- Add --abort command to clean up failed releases ([1dee0af](https://github.com/fxstein/todo.ai/commit/1dee0afb169bfdebe71d72e47d5d81bbf89cc239))
- Implement clean release dependencies with Python PEP 440 validation ([7305dd0](https://github.com/fxstein/todo.ai/commit/7305dd03402500e8973c79d277520655ba665894))
- Fix release workflow dependencies and sequencing (task#177) ([7443ce9](https://github.com/fxstein/todo.ai/commit/7443ce9cefe5f07aa9069803ef410d60ae428d0e))
- Improve workflow run naming and version commit message ([7268a41](https://github.com/fxstein/todo.ai/commit/7268a4118e7bd29b04d6baf211e45d31db5be319))
- Add dynamic workflow names with emojis for clarity (task#177) ([450c7fe](https://github.com/fxstein/todo.ai/commit/450c7fe42951c1132d2b5d91fe761e8e56ca52ab))
- Add three-layer defense against forbidden flags (task#175) ([1b603bf](https://github.com/fxstein/todo.ai/commit/1b603bfbf5cc85ae9501bd86502947368e9eadf5))

### 🐛 Bug Fixes

- Make workflow CI check tolerate 'pending' status ([39621bd](https://github.com/fxstein/todo.ai/commit/39621bd1d55211f147f01c7fb1908e1880e82a53))
- Add 10s wait before CI status check to prevent race condition ([c876297](https://github.com/fxstein/todo.ai/commit/c8762973064ddc842307bc83a2701426d100f2b8))
- Remove quotes from Python heredoc to allow variable expansion ([8c71f54](https://github.com/fxstein/todo.ai/commit/8c71f54e5c5c815ebaec82f6426033e28e98eb01))
- Use run-name instead of name for dynamic workflow titles ([ac483de](https://github.com/fxstein/todo.ai/commit/ac483de6e3e9268703b1ce5174d4fc83654f6137))
- Add environment field for PyPI Trusted Publisher (task#177.1) ([f1ec156](https://github.com/fxstein/todo.ai/commit/f1ec1563d9f0380a98226b6fd8bd096b99ae7935))
- Move GitHub release creation to workflow (after PyPI success) (task#177.2, task#177.3) ([c58526d](https://github.com/fxstein/todo.ai/commit/c58526dda65b3d7bd2554d7a6cea5eac9d29326a))
- Merge CI and Release workflows with mandatory dependencies (task#176) CRITICAL ([1ca2563](https://github.com/fxstein/todo.ai/commit/1ca2563eeb8350d0726cc8d0fe8870f87f18d485))
- Skip bash script test on Windows (task#175) ([700bd6f](https://github.com/fxstein/todo.ai/commit/700bd6f60284f32121ff6e015ec3368f6b30286d))
- Remove --no-verify from release script (task#173.12) CRITICAL ([1a718a0](https://github.com/fxstein/todo.ai/commit/1a718a04d1bbeab0e8fd9b854a50517e17bdcb51))
- Run pre-commit hooks before staging to prevent format issues (task#173.11) ([84055f6](https://github.com/fxstein/todo.ai/commit/84055f66c91173da47cae04002eeef234bb4b6c6))
- Fix todo.bash formatting issues causing CI failures (task#173.10) ([e22f107](https://github.com/fxstein/todo.ai/commit/e22f1073813fe631aa2a174c7b92fa61a6b729f4))
- Auto-detect RELEASE_SUMMARY.md in prepare phase (task#173.9) ([16a2191](https://github.com/fxstein/todo.ai/commit/16a21919cd643029fa3346cafe488eb101dbcd7a))
- Fix pathspec issue in pre-commit hook re-staging (task#173.8) ([88e4f51](https://github.com/fxstein/todo.ai/commit/88e4f51487b197aa6fd7b4be1b8790a2c308339a))

### 🔧 Other Changes

- chore: Remove stale release artifacts from index ([f73e200](https://github.com/fxstein/todo.ai/commit/f73e200f5d421b48ce9aae40113c77fb84462374))
- chore: Bump version to 3.0.0b2 ([a1bb5bc](https://github.com/fxstein/todo.ai/commit/a1bb5bc5fbe02e1b3bbbddc085b73e713c8ca462))
- chore: Clean up release artifacts from git index ([7c6dc9c](https://github.com/fxstein/todo.ai/commit/7c6dc9c79feb6dc261a37be66858b73eeec58584))
- chore: Bump version to 3.0.0b2 ([9e26524](https://github.com/fxstein/todo.ai/commit/9e26524e31caf8ba853652d8fa4ea3a95ed75d12))
- chore: Remove temporary release artifacts from index ([8398d30](https://github.com/fxstein/todo.ai/commit/8398d30f62338cd5e63e187c65d5584227b3ca7e))
- chore: Reset version to 3.0.0b1 to retest with fixed Python validation ([268bca3](https://github.com/fxstein/todo.ai/commit/268bca3f1fbd472a27846235960732b31a98c4cc))
- chore: Bump version to 3.0.0b2 ([8a8798d](https://github.com/fxstein/todo.ai/commit/8a8798d81e9ba3433fdcf5b0551cfa38d319ed20))
- chore: Reset version to 3.0.0b1 to retest release with new dependencies ([9f19547](https://github.com/fxstein/todo.ai/commit/9f19547709cc5fe9dbe96bf6a62dd469249a194a))
- chore: Bump version to 3.0.0b2 ([987b8c2](https://github.com/fxstein/todo.ai/commit/987b8c22f7c7a89b1f73c3b3674704ca4875a87a))
- chore: Reset version to 3.0.0b1 for release retest ([88f329a](https://github.com/fxstein/todo.ai/commit/88f329a3bf9a315d99e80936a1972402017052b0))
- chore: Revert version to 3.0.0b1 for release process testing ([f8d0ad0](https://github.com/fxstein/todo.ai/commit/f8d0ad0bcff7f5c843b091600b77a3321494ec18))
- docs: Update release summary to focus on Python refactor, not process ([a442e0b](https://github.com/fxstein/todo.ai/commit/a442e0b4c5d7c55efdcaf79e454efe91060f13ce))
- chore: Add AI release summary for v3.0.0b2 ([4456c0b](https://github.com/fxstein/todo.ai/commit/4456c0b97254345049d104151043ca886508d9a6))
- docs: Add rule forbidding --no-verify in release process ([949e11e](https://github.com/fxstein/todo.ai/commit/949e11eab674d39f8ffa8c191759a9ab686d2de0))
- chore: Complete beta release tasks (task#172.4.1, task#174.7, task#174) ([0ad2c95](https://github.com/fxstein/todo.ai/commit/0ad2c9534a76fac5a91e5d338ac7e190729aed33))
