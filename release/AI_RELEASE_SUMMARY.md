This release streamlines the release workflow and day-to-day maintenance by
reducing unnecessary CI/CD runs while keeping full coverage for code changes
and tag-based releases. Docs and log changes now trigger focused checks,
improving turnaround without weakening release safeguards.

It also removes confirmation prompts for delete-note and update-note flows,
making note management faster and more scriptable, and fixes a checkbox parsing
edge case when modifying tasks so formatting stays consistent.
