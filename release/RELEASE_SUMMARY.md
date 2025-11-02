# Release Summary

This release addresses a critical bug fix for the delete command section placement, ensuring that deleted tasks are properly organized in TODO.md files.

The main fix resolves issue #25 where the Deleted Tasks section could be incorrectly placed after the footer instead of before it. The updated `ensure_deleted_section()` function now properly checks for the footer boundary (`---`) before inserting or moving the Deleted Tasks section, guaranteeing the correct section order: Tasks → Recently Completed → Deleted Tasks → Footer. This fix also includes logic to automatically correct any existing incorrectly-positioned Deleted Tasks sections when they're detected.

Additionally, this release includes a new Cursor rule for bug review workflow, providing AI agents with clear guidelines on how to review GitHub bugs, create tasks with issue numbers, and format commits with both task and issue references. This improves the development workflow and ensures consistent bug tracking and resolution.

**Key improvements:**
- Fixed Deleted Tasks section placement bug (issue #25)
- Added automatic correction for incorrectly-positioned sections
- Added bug-review-workflow.mdc Cursor rule for standardized bug review process
