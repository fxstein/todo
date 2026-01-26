## ai-todo v3.0.1 Release Summary

This patch release fixes a bug in the archive cooldown feature and updates CI/CD dependencies.

**Bug Fix:** The archive cooldown (which prevents AI agents from immediately archiving completed tasks) was incorrectly triggering for all tasks because `completed_at` timestamps were reset to `datetime.now()` when parsing TODO.md. The cooldown is now session-based in the MCP server, only blocking archival of tasks completed within the current session. This allows archiving of previously completed tasks while still protecting against overeager agents archiving tasks immediately after completion.

**Infrastructure:** Updated GitHub Actions dependencies via Dependabot: `actions/checkout` v6, `actions/setup-python` v6, `actions/cache` v5, `astral-sh/setup-uv` v7, and `markdownlint-cli2-action` v22.
