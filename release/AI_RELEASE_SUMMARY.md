# Release Summary

This release introduces the **Tamper Detection System**, a significant new feature that protects TODO.md integrity by detecting external modifications. When enabled, todo.ai maintains a shadow copy and checksum of TODO.md, alerting users if the file is modified outside of todo.ai tools. This is an opt-in feature that helps maintain task consistency in collaborative or automated environments.

Several important bug fixes improve the overall experience. Subtask sorting now uses numerical comparison instead of alphabetical, ensuring task#10 appears after task#9 rather than after task#1. The restore command has been fixed to correctly position both root tasks and subtasks. A whitespace conflict between todo.ai and pre-commit hooks has been resolved, and UTF-8 encoding is now explicitly specified for Windows compatibility.

Documentation and developer experience have been enhanced with simplified Cursor rules that are more concise and actionable. The TODO.md visual standards have been implemented to ensure consistent formatting, and the tamper detection documentation clearly explains the feature as an optional integrity tool rather than a security mechanism.
