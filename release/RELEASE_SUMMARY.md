This release fixes a critical bug where TODO.md files became malformed when adding multiple subtasks via MCP on fresh repositories. The issue caused orphaned timestamp lines to accumulate in the file, breaking the expected format. The fix ensures footer timestamps are properly handled and always regenerated cleanly, while also updating the branding from legacy "todo.ai" to "ai-todo" in default headers.

Additionally, this release adds proactive compatibility testing for fastmcp 3.x in the CI pipeline. This experimental job monitors compatibility with the upcoming fastmcp 3.0 release, helping catch breaking changes early. The job is informational only and does not block releases.

The cursor rule generator that installs rules in new projects now documents that tasks are displayed in reverse chronological order (newest on top), helping prevent confusion about the intentional task ordering behavior.
