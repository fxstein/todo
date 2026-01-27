# Release 3.0.2

This release fixes a critical bug where TODO.md files became malformed when adding multiple subtasks via MCP on fresh repositories. The issue caused orphaned timestamp lines to accumulate in the file, breaking the expected format. The fix ensures footer timestamps are properly handled and always regenerated cleanly, while also updating the branding from legacy "todo.ai" to "ai-todo" in default headers.

The cursor rule generator that installs rules in new projects now documents that tasks are displayed in reverse chronological order (newest on top), helping prevent confusion about the intentional task ordering behavior.

---

## 🐛 Bug Fixes

- Resolve malformed TODO.md on fresh repos with multiple subtasks (task#240) ([cddfb9d](https://github.com/fxstein/ai-todo/commit/cddfb9df563d9830a4e702d3d916b831e55f04b9))

## 🔧 Infrastructure

- Add fastmcp 3.x compatibility testing in CI (task#239) ([661253b](https://github.com/fxstein/ai-todo/commit/661253b89d6ca9376204a95ec51e61d06e777e16))
