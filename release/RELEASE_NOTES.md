# Release 3.0.1

## ai-todo v3.0.1 Release Summary

This patch release fixes a bug in the archive cooldown feature and updates CI/CD dependencies.

**Bug Fix:** The archive cooldown (which prevents AI agents from immediately archiving completed tasks) was incorrectly triggering for all tasks because `completed_at` timestamps were reset to `datetime.now()` when parsing TODO.md. The cooldown is now session-based in the MCP server, only blocking archival of tasks completed within the current session. This allows archiving of previously completed tasks while still protecting against overeager agents archiving tasks immediately after completion.

**Infrastructure:** Updated GitHub Actions dependencies via Dependabot: `actions/checkout` v6, `actions/setup-python` v6, `actions/cache` v5, `astral-sh/setup-uv` v7, and `markdownlint-cli2-action` v22.

---

### 🐛 Bug Fixes

- Make archive cooldown session-based in MCP server ([683fa05](https://github.com/fxstein/ai-todo/commit/683fa05503eb2f3b2e7dd14d478f02bf5108aae7))

### 🔧 Other Changes

- docs: Add AI release summary for v3.0.1 ([461399b](https://github.com/fxstein/ai-todo/commit/461399b16ddd4523e21676314e4aa8e20ffb42ad))
- chore: Archive completed v3.0 release tasks ([fc4c6f8](https://github.com/fxstein/ai-todo/commit/fc4c6f8e0dbee8b6587d8acadffbaca06dea85be))
- chore(deps): Bump `astral-sh/setup-uv` from 3 to 7 ([dede9b0](https://github.com/fxstein/ai-todo/commit/dede9b03c2a852cb68e8e4dd56c23f843d41416b))
- chore(deps): Bump `actions/cache` from 4 to 5 ([0c13116](https://github.com/fxstein/ai-todo/commit/0c131167ff281ddd3541e620c3b75649f37dcf8f))
- chore(deps): Bump `DavidAnson/markdownlint-cli2-action` from 20 to 22 ([934deef](https://github.com/fxstein/ai-todo/commit/934deefd152268187fe9f7179fc34e184cd6963d))
- chore(deps): Bump `actions/checkout` from 4 to 6 ([4121abf](https://github.com/fxstein/ai-todo/commit/4121abf00ed6870a10e83f656a03e96c37708c4f))
- chore(deps): Bump `actions/setup-python` from 5 to 6 ([eedcd0a](https://github.com/fxstein/ai-todo/commit/eedcd0ace96c7429949c7d23056bc0499fccd4c2))
