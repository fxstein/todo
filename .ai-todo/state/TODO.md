# todo.ai ToDo List

> ⚠️ **MANAGED FILE**: Do not edit manually. Use `todo-ai` (CLI/MCP) or `todo.ai` to manage tasks.

## Tasks

- [ ] **#268** [AIT-3] Implement Empty Trash on Startup (Deleted Tasks) `#AIT-3` `#cleanup` `#feature` `#linear`
  > Linear issue: https://linear.app/fxstein/issue/AIT-3/implement-empty-trash-on-startup-deleted-tasks
  > Startup policy to permanently remove items from "Deleted Tasks" section.
  > - Target: Only items explicitly in the "Deleted Tasks" section
  > - Rule: Remove items older than 30 days (UPDATED from 7 days)
  > - Safety: Do NOT touch "Archived" tasks or active tasks
  > - Strictly an "Empty Trash" operation
  > Blocked by: AIT-2 (✅ complete)
  > Change Request (2026-01-29): Updated retention from 7 to 30 days to align with existing expires_at metadata.
  - [ ] **#268.6** Documentation: Update docs and examples `#documentation` `#inprogress`
  - [x] **#268.5** Verification: Verify empty trash behavior `#verification` (2026-01-29)
  - [x] **#268.4** Testing: Create unit and integration tests `#testing` (2026-01-29)
  - [x] **#268.3** Implementation: Add empty trash functionality `#implementation` (2026-01-29)
  - [x] **#268.2** Design: Create empty trash implementation plan `#design` (2026-01-29)
    > Create empty trash implementation plan addressing all open questions from analysis phase.
    > Design document: docs/design/empty_trash_design.md
  - [x] **#268.1** Analysis: Review deleted tasks section and prune implementation `#analysis` (2026-01-29)
    > Review existing work in task#129 and its subtasks to understand what was already planned. Analyze Linear issue requirements and identify gaps or changes needed. Document findings.
    > Analysis document: docs/design/empty_trash_analysis.md

- [ ] **#266** Design and implement full Linear integration `#cursor-rules` `#design` `#github` `#integration` `#linear`
  > End-to-end: (1) Assessment of current setup (including MCP tool payload verification). (2) Design implementation plan (data model, branching, security). (3) Implementation (Rules, Templates, Secrets). (4) Test & Docs.
  - [ ] **#266.5** Test and document the implementation `#documentation` `#verification`
    > Verify end-to-end flow. create a "Day 1" guide for new devs (How to start a task, how to PR).
  - [x] **#266.4** Implement: settings, Cursor rules, templates, GitHub `#implementation` (2026-01-29)
    > Implement approved design: .cursor/rules, .github/ workflows, and configure GitHub Repository Secrets (if required for Actions).
  - [x] **#266.3** Design: implementation plan for REVIEW `#design` `#review` (2026-01-29)
    > Draft detailed spec. Include: "The Life of a Ticket" flow diagram. STOP for human review.
    > Design doc: docs/linear_integration_design.md
  - [x] **#266.2** Best practices: branching, data model, and PR setup `#best-practices` `#design` (2026-01-29)
    > Define the "Data Model": How Linear Teams/Cycles map to GitHub Repos/Releases. Define Branch naming convention (`user/ID-desc`) and PR title standards.
    > Design doc: docs/linear_integration_design.md
  - [x] **#266.1** Assessment: document current Linear setup & MCP audit `#analysis` `#assessment` (2026-01-29)
    > Inventory current config (Linear workspace, GitHub integration). CRITICAL: Audit `linear` MCP tools to confirm they provide necessary fields (IDs, status, assignee) for automation.
    > Assessment doc: docs/linear_integration_assessment.md

- [ ] **#51** Add contributor section to release summary: list all contributors for each release `#feature`

- [ ] **#237** Future Enhancements Backlog - Post v3.0 features and improvements `#backlog` `#future` `#meta`
  - [ ] **#237.19** FUTURE: Add contributor section to releases (task#51) `#feature` `#future`
  - [ ] **#237.18** FUTURE: Enhance --lint command (task#127) `#feature` `#future`
  - [ ] **#237.17** FUTURE: Create git commit hook for linting (task#128) `#feature` `#future`
  - [ ] **#237.16** FUTURE: Implement --prune function (task#129) `#feature` `#future`
  - [ ] **#237.15** FUTURE: Implement feature request capability (task#47) `#feature` `#future`
  - [ ] **#237.14** FUTURE: Investigate cybersecurity implications (task#49) `#future` `#security`
  - [ ] **#237.13** FUTURE: Evaluate Gemini LLM integration (task#236) - v3.1  `#v3.1` `#future`

- [ ] **#236** Evaluate Gemini LLM integration for enhanced task management features (see docs/design/GEMINI_INTEGRATION_USE_CASES.md)  `#v3.1` `#enhancement`

---

## Archived Tasks
- [x] **#267** [AIT-2] Implement --prune function to remove archived tasks `#AIT-2` `#feature` `#linear` (2026-01-29)
  > Linear issue: https://linear.app/fxstein/issue/AIT-2
  > Migrated from task#129.
  > Implement prune functionality to remove old archived tasks from TODO.md based on git history analysis.
  > Key requirements:
  > - 30-day default retention period
  > - Task ID targeting options (--from-task)
  > - Git history analysis to identify archive dates
  > - CLI command with --days and --from-task options
  > - MCP server equivalent
  > Reuse existing work from task#129 where possible.
  - [x] **#267.9** Documentation: Update docs and help text `#documentation` (2026-01-29)
    > Update all relevant documentation:
    > - Add prune command to docs/cli.md
    > - Add prune_tasks tool to docs/mcp.md
    > - Update README.md with prune examples
    > - Add inline help text to CLI
    > - Update CHANGELOG.md
    > - Create usage examples in docs/examples/
  - [x] **#267.8** Verification: Run full test suite and linting `#verification` (2026-01-29)
    > Run complete verification:
    > - Run all unit tests: uv run pytest tests/unit/
    > - Run all integration tests: uv run pytest tests/integration/
    > - Run linting: uv run ruff check ai_todo/
    > - Verify no regressions in existing functionality
    > - Test manually with real TODO.md
  - [x] **#267.7** Testing: Integration tests `#testing` (2026-01-29)
    > Create integration tests in tests/integration/:
    > - Test CLI prune command end-to-end
    > - Test MCP prune_tasks tool
    > - Test with real git history scenarios
    > - Test --days and --from-task options
    > - Test MCP-CLI parity
  - [x] **#267.6** Testing: Unit tests `#testing` (2026-01-29)
    > Create comprehensive unit tests in tests/unit/:
    > - Test git history parsing
    > - Test date calculation logic
    > - Test task filtering
    > - Test edge cases (no git history, empty archives, etc.)
    > - Ensure 100% code coverage for new modules
  - [x] **#267.5** Implementation: MCP server integration `#implementation` (2026-01-29)
    > Add prune tool to MCP server in ai_todo/mcp/:
    > - Implement prune_tasks MCP tool
    > - Parameter validation
    > - Integration with core prune logic
  - [x] **#267.4** Implementation: CLI command `#implementation` (2026-01-29)
    > Add prune command to CLI in ai_todo/cli/:
    > - Add --prune command with --days and --from-task options
    > - Argument parsing and validation
    > - User confirmation prompts
    > - Output formatting
  - [x] **#267.3** Implementation: Core prune logic `#implementation` (2026-01-29)
    > Implement core prune functionality in ai_todo/core/ following approved design:
    > - Git history parser
    > - Archive date identification
    > - Task filtering and removal logic
    > - FileOps integration for safe TODO.md updates
  - [x] **#267.2** Design: Create prune function design document `#design` (2026-01-29)
    > Create comprehensive design document covering:
    > - Architecture and approach
    > - Git history analysis strategy
    > - CLI interface (--days, --from-task options)
    > - MCP server integration
    > - Edge cases and error handling
    > - Backwards compatibility
    > Design document: docs/design/prune_function_design.md
    > ⚠️ STOP FOR REVIEW - Do not proceed to implementation until design is approved.
  - [x] **#267.1** Analysis: Review existing task#129 and requirements `#analysis` (2026-01-29)
    > Review existing work in task#129 and its subtasks to understand what was already planned. Analyze Linear issue requirements and identify gaps or changes needed. Document findings.
    > Analysis document: docs/design/prune_function_analysis.md
- [x] **#129** Implement --prune function to remove old archived tasks based on git history `#feature` (2026-01-29)
  - [x] **#129.3** Add prune command with --days and --from-task options `#feature` (2026-01-29)
  - [x] **#129.2** Implement git history analysis to identify archive dates for tasks `#feature` (2026-01-29)
  - [x] **#129.1** Design prune function with 30-day default and task ID targeting options `#feature` (2026-01-29)
- [x] **#265** Add commit guideline to ai-todo–written Cursor rule `#cursor-rules` `#guidance` (2026-01-28)
  > Extend the Python code that writes the Cursor rule to `.cursor/rules/ai-todo-task-management.mdc` so the rule includes a commit guideline.
  > **Context:** The rule content is the string `AI_TODO_CURSOR_RULE` in `ai_todo/mcp/server.py`, written by `_init_cursor_rules()` when the rule file does not exist. We need to add this bullet to that rule text:
  > - **When committing:** If TODO.md or `.ai-todo/` have changes, always stage and commit them together (with other changes). They are versioned like the rest of the repo.
  > **Flow:** Design (and get approved) → Implement → Write tests → Verify.
  - [x] **#265.4** Verify: run tests and confirm rule output `#verification` (2026-01-28)
    > Run unit tests and manually confirm the generated .cursor/rules/ai-todo-task-management.mdc contains the new bullet and renders correctly.
  - [x] **#265.3** Write tests for new rule content `#testing` (2026-01-28)
    > Extend tests in tests/unit/test_cursor_rules.py to assert the written rule file contains the new commit guideline (e.g. “When committing”, “TODO.md”, “.ai-todo/”).
  - [x] **#265.2** Implement: extend AI_TODO_CURSOR_RULE in server.py `#implementation` (2026-01-28)
    > Add the commit guideline bullet to the rule string in ai_todo/mcp/server.py. Implement per approved design.
  - [x] **#265.1** Design: add commit bullet to rule content and get approval `#analysis` `#design` (2026-01-28)
    > Document where and how to add the commit guideline bullet to AI_TODO_CURSOR_RULE (wording, placement). Consider: existing installs already have the file (code only writes if missing)—document upgrade path or leave as "new installs only". Write design doc and link from this subtask; stop for human review and approval.
    > Design doc: docs/design/COMMIT_GUIDELINE_CURSOR_RULE_265.md
- [x] **#264** GitHub Issue #49: Archived tasks reappear under ## Tasks when adding new tasks    `#v4.0.1` `#bug` `#critical` `#file-ops` (2026-01-28)
  > Bug: When starting with TODO.md where Tasks section is empty but Archived/Recently Completed has many entries, creating new tasks causes some archived tasks (e.g., #79.3.x, #58.x) to incorrectly appear under Tasks. Environment: ai-todo v4.0.0b1, MCP via Cursor. Repro: https://gist.github.com/fxstein/19a43595ce66e9ca7ba624ad9f19b081
  - [x] **#264.9** Document: Close GitHub Issue #49 with fix reference `#documentation` (2026-01-28)
    > CLOSED: Posted fix summary on GitHub Issue #49 (https://github.com/fxstein/ai-todo/issues/49#issuecomment-3808303422) and closed issue as fixed.
  - [x] **#264.8** Test: Verify fix with user's TODO.md from gist `#testing` (2026-01-28)
    > VERIFIED: Tested with user's actual TODO.md from /Users/oratzes/cursor/ascii-guard/TODO.md. Before fix: orphan subtasks #79.3.7, #79.3.5, #58.1-58.7 leaked into Tasks section. After fix: only new task appears in Tasks section, all archived content stays in Archived Tasks.
  - [x] **#264.7** Test: Create unit tests for empty Tasks section with archived content `#testing` (2026-01-28)
    > ADDED: test_issue_49_orphan_subtasks_stay_in_archived_section() in test_archive_subtasks.py. Tests that incomplete subtasks [ ] under archived parents [x] stay in Archived section when adding new tasks. Validates fix for GitHub Issue #49.
  - [x] **#264.6** Implement: Ensure tasks stay in their original sections when writing `#implementation` (2026-01-28)
    > VERIFIED: With fix to status determination, tasks now stay in their original sections during write. ARCHIVED tasks go to Archived Tasks section regardless of checkbox. Write logic in _generate_markdown routes by status which is now correctly set during parse.
  - [x] **#264.5** Implement: Fix section parsing to respect task section membership `#implementation` (2026-01-28)
    > FIXED: Modified _parse_markdown lines 647-668 to determine status based on section first, then checkbox. Tasks in 'Recently Completed' or 'Archived Tasks' sections are now ARCHIVED regardless of checkbox state. This prevents orphan subtasks with [ ] from leaking into Tasks section.
  - [x] **#264.4** Design: Document fix approach for section boundary handling `#design` (2026-01-28)
    > FIX APPROACH: Section takes precedence over checkbox for status determination. Changed order in _parse_markdown: (1) check section first, (2) if archived section → ARCHIVED, (3) if deleted section → DELETED, (4) only then check checkbox for COMPLETED in Tasks section.
  - [x] **#264.3** Analyze: Identify how tasks get moved between sections during write operations `#analysis` (2026-01-28)
    > ROOT CAUSE FOUND: In _parse_markdown lines 648-666, status determination only considers section for [x] checkboxes. Tasks with [ ] stay PENDING even when in 'Recently Completed' section. Fix: section should override checkbox for status determination - if task is in archived section, status=ARCHIVED regardless of checkbox.
  - [x] **#264.2** Analyze: Trace file_ops.py parsing of non-standard sections (Recently Completed vs Archived Tasks) `#analysis` (2026-01-28)
    > ANALYZED: Code properly handles 'Recently Completed' as a valid TASK_SECTION (line 438, 804). Tasks in this section with [x] get TaskStatus.ARCHIVED (line 652-655). Section is converted to 'Archived Tasks' on write. The code path is correct - unable to identify how tasks could leak into the Tasks section. The gist shows non-standard output format which suggests either a different tool or an edge case we haven't identified.
  - [x] **#264.1** Investigate: Reproduce bug with empty Tasks section and archived tasks `#research` (2026-01-28)
    > REPRODUCED! With user's original TODO.md from ascii-guard: (1) Empty Tasks section, (2) Recently Completed has parent tasks with incomplete subtasks (e.g., #58 with [~] has subtasks #58.1-58.7 with [ ], #79 with [x] has subtasks #79.3.5, #79.3.7 with [ ]). After adding new task #94, orphan subtasks appear under Tasks section. Root cause: subtask status based on checkbox [ ] not parent's section/status.
- [x] **#263** Design task metadata persistence for timestamps (created_at, updated_at, completed_at)    `#v3.1` `#design` `#enhancement` `#metadata` (2026-01-27)
  > MCP resources revealed that task timestamps (created_at, updated_at, completed_at) are not being persisted. Currently generated at parse-time rather than stored. Need to design metadata storage that persists these values across sessions.
  - [x] **#263.8** Document: Update TODO.md format documentation `#documentation` (2026-01-27)
    > Document: Update TODO.md format documentation
    > > SKIPPED: Format is self-documenting via comment in TASK_METADATA block.
  - [x] **#263.7** Verify: Confirm MCP resources return accurate timestamps `#verification` (2026-01-27)
  - [x] **#263.6** Test: Create unit tests for metadata persistence `#testing` (2026-01-27)
    > Test: Create unit tests for metadata persistence
    > > DONE: Added 6 tests covering timestamp parsing, roundtrip, and backfill behavior.
  - [x] **#263.5** Implement: Update parser to read persisted metadata `#implementation` (2026-01-27)
    > Implement: Update parser to read persisted metadata
    > > DONE: Added parsing for <!-- TASK_METADATA ... --> block, applied timestamps to Task objects after parsing.
  - [x] **#263.4** Implement: Add metadata storage to file_ops write operations `#implementation` (2026-01-27)
    > Implement: Add metadata storage to file_ops write operations
    > > DONE: Added task_timestamps dict, TASK_METADATA comment block writing in _generate_markdown, and backfill_timestamps() helper.
  - [x] **#263.3** Design: Create metadata persistence design document with storage format and migration strategy `#design` (2026-01-27)
    > Design: Create metadata persistence design document with storage format and migration strategy
    > > APPROVED: Hybrid (Option C + inline dates) with lazy backfilling on mutations. No migration scripts. See docs/task-metadata-design.md
  - [x] **#263.2** Analyze: Identify storage options (inline markdown, separate metadata file, hidden comments) `#analysis` (2026-01-27)
    > Analyze: Identify storage options (inline markdown, separate metadata file, hidden comments)
    > > DONE: Analyzed 3 options based on existing patterns (inline dates, metadata.json, HTML comments). Ready for design document.
  - [x] **#263.1** Investigate: Audit current timestamp handling in Task dataclass and file_ops `#research` (2026-01-27)
    > Investigate: Audit current timestamp handling in Task dataclass and file_ops
    > > DONE: Found that created_at/updated_at use datetime.now() at parse-time (not persisted). completed_at is approximated. Only deleted_at/expires_at are properly persisted in markdown.
- [x] **#262** GitHub Issue #48: Expose task lists as MCP resources for IDE integration    `#v3.1` `#enhancement` `#github-issue` `#mcp` (2026-01-27)
  > GitHub Issue #48: Expose task lists as MCP resources for IDE integration `#v3.1` `#enhancement` `#github-issue` `#mcp`
  > > COMPLETE: Implemented Option A (Minimal Set) with 4 resources: tasks://open, tasks://active, tasks://{id}, config://settings. Added unit tests and documentation. GitHub issue #48 closed.
  - [x] **#262.12** Document: Update MCP documentation and close GitHub issue #48 `#documentation` (2026-01-27)
    > Document: Update MCP documentation and close GitHub issue #48
    > > DONE: Updated docs/user/MCP_SETUP.md with resources section. Closed GitHub issue #48.
  - [x] **#262.11** Verify: Test resources in Cursor IDE with MCP Inspector `#verification` (2026-01-27)
    > Verify: Test resources in Cursor IDE with MCP Inspector
    > > READY FOR MANUAL VERIFICATION: Reload MCP server and check that resources (tasks://open, tasks://active, tasks://{id}, config://settings) appear in inspector.
  - [x] **#262.10** Test: Create integration tests for resource subscriptions and change notifications `#testing` (2026-01-27)
  - [x] **#262.9** Test: Create unit tests for MCP resource handlers `#testing` (2026-01-27)
    > Test: Create unit tests for MCP resource handlers
    > > DONE: Created tests/unit/test_mcp_resources.py with 9 tests for task-to-dict and data helper functions.
  - [x] **#262.8** Implement: Add notify_resource_changed() calls to task mutation tools `#implementation` (2026-01-27)
  - [x] **#262.7** Implement: Add config://settings resource for ai-todo configuration `#implementation` (2026-01-27)
  - [x] **#262.6** Implement: Add tasks://{id} dynamic resource for individual task details `#implementation` (2026-01-27)
  - [x] **#262.5** Implement: Add tasks://active resource for in-progress tasks `#implementation` (2026-01-27)
  - [x] **#262.4** Implement: Add tasks://open resource (pending + in-progress tasks) `#implementation` (2026-01-27)
    > Implement: Add tasks://open resource (pending + in-progress tasks)
    > > DONE: Added @mcp.resource('tasks://open') returning JSON with root tasks, subtask counts, and metadata.
  - [x] **#262.3** Design: Create MCP resources design document with URI schema and change notification strategy `#design` (2026-01-27)
    > Design: Create MCP resources design document with URI schema and change notification strategy
    > > APPROVED: Option A (Minimal Set) - tasks://open, tasks://active, tasks://{id}, config://settings. Built-in notifications only. See docs/mcp-resources-design.md
  - [x] **#262.2** Analyze: Identify resource URIs and data structures for task lists `#analysis` (2026-01-27)
    > Analyze: Identify resource URIs and data structures for task lists
    > > DONE: Task dataclass has id, description, status, tags, notes, timestamps. Status: PENDING, COMPLETED, ARCHIVED, DELETED. IN_PROGRESS tracked via #inprogress tag. Resources should return JSON (not markdown) for better client integration.
  - [x] **#262.1** Investigate: Research FastMCP resource patterns and subscription capabilities `#research` (2026-01-27)
    > Investigate: Research FastMCP resource patterns and subscription capabilities
    > > DONE: FastMCP uses @mcp.resource() decorator with URI-based addressing. Supports static resources and dynamic templates with {param} placeholders. Change notifications via automatic list_changed events.
- [x] **#261** Implement batch operations for task state commands `#api` `#batch-operations` `#enhancement` (2026-01-27)
  > Add batch support (one or list of task IDs) to complete, archive, delete, and restore commands. Ensure consistent API across CLI and MCP.
  - [x] **#261.7** Document: Update API docs and CLI help for batch operations (2026-01-27)
    > CLI help updated (shows TASK_IDS...). Design doc at docs/batch-operations-design.md
  - [x] **#261.6** Verify: End-to-end validation of batch operations (2026-01-27)
    > Full test suite: 241 passed. CLI and MCP batch operations verified.
  - [x] **#261.5** Test: Create unit and integration tests for batch operations (2026-01-27)
    > Updated test_mcp_cli_parity.py to use task_ids: list[str]. All 241 tests pass.
  - [x] **#261.4** Implement: Add batch support to restore CLI command (2026-01-27)
    > Updated restore CLI command to accept multiple task IDs via nargs=-1, refactored restore_command to accept list[str]
  - [x] **#261.3** Implement: Add batch support to MCP tools (2026-01-27)
    > Updated complete_task, delete_task, archive_task, restore_task MCP tools to accept task_ids: list[str]
  - [x] **#261.2** Design: Create design document for batch operations API (2026-01-27)
    > APPROVED: Option A - task_ids: list[str] (1 to n items). See docs/batch-operations-design.md
  - [x] **#261.1** Investigate: Audit current batch support in CLI, MCP, and core (2026-01-27)
- [x] **#260** GitHub Issue #29: Add .cursorignore files for secrets/sensitive content `#enhancement` `#github-issue` `#security` (2026-01-27)
  > GitHub Issue #29: Add .cursorignore files for secrets/sensitive content `#enhancement` `#github-issue` `#security`
  > > COMPLETE: Implemented Option A (Minimal Security Focus). Updated .cursorignore to protect tamper detection state. Added security best practices docs. GitHub issue #29 closed.
  - [x] **#260.7** Document: Add security best practices docs and close GitHub issue #29 (2026-01-27)
    > Document: Add security best practices docs and close GitHub issue #29
    > > DONE: Created docs/guides/SECURITY_BEST_PRACTICES.md, updated docs/README.md index, closed GitHub issue #29.
  - [x] **#260.6** Verify: Confirm sensitive content is not exposed to AI agents (2026-01-27)
    > Verify: Confirm sensitive content is not exposed to AI agents
    > > VERIFIED: .cursorignore blocks Cursor AI features (Tab, inline edit, @ refs) from state/. Note: MCP tools bypass .cursorignore by design - this is expected and necessary for ai-todo to function.
  - [x] **#260.5** Test: Verify ignore patterns work correctly in Cursor (2026-01-27)
    > Test: Verify ignore patterns work correctly in Cursor
    > > VERIFIED: .cursorignore patterns use valid gitignore syntax. Protected directories exist and contain sensitive files (checksum, tamper_mode, shadow TODO.md).
  - [x] **#260.4** Implement: Add .cursorignore file with recommended patterns (2026-01-27)
  - [x] **#260.3** Decide: Define default ignore patterns and user customization options (2026-01-27)
    > AWAITING APPROVAL: Select Option A, B, or C from docs/cursorignore-design.md
  - [x] **#260.2** Analyze: Identify sensitive files/patterns that should be ignored (2026-01-27)
    > See docs/cursorignore-design.md for analysis
  - [x] **#260.1** Investigate: Research .cursorignore format and best practices for secrets (2026-01-27)
- [x] **#259** GitHub Issue #30: Evaluate MCP server benefits over CLI `#github-issue` `#investigation` `#mcp` (2026-01-27)
  > IMPLEMENTED in v3.0.0: MCP server fully implemented with CLI parity. Close GitHub issue #30.
  - [x] **#259.8** Close GitHub issue #30 as implemented in v3.0.0 (2026-01-27)
  - [x] **#259.7** Document: Update MCP documentation and close GitHub issue #30 (2026-01-27)
  - [x] **#259.6** Verify: Validate MCP/CLI parity and integration quality (2026-01-27)
  - [x] **#259.5** Test: Ensure MCP server has comprehensive test coverage (2026-01-27)
  - [x] **#259.4** Implement: Address any identified MCP enhancement opportunities (2026-01-27)
  - [x] **#259.3** Decide: Close issue if complete, or identify remaining enhancements (2026-01-27)
  - [x] **#259.2** Analyze: Document MCP benefits realized vs original issue expectations (2026-01-27)
  - [x] **#259.1** Investigate: Review GitHub issue #30 and current MCP server implementation (2026-01-27)
- [x] **#258** GitHub Issue #31: Investigate Cursor CLI and Shell Commands `#cursor-integration` `#github-issue` `#investigation` (2026-01-27)
  > COMPLETE: ai-todo already integrates with Cursor via MCP. Cursor CLI provides: (1) `cursor agent` for terminal AI with MCP support, (2) `cursor agent mcp list/list-tools/enable/disable` for server management, (3) `cursor --add-mcp` for programmatic setup. No additional integration work needed. Close GitHub issue #31.
  - [x] **#258.8** Close GitHub issue #31 as complete - ai-todo MCP integration already works with Cursor CLI (2026-01-27)
  - [x] **#258.7** Document: Update docs with Cursor integration guide, close GitHub issue #31 (2026-01-27)
  - [x] **#258.6** Verify: Test integration in real Cursor environment (2026-01-27)
  - [x] **#258.5** Test: Create tests for Cursor CLI integration (2026-01-27)
  - [x] **#258.4** Implement: Build Cursor CLI integration features (2026-01-27)
  - [x] **#258.3** Decide: Determine which integrations provide most value (2026-01-27)
  - [x] **#258.2** Analyze: Identify integration opportunities between ai-todo and Cursor CLI (2026-01-27)
  - [x] **#258.1** Investigate: Research Cursor CLI features and shell command capabilities (2026-01-27)
- [x] **#257** GitHub Issue #33: Enhanced bug reporting with duplicate detection and privacy `#developer-experience` `#enhancement` `#github-issue` (2026-01-27)
  > WON'T IMPLEMENT: Use native GitHub bug reporting instead of building custom tooling. Close GitHub issue #33.
  - [x] **#257.8** Close GitHub issue #33 as won't implement - use native GitHub bug reporting (2026-01-27)
  - [x] **#257.7** Document: Update CLI help and docs, close GitHub issue #33 (2026-01-27)
  - [x] **#257.6** Verify: Test with real bug scenarios and private repo simulation (2026-01-27)
  - [x] **#257.5** Test: Create tests for bug reporting enhancements (2026-01-27)
  - [x] **#257.4** Implement: Add duplicate detection and privacy mode features (2026-01-27)
  - [x] **#257.3** Decide: Design API for enhanced bug reporting options (2026-01-27)
  - [x] **#257.2** Analyze: Prioritize features (duplicate detection, privacy, metadata, suggestions) (2026-01-27)
  - [x] **#257.1** Investigate: Review GitHub issue #33 and current report-bug implementation (2026-01-27)
- [x] **#256** GitHub Issue #34: Smart installer with bash/zsh auto-detection `#enhancement` `#github-issue` `#installer` (2026-01-27)
  > WON'T FIX: Shell installer no longer relevant since v3.0.0 moved to Python with uv/pipx installation. Legacy shell scripts are frozen and no longer receive updates. Close GitHub issue #34.
  - [x] **#256.8** Close GitHub issue #34 as won't fix - no longer relevant since v3.0.0 (2026-01-27)
  - [x] **#256.7** Document: Update installation docs and close GitHub issue #34 (2026-01-27)
  - [x] **#256.6** Verify: Test installer on macOS, Linux, and Windows environments (2026-01-27)
  - [x] **#256.5** Test: Create tests for installer across different OS/shell combinations (2026-01-27)
  - [x] **#256.4** Implement: Create smart installer with OS/shell auto-detection (2026-01-27)
  - [x] **#256.3** Decide: Design installer architecture and shell detection strategy (2026-01-27)
  - [x] **#256.2** Analyze: Evaluate bash vs zsh performance and compatibility requirements (2026-01-27)
  - [x] **#256.1** Investigate: Review GitHub issue #34 and existing installer research docs (2026-01-27)
- [x] **#255** GitHub Issue #39: Python-based MCP server with pipx installation `#architecture` `#enhancement` `#github-issue` (2026-01-27)
  > IMPLEMENTED in v3.0.0: Python-based ai-todo with dual interfaces (MCP server + CLI), shared core logic in ai_todo.core, and uv/pipx installation support. Close GitHub issue #39.
  - [x] **#255.8** Close GitHub issue #39 as implemented in v3.0.0 (2026-01-27)
  - [x] **#255.7** Document: Update README, docs, and close GitHub issue #39 (2026-01-27)
  - [x] **#255.6** Verify: Run full test suite and validate implementation (2026-01-27)
  - [x] **#255.5** Test: Create/update tests for any new functionality (2026-01-27)
  - [x] **#255.4** Implement: Address any remaining requirements (2026-01-27)
  - [x] **#255.3** Decide: Determine remaining gaps and next steps (or close issue if complete) (2026-01-27)
  - [x] **#255.2** Analyze: Compare current codebase against issue requirements (2026-01-27)
  - [x] **#255.1** Investigate: Review GitHub issue #39 details and current implementation status (2026-01-27)
- [x] **#254** Freeze legacy shell scripts and remove from test comparisons `#cleanup` `#legacy` `#testing` (2026-01-27)
  > Implemented: (1) Added FROZEN header with date and reason to legacy/todo.ai and todo.bash, (2) Deleted parity test files (test_feature_parity.py, test_dataset_parity.py, compare_outputs.py, test_show_root_shell.py), (3) Rewrote TEST_PLAN.md for Python-only testing, (4) CI runs pytest which now excludes deleted tests, (5) Release script references kept intentionally - scripts are frozen but still distributed for backward compatibility.
  - [x] **#254.6** Remove legacy script references from release scripts (release.sh, etc.) (2026-01-27)
  - [x] **#254.5** Update CI workflow to skip legacy comparison tests (2026-01-27)
  - [x] **#254.4** Update TEST_PLAN.md to reflect Python-only testing strategy (2026-01-27)
  - [x] **#254.3** Remove test_show_root_shell.py (shell-based show command tests) (2026-01-27)
  - [x] **#254.2** Remove shell script parity tests (test_feature_parity.py, test_dataset_parity.py, compare_outputs.py) (2026-01-27)
  - [x] **#254.1** Mark legacy/ scripts as frozen (add header comment with freeze date and reason) (2026-01-27)
- [x] **#253** Standardize API terminology to follow industry conventions (title/description) `#api` `#breaking-change` `#enhancement` (2026-01-27)
  > DEPENDENCY: Complete #254 (freeze legacy scripts) before starting implementation phase (#253.4+)
  > ANALYSIS: See docs/api-terminology-analysis.md for full audit, research, and design proposal.
  - [x] **#253.11** Update CHANGELOG with breaking change notes (2026-01-27)
  - [x] **#253.10** Run full test suite and verify no regressions (2026-01-27)
  - [x] **#253.9** Update all documentation (README, docs/, cursor rules) (2026-01-27)
  - [x] **#253.8** Update integration and e2e tests (2026-01-27)
  - [x] **#253.7** Create/update unit tests for renamed parameters (2026-01-27)
  - [x] **#253.6** Update core functions and internal APIs (2026-01-27)
  - [x] **#253.5** Update CLI commands with new parameter names (2026-01-27)
  - [x] **#253.4** Update MCP server tools (server.py) with new parameter names (2026-01-27)
  - [x] **#253.3** Design new naming standard with mapping table (old → new) - WAIT FOR APPROVAL (2026-01-27)
  - [x] **#253.2** Research industry standards: GitHub Issues, Jira, Linear, Todoist APIs for terminology (2026-01-27)
  - [x] **#253.1** Audit all current parameter names across MCP tools, CLI commands, and core functions (2026-01-27)
- [x] **#251** Debug and fix MCP server restart functionality in Cursor `#bug` `#mcp` (2026-01-27)
  - [x] **#251.8** Document restart behavior and any limitations (2026-01-27)
  - [x] **#251.7** Test restart across multiple scenarios (dev mode, after updates) (2026-01-27)
  - [x] **#251.6** Implement working restart solution (2026-01-27)
    > SOLUTION: Use sys.exit() instead of os._exit()
    > - os._exit() bypasses Python cleanup handlers, preventing Cursor from detecting proper shutdown
    > - sys.exit() allows cleanup to run, enabling Cursor to restart the server correctly
    > - Also flush stdout/stderr before exit and use 0.5s delay
    > - Exit code 1 (error) didn't matter - the key was sys.exit() vs os._exit()
  - [x] **#251.5** Investigate Cursor MCP logs to understand reconnection behavior (2026-01-27)
  - [x] **#251.4** Test alternative exit strategies: sys.exit() vs os._exit(), various delays (2026-01-27)
  - [x] **#251.3** Try non-zero exit code (simulate crash) to trigger different Cursor restart mechanism (2026-01-27)
  - [x] **#251.2** Ensure response is fully sent before exit - verify threading/async behavior (2026-01-27)
  - [x] **#251.1** Analyze current restart behavior - server exits but Cursor reconnects with 0 tools (2026-01-27)
    > Current behavior observed:
    > - restart() tool returns "Restarting MCP server..."
    > - 0.5s later, os._exit(0) is called
    > - Cursor log shows "Client closed for command"
    > - Cursor reconnects: "Connected to stdio server, fetching offerings"
    > - But reports "Found 0 tools, 0 prompts, and 0 resources"
    > - Server code is correct - 30 tools register when run directly via `uv run`
    > - Issue appears to be Cursor-specific with how it handles MCP process restarts
- [x] **#250** Improve update command for development mode - skip version checks and provide direct restart capability `#dev-experience` `#enhancement` `#mcp` (2026-01-27)
  > CONTEXT: In dev mode, version numbers are irrelevant - developers iterate on the same version many times. The update command should recognize this and provide a streamlined restart experience without unnecessary version checks or 'already up to date' messages.
  > CLARIFICATION: CLI is one-shot (no restart concept). Only MCP server needs restart capability. Focus on: (1) dedicated `restart` MCP tool for dev quick-reload, (2) improve `update` tool messaging in dev mode.
  - [x] **#250.12** Docs: Update development workflow documentation with restart usage `#documentation` (2026-01-27)
  - [x] **#250.11** Verify: Test restart functionality in live dev environment `#verification` (2026-01-27)
    > Live test: Use 'restart' tool in Cursor to verify MCP server restarts and picks up code changes.
  - [x] **#250.10** Test: Unit tests for dev mode detection and restart behavior `#testing` (2026-01-27)
  - [x] **#250.9** Implement: Add CLI restart command for development workflow `#implementation` (2026-01-27)
  - [x] **#250.8** Implement: Modify check_update to show dev-appropriate messaging `#implementation` (2026-01-27)
  - [x] **#250.7** Implement: Add restart MCP tool for dev mode quick reload `#implementation` (2026-01-27)
  - [x] **#250.6** Design: Consider CLI flags for dev workflow (--restart-only, --force) `#design` (2026-01-27)
  - [x] **#250.5** Design: Plan MCP tool API - add restart tool or modify update tool for dev mode `#design` (2026-01-27)
    > DESIGN: Add dedicated `restart` MCP tool - zero version logic, just triggers server restart. Keep `update` for production use, but improve its dev mode behavior.
  - [x] **#250.4** Design: Define dev mode update behavior - skip version check, offer restart-only option `#design` (2026-01-27)
    > DESIGN: In dev mode, skip version checks entirely. Provide direct restart with message 'Restarting MCP server to pick up code changes...'
  - [x] **#250.3** Analyze: Review how other dev tools handle hot-reload/restart patterns `#analysis` (2026-01-27)
  - [x] **#250.2** Analyze: Identify use cases - version check vs simple restart vs git pull + restart `#analysis` (2026-01-27)
    > Use cases: (1) Simple restart - pick up code changes without any version checks, (2) Update+restart - for production installs. In dev mode, only #1 matters.
  - [x] **#250.1** Analyze: Review current update command behavior in dev mode `#analysis` (2026-01-27)
    > Current behavior: `check_update` shows 'Running in development mode at version X (latest: X)' - version comparison is irrelevant in dev. `update` in dev mode suggests git pull but the restart capability is what developers actually want.
- [x] **#247** Investigate and fix GitHub task number coordination - last sync was 2 days ago (Issue #23) `#bug` `#coordination` `#github` (2026-01-27)
  > CONTEXT: GitHub Issue #23 (https://github.com/fxstein/ai-todo/issues/23) is used for atomic task number coordination across multiple contributors. Last update was 2 days ago, suggesting v3 refactor may have broken the coordination sync.
  > CONFIRMED ROOT CAUSE: GitHubClient has get_issue_comments() but NO create_issue_comment() method. The Python code can READ the latest task number from Issue #23 but cannot WRITE back after creating a task. The shell script had this capability but it was not ported to Python.
  - [x] **#247.13** Docs: Update coordination setup documentation if needed `#documentation` (2026-01-27)
  - [x] **#247.12** Verify: Create test task and confirm Issue #23 is updated `#verification` (2026-01-27)
    > MANUAL VERIFICATION NEEDED: After commit, create a test task and verify GitHub Issue #23 receives the 'Next task number: X' comment.
  - [x] **#247.11** Test: Integration test verifying GitHub Issue update on task creation `#testing` (2026-01-27)
  - [x] **#247.10** Test: Unit tests for coordination module integration `#testing` (2026-01-27)
  - [x] **#247.9** Implement: Ensure GitHub Issue #23 gets updated on task number changes `#implementation` (2026-01-27)
  - [x] **#247.8** Implement: Fix coordination calls in task creation/modification paths `#implementation` (2026-01-27)
  - [x] **#247.7** Design: Plan fix for coordination integration with Python task manager `#design` (2026-01-27)
  - [x] **#247.6** Diagnose: Check if coordination mode is enabled and GitHub token is configured `#diagnosis` (2026-01-27)
  - [x] **#247.5** Diagnose: Compare v3 refactor changes that may have affected coordination calls `#diagnosis` (2026-01-27)
  - [x] **#247.4** Analyze: Trace task creation flow to identify where coordination should trigger `#analysis` (2026-01-27)
  - [x] **#247.3** Analyze: Check GitHub Issue #23 for last successful coordination update `#analysis` (2026-01-27)
  - [x] **#247.2** Analyze: Review coordination.py implementation and GitHub client logic `#analysis` (2026-01-27)
    > ROOT CAUSE FOUND: GitHubClient is missing `create_issue_comment` method. coordination.py only READS from Issue #23 but never WRITES back the new task number after creating a task.
  - [x] **#247.1** Analyze: Review current coordination settings in .ai-todo/config.yaml `#analysis` (2026-01-27)
    > FINDING: mode is 'single-user' but coordination.type is 'github-issues' with issue_number 23. Mode may need to be 'enhanced' for coordination to trigger.
    > CORRECTION: Single-user mode DOES support coordination via github-issues - the `_generate_single_user_id` method checks coordination.type. The config is correct.
- [x] **#246** Investigate reorder command not reordering archived tasks `#archive` `#bug` `#reorder` (2026-01-27)
  > CAUTION: May be false positive caused by IDE window refresh delays. Verify actual bug before implementing fixes. Start with analysis and test review.
  > VERIFIED: Not a bug. Testing confirms reorder correctly reorders archived tasks. Original observation was IDE refresh delay.
  - [x] **#246.11** Docs: Update reorder command help text to mention all sections are processed `#documentation` (2026-01-27)
  - [x] **#246.10** Verify: Run reorder on live TODO.md and confirm archived tasks are properly ordered `#verification` (2026-01-27)
  - [x] **#246.9** Test: Integration tests verifying reorder fixes out-of-order archived tasks `#testing` (2026-01-27)
  - [x] **#246.8** Test: Unit tests for reorder affecting archived tasks `#testing` (2026-01-27)
    > REVIEW: Existing test_reorder_command.py only covers active tasks. Should add test for archived task ordering.
  - [x] **#246.7** Implement: Ensure archived/deleted sections use order_tasks_with_hierarchy for parent-subtask grouping `#implementation` (2026-01-27)
  - [x] **#246.6** Implement: Update reorder logic to process all sections (Tasks, Archived, Deleted) `#implementation` (2026-01-27)
  - [x] **#246.5** Design: Plan fix to extend reorder to archived/deleted sections with proper hierarchy ordering `#design` (2026-01-27)
  - [x] **#246.4** Design: Determine expected behavior - should archived/deleted sections also be reordered? `#design` (2026-01-27)
    > Expected behavior confirmed: reorder processes all sections. _generate_markdown calls order_tasks_with_hierarchy for archived/deleted during every write.
  - [x] **#246.3** Analyze: Reproduce the bug - verify archived tasks remain out of order after reorder `#analysis` `#testing` (2026-01-27)
  - [x] **#246.2** Analyze: Identify which sections reorder currently processes (Tasks only? Archived? Deleted?) `#analysis` (2026-01-27)
  - [x] **#246.1** Analyze: Review current reorder command implementation in cli and core `#analysis` (2026-01-27)
- [x] **#245** Add version pinning and maximum version constraints to self-update feature (builds on #241) `#feature` `#mcp` `#update` (2026-01-27)
  > DESIGN: Two deployment modes with different constraint sources:
  > - Project-local (uv add ai-todo): Use pyproject.toml constraints (uv handles automatically)
  > - System-global (uv tool install): Use ~/.config/ai-todo/config.yaml for version constraints
  > DESIGN: Global config location follows uv pattern (~/.config/uv/uv.toml):
  > - Linux/macOS: ~/.config/ai-todo/config.yaml
  > - Windows: %APPDATA%\ai-todo\config.yaml
  > - XDG override: $XDG_CONFIG_HOME/ai-todo/config.yaml
  > DESIGN: Constraint precedence (highest to lowest):
  > 1. CLI flags (--version=X.Y.Z)
  > 2. Project pyproject.toml (if ai-todo is a dependency)
  > 3. User-level ~/.config/ai-todo/config.yaml (for global installs)
  > 4. Built-in default (upgrade to latest)
  > DESIGN: Use PEP 440 version specifiers (same as pyproject.toml):
  > - Pin exact: version_constraint: "==3.0.2"
  > - Min+max: version_constraint: ">=3.0.0,<4.0.0" (like fastmcp in this repo)
  > - Minimum only: version_constraint: ">=3.0.0"
  > DESIGN: Version mismatch warning for global installs:
  > - On MCP startup, check if project has ai-todo in pyproject.toml
  > - If global version doesn't satisfy project's constraint, emit warning
  > - Example: "Warning: Global ai-todo 4.1.0 doesn't match project constraint >=3.0.0,<4.0.0"
  > - Suggest: "Consider using project-local install: uv add ai-todo"
  > IMPLEMENTATION: MCP protocol safety - all warnings MUST use stderr (file=sys.stderr), never stdout. MCP uses stdout for JSON-RPC; any raw text to stdout corrupts the protocol stream.
  - [x] **#245.13** Implement: Add startup warning when global install version mismatches project pyproject.toml constraint (2026-01-27)
  - [x] **#245.12** Implement: Extend updater.py to check constraints before performing update (2026-01-27)
  - [x] **#245.11** Docs: Document version constraint configuration options in user guide (2026-01-27)
  - [x] **#245.10** Test: Integration tests for update with max_version constraint (should cap at boundary) (2026-01-27)
  - [x] **#245.9** Test: Integration tests for update with pinned version (should skip upgrade) (2026-01-27)
  - [x] **#245.8** Test: Unit tests for version constraint parsing and comparison logic (2026-01-27)
  - [x] **#245.7** Implement: Update MCP check_update/update tools to respect version constraints (2026-01-27)
  - [x] **#245.6** Implement: Add CLI commands for setting/viewing version constraints (ai-todo config update.pin-version) (2026-01-27)
  - [x] **#245.5** Implement: Add version constraint fields to config schema and loader (2026-01-27)
  - [x] **#245.4** Design: Plan update behavior with constraints (skip if pinned, cap at max_version, warn on constraint violations) (2026-01-27)
  - [x] **#245.3** Design: Define version constraint schema for config.yaml (pinned_version, max_version, allow_prerelease) (2026-01-27)
  - [x] **#245.2** Analyze: Investigate how other tools handle version locks (e.g., uv.lock, pip-tools, poetry.lock) (2026-01-27)
  - [x] **#245.1** Analyze: Research uv/pip version specifier patterns (==, <=, <, ~=, ^) and common ecosystem practices (2026-01-27)
- [x] **#242** Investigate archive/delete task ordering bug - root task appears below subtasks `#bug` `#file-ops` (2026-01-27)
  - [x] **#242.11** Docs: Document fix if behavior change affects user expectations (2026-01-27)
  - [x] **#242.10** Test: Run full test suite to verify no regressions (2026-01-27)
  - [x] **#242.9** Test: Add unit tests for delete ordering with parent and subtasks (2026-01-27)
  - [x] **#242.8** Test: Add unit tests for archive ordering with parent and subtasks (2026-01-27)
  - [x] **#242.7** Implement: Fix task ordering in delete operation (if affected) (2026-01-27)
  - [x] **#242.6** Implement: Fix task ordering in archive operation (2026-01-27)
  - [x] **#242.5** Design: Define correct archive/delete ordering (root task first, then subtasks) (2026-01-27)
  - [x] **#242.4** Analyze: Check if legacy shell script has same behavior or handles ordering differently (2026-01-27)
  - [x] **#242.3** Analyze: Trace archive/delete code path in file_ops.py to identify root cause (2026-01-27)
  - [x] **#242.2** Analyze: Verify if delete operation has the same ordering issue (2026-01-27)
  - [x] **#242.1** Analyze: Reproduce archive ordering issue with root task and subtasks (2026-01-27)
- [x] **#241** Implement self-update feature via uv with MCP server graceful shutdown `#feature` `#mcp` (2026-01-27)
  > REQUIREMENT: Must detect developer environment (running from live repo vs installed package). In dev mode, skip uv upgrade but still support restart to pick up code changes.
  - [x] **#241.12** Docs: Add troubleshooting section for update failures and rollback (2026-01-27)
  - [x] **#241.11** Docs: Document self-update feature in README and user guide (2026-01-27)
  - [x] **#241.10** Test: Verify graceful shutdown signals pending operations to complete (2026-01-27)
  - [x] **#241.9** Test: Integration tests for MCP update tool with mocked uv commands (2026-01-27)
  - [x] **#241.8** Test: Unit tests for version comparison and update detection logic (2026-01-27)
  - [x] **#241.7** Implement: Add CLI `ai-todo update` command for manual updates (2026-01-27)
  - [x] **#241.6** Implement: Add graceful shutdown mechanism for MCP server after update completes (2026-01-27)
  - [x] **#241.5** Implement: Create `update` MCP tool that triggers uv upgrade subprocess (2026-01-27)
  - [x] **#241.4** Implement: Add version check against PyPI to detect available updates (2026-01-27)
  - [x] **#241.3** Design: Determine graceful shutdown strategy for MCP server (signal handling, cleanup) (2026-01-27)
  - [x] **#241.2** Design: Define update workflow (check version, download, shutdown, restart by host) (2026-01-27)
  - [x] **#241.1** Design: Research uv self-update mechanisms and MCP server shutdown patterns (2026-01-27)
- [x] **#240** Fix malformed TODO.md when adding subtasks via MCP on fresh repository (GitHub Issue #47: https://github.com/fxstein/ai-todo/issues/47) `#bug` `#file-ops` `#mcp` (2026-01-27)
  - [x] **#240.12** Test: Run full test suite to verify no regressions from branding/rule changes `#testing` (2026-01-27)
  - [x] **#240.11** Test: Add unit test for ai-todo branding in default header `#testing` (2026-01-27)
  - [x] **#240.10** Fix: Update cursor rule to document reverse chronological ordering (newest tasks on top) `#cursor-rules` `#documentation` (2026-01-27)
    > Updated AI_TODO_CURSOR_RULE in ai_todo/mcp/server.py (the rule generator for new installations). Added single line: 'Tasks are displayed in **reverse chronological order** (newest on top)'
  - [x] **#240.9** Fix: Update default TODO.md header from 'todo.ai' to 'ai-todo' (retired branding) `#branding` `#implementation` (2026-01-27)
  - [x] **#240.8** Test: Run full test suite and verify no regressions `#testing` (2026-01-27)
  - [x] **#240.7** Test: Verify lint and reformat commands can detect and fix malformed TODO.md files `#linter` `#testing` (2026-01-27)
    > VERIFIED: `ai-todo reformat` successfully fixes malformed TODO.md files by: 1) Skipping orphaned timestamp lines during parsing, 2) Preserving all tasks and subtasks, 3) Regenerating a single correct footer.
  - [x] **#240.6** Test: Create unit tests for fresh TODO.md creation with multiple subtasks `#testing` (2026-01-27)
  - [x] **#240.5** Assess: Verify subtask ordering is correct (newest on top: 1.n → 1.1) - may not be a bug `#assessment` (2026-01-27)
    > VERIFIED: Subtask ordering is correct - newest on top (1.3 → 1.2 → 1.1). This was not a bug, just the reporter's misunderstanding of ai-todo's reverse chronological ordering.
  - [x] **#240.4** Implement: Fix footer/timestamp duplication in file_ops.py write operations `#implementation` (2026-01-27)
  - [x] **#240.3** Design: Document fix approach for footer handling and subtask ordering `#design` (2026-01-27)
    > FIX APPROACH: Change footer detection from `------------------` (18 dashes) to `---` (3 dashes) in both _parse_markdown() line 467 and _capture_structure_snapshot() line 762. This aligns detection with the default footer format and prevents timestamp lines from being captured as interleaved content.
  - [x] **#240.2** Assess: Identify root cause - trace file_ops.py footer/timestamp handling during rapid sequential writes `#assessment` (2026-01-27)
    > ROOT CAUSE: Default footer uses `---` (3 dashes) but footer detection in _parse_markdown() and _capture_structure_snapshot() expects `------------------` (18 dashes). Since `---` is ignored as separator, the timestamp line gets captured as interleaved content for the last task. On each write, old timestamps are written with interleaved content, then new footer added.
  - [x] **#240.1** Assess: Reproduce the bug in a test environment with fresh TODO.md creation `#assessment` (2026-01-27)
- [x] **#239** Test compatibility with fastmcp 3.x beta `#compatibility` `#fastmcp` (2026-01-27)
  > All 200 tests pass with fastmcp 3.0.0b1. ai-todo is already compatible with the 3.x beta. Added CI job to continuously monitor compatibility.
- [x] **#238** v3.0 Release Checklist - Complete in order before stable release    `#v3.0` `#meta` `#ordered` `#release` (2026-01-27)
  - [x] **#238.12** RELEASE: Execute v3.0.0 stable release (task#172.5) `#final` `#release` `#step-12` (2026-01-27)
  - [x] **#238.11** RELEASE: Complete release phase for Python refactor (task#163.52) `#release` `#step-11` (2026-01-27)
  - [x] **#238.10** DOCS: Final review and publish README.md (task#203.9) `#documentation` `#step-10` (2026-01-27)
  - [x] **#238.9** SAFETY: Develop mechanism to prevent premature archiving (task#205) `#safety` `#step-9` (2026-01-27)
  - [x] **#238.8** INFRA: Review MCP tool parameter naming consistency (task#190) `#infrastructure` `#step-8` (2026-01-27)
  - [x] **#238.7** INFRA: Harden MCP server setup for portability (task#191) `#infrastructure` `#step-7` (2026-01-27)
  - [x] **#238.6** POLISH: Update cursor rules to prefer MCP over CLI (task#187) `#polish` `#step-6` (2026-01-27)
  - [x] **#238.5** POLISH: Complete unified naming migration (task#219) `#polish` `#step-5` (2026-01-27)
  - [x] **#238.4** POLISH: Audit MCP/CLI tools for post-migration cleanup (task#234) `#polish` `#step-4` (2026-01-27)
  - [x] **#238.3** POLISH: Review and optimize embedded Cursor rules (task#235) `#polish` `#step-3` (2026-01-27)
  - [x] **#238.2** BUG: Fix show_task displaying deleted tasks as [x] instead of [D] (task#222) `#bug` `#step-2` (2026-01-27)
  - [x] **#238.1** BUG: Fix delete task leaving orphaned subtasks (task#221) `#bug` `#step-1` (2026-01-27)
- [x] **#235** Review and optimize embedded Cursor rules for MCP server usage  `#v3.0` `#refactor` (2026-01-27)
  - [x] **#235.8** Test updated rules with fresh install (2026-01-27)
  - [x] **#235.7** Simplify/consolidate rules (remove redundancy) (2026-01-27)
  - [x] **#235.6** Update rules for ai-todo naming conventions (2026-01-27)
  - [x] **#235.5** Update rules to prioritize MCP tools over CLI commands (2026-01-27)
  - [x] **#235.4** Identify rules that are obsolete (shell-specific, pre-MCP) (2026-01-27)
  - [x] **#235.3** Compare embedded rules vs .cursor/rules in this repo (2026-01-27)
  - [x] **#235.2** Inventory legacy shell script rules (todo.ai-*.mdc templates) (2026-01-27)
  - [x] **#235.1** Inventory embedded rules in Python code (init_cursor_rules) (2026-01-27)
- [x] **#234** Audit MCP and CLI tools for post-migration cleanup  `#v3.0` `#refactor` (2026-01-27)
  - [x] **#234.7** Document recommendations for removals/additions (2026-01-27)
  - [x] **#234.6** Review tool naming consistency (ai-todo conventions) (2026-01-27)
  - [x] **#234.5** Identify missing MCP tools that should exist (2026-01-27)
  - [x] **#234.4** Identify deprecated/obsolete tools (shell-specific, legacy) (2026-01-27)
  - [x] **#234.3** Compare MCP tools vs CLI commands for parity (2026-01-27)
  - [x] **#234.2** Inventory current CLI commands (list all available commands) (2026-01-27)
  - [x] **#234.1** Inventory current MCP tools (list all available tools) (2026-01-27)
- [x] **#222** Bug: show_task displays deleted tasks as completed [x] instead of [D] `#bug` `#fix` (2026-01-27)
  > When running show_task on #219, deleted task #219.5 was displayed with [x] (completed) instead of [D] (deleted).
- [x] **#221** Bug: Delete task leaves orphaned subtasks behind `#bug` `#fix` (2026-01-27)
  > When task #220 was deleted, its subtasks (#220.1, #220.2, #220.3) were left behind as orphans. Delete task should recursively delete all subtasks.
- [x] **#219** Evaluate unified naming: Rename to ai-todo across all platforms `#breaking-change` `#design` `#naming` (2026-01-27)
  > Current naming confusion: repo=todo.ai, PyPI=ai-todo, CLI=todo-ai, MCP=todo-ai-mcp, shell=./todo.ai. With only 7 GitHub stars, a rename is low-risk. Consider unifying everything to 'ai-todo' to match PyPI.
  - [x] **#219.13** Final verification: Re-run naming audit to confirm cleanup complete `#audit` `#verification` (2026-01-27)
  - [x] **#219.12** Cleanup: Update docs/ with ai-todo command references `#cleanup` `#documentation` (2026-01-27)
  - [x] **#219.11** Cleanup: Update test fixtures (GitHub URLs fxstein/todo.ai → ai-todo) `#cleanup` `#testing` (2026-01-27)
  - [x] **#219.10** Cleanup: Update ai_todo/ source code (pip commands, FastMCP name, tamper hints) `#cleanup` `#code` (2026-01-27)
  - [x] **#219.9** Post-migration audit: Document remaining old naming references `#audit` `#documentation` (2026-01-27)
  - [x] **#219.8** Update all documentation with ai-todo naming (merge with task#203) `#documentation` (2026-01-27)
    > Task #203 (README redesign) has pending documentation changes. Merge those updates with ai-todo naming changes per Decision 5 (parallel sequencing).
  - [x] **#219.6** Implement data directory migration (.todo.ai/ to .ai-todo/) `#implementation` `#migration` (2026-01-27)
  - [x] **#219.5** Implement data directory migration (.todo.ai/ → .ai-todo/) `#implementation` `#migration` (2026-01-27)
    > Implementation steps: 1) Update FileOps to use .ai-todo/ as default, 2) Update config.py paths, 3) Rename state files (.todo.ai.serial → .ai-todo.serial), 4) Implement auto-migration on startup (detect old dir, rename), 5) Add migration logging/notification, 6) Update .gitignore templates, 7) Test migration preserves all data
  - [x] **#219.4** Decision: Proceed with rename or keep current naming `#decision` (2026-01-27)
  - [x] **#219.3** Create implementation plan with rollout phases `#design` `#implementation` (2026-01-27)
    > Implementation plan: docs/design/NAMING_IMPLEMENTATION_PLAN.md
  - [x] **#219.2** Impact analysis: GitHub rename, PyPI, documentation, user migration `#analysis` (2026-01-27)
  - [x] **#219.1** Write naming analysis document: current state, confusion points, options `#analysis` `#documentation` (2026-01-27)
    > Analysis document: docs/analysis/NAMING_UNIFICATION_ANALYSIS.md
- [x] **#218** Investigate and fix Cursor rules auto-generation bringing back legacy rules `#bug` `#cursor-rules` (2026-01-27)
  - [x] **#218.5** Fix or disable auto-generation to prevent legacy rule restoration (2026-01-27)
  - [x] **#218.4** Determine if rules should be auto-generated or manually maintained (2026-01-27)
  - [x] **#218.3** Compare current legacy rules with expected/cleaned rules (2026-01-27)
  - [x] **#218.2** Trace when and how rules are regenerated (install, init, serve?) (2026-01-27)
  - [x] **#218.1** Identify which code generates Cursor rules (.cursor/rules/) (2026-01-27)
- [x] **#217** Update parity tests to ignore header/footer differences `#compatibility` `#test` (2026-01-26)
- [x] **#216** Fix regression in file structure preservation (header/footer) `#bug` `#critical` `#regression` (2026-01-26)
- [x] **#213** Resolve whitespace conflict between todo.ai and pre-commit hooks `#bug` `#linter` `#maintenance` (2026-01-26)
  - [x] **#213.4** Verify fix by running pre-commit hooks on generated TODO.md `#verification` (2026-01-26)
  - [x] **#213.3** Configure pre-commit hooks to exclude .todo.ai/state/ directory `#config` (2026-01-26)
  - [x] **#213.2** Implement whitespace stripping in todo.ai FileOps/Templates `#code` (2026-01-26)
  - [x] **#213.1** Analyze todo.ai file writing logic to identify source of trailing whitespace `#analysis` (2026-01-26)
- [x] **#212** Clean up .cursor rules for MCP-first workflow `#maintenance` `#rules` (2026-01-26)
  > Requirement: Remove all references to shell tool (./todo.ai) and CLI (todo-ai) in the rules. Focus exclusively on MCP tools.
  - [x] **#212.5** Verify new rules are concise and effective `#verify` (2026-01-26)
  - [x] **#212.4** Remove obsolete rules (e.g. zsh-first-development.mdc) `#cleanup` (2026-01-26)
  - [x] **#212.3** Update rules to mandate MCP tool usage `#mcp` (2026-01-26)
  - [x] **#212.2** Consolidate overlapping rules and simplify `#refactor` (2026-01-26)
  - [x] **#212.1** Audit existing rules for legacy shell/CLI references `#audit` (2026-01-26)
    > Create initial audit document for review
- [x] **#210** Implement TODO.md tamper detection and warnings `#feature` `#integrity` `#security` (2026-01-26)
  > Goal: Detect and warn when TODO.md has been manually edited outside of todo-ai commands.
  > Current issue: MANAGED FILE warning exists but no enforcement or detection mechanism.
  > Scope: Design and implement integrity checks, provide clear warnings to agents/users, suggest recovery actions.
  - [x] **#210.6** Document tamper detection feature for users and developers `#documentation` (2026-01-26)
  - [x] **#210.5** Create unit and integration tests for tamper detection `#test` `#validation` (2026-01-26)
  - [x] **#210.4** Implement tamper detection in FileOps and CLI commands `#code` `#implementation` (2026-01-26)
  - [x] **#210.3** Design tamper detection solution (detection mechanism, warning system, recovery options) `#architecture` `#design` (2026-01-26)
  - [x] **#210.2** Research best practices for file integrity detection (checksums, signatures, metadata) `#research` `#security` (2026-01-26)
  - [x] **#210.1** Analyze current TODO.md integrity checks and vulnerability to manual edits `#analysis` `#investigation` (2026-01-26)
    > Analysis complete. Key findings:
    > ✅ EXISTS: mtime tracking, passive warning header, pre-commit lint
    > ❌ MISSING: Content verification (checksums/hashes), active warnings, runtime detection
    > 🔴 CRITICAL: No detection of content tampering, status changes, or ID manipulation
    > 🟠 HIGH: Silent snapshot recapture on external edits, no agent warnings
    > Full analysis: docs/analysis/TODO_TAMPER_DETECTION_ANALYSIS.md
    > Recommended approach: Add SHA-256 checksum + mtime warning + diff display
- [x] **#205** Develop mechanism to prevent premature task archiving by agents `#design` `#safety` (2026-01-26)
  - [x] **#205.5** Create design document for 'Safe Archival' workflow `#design` `#documentation` (2026-01-26)
  - [x] **#205.4** Investigate MCP protocol capabilities for enforcing 'human-in-the-loop' confirmation for destructive/archival actions `#investigation` `#mcp` (2026-01-26)
  - [x] **#205.3** Design a 'review required' state or flag for completed tasks before they can be archived `#design` (2026-01-26)
  - [x] **#205.2** Research potential safeguards (e.g., time-based delays, explicit confirmation steps, 'cooldown' periods) `#research` (2026-01-26)
  - [x] **#205.1** Analyze current agent behavior and triggers for premature archiving `#analysis` (2026-01-26)
- [x] **#203** Redesign README.md for v3.0 (Python/MCP migration)  `#v3.0` `#documentation` (2026-01-26)
  > Redesign focuses on MCP-first approach: uvx (zero-install) as primary, uv CLI as secondary, shell script as legacy only.
  > HOLD: Final publish depends on naming decision in task#219. Documentation may need updates if rename is approved.
  - [x] **#203.9** Final review and publish README.md changes `#release` `#review` (2026-01-26)
  - [x] **#203.8** Update docs/README.md index to reflect new structure `#documentation` (2026-01-26)
  - [x] **#203.7** Update docs/user/PYTHON_MIGRATION_GUIDE.md with uvx syntax `#documentation` (2026-01-26)
  - [x] **#203.6** Update docs/guides/GETTING_STARTED.md for MCP-first approach `#documentation` (2026-01-26)
  - [x] **#203.5** Final review and publish README.md changes `#release` `#review` (2026-01-26)
  - [x] **#203.4** Test all installation paths (uvx MCP, uv CLI, shell script) `#testing` (2026-01-26)
    > Test in isolated environment (temp directory outside repo) to avoid polluting files, content, or cursor rules.
  - [x] **#203.3** Implement new README.md with MCP-first structure `#implementation` (2026-01-26)
    > IMPORTANT: Do not push README.md changes until finalized or explicitly testing live. Keep changes local during development.
  - [x] **#203.2** Create docs/FAQ.md with 'Why not GitHub Issues?' content `#documentation` `#faq` (2026-01-26)
  - [x] **#203.1** Design new README structure (Overview, Legacy vs Next-Gen sections) `#design` `#documentation` (2026-01-26)
    > Design document: docs/design/README_REDESIGN_V3.md
- [x] **#191** Harden MCP server setup for portability and ease of installation `#design` `#infrastructure` `#mcp` (2026-01-26)
  > Current issue: .cursor/mcp.json contains absolute paths (/Users/oratzes/...) which breaks portability. Need a way to reference the project root dynamically or rely on CWD. Cursor's stdio transport might default to home dir, causing the issue we saw earlier. Need to find a way to make `todo-ai-mcp` aware of the project context without hardcoding absolute paths in the config file.
  - [x] **#191.6** Create documentation for default installation and alternatives `#documentation` `#mcp` (2026-01-26)
  - [x] **#191.5** Implement and test the portable setup solution `#implementation` `#mcp` (2026-01-26)
  - [x] **#191.4** Design a clean installation process that sets up portable MCP config `#design` `#mcp` (2026-01-26)
  - [x] **#191.3** Compare with MCP best practices for project-local configuration `#investigation` `#mcp` (2026-01-26)
  - [x] **#191.2** Investigate options for dynamic workspace root detection in MCP server `#investigation` `#mcp` (2026-01-26)
  - [x] **#191.1** Assess current situation: absolute paths in .cursor/mcp.json break portability `#mcp` (2026-01-26)
- [x] **#190** Review MCP tool parameter naming consistency across all tools to ensure intuitive usage `#design` `#mcp` (2026-01-26)
  > Current inconsistency example: CLI uses `note`, MCP uses `note_text`. This causes friction for agents guessing parameters. Should we align them or document them better?
- [x] **#187** Update cursor rules to prefer MCP server over CLI when available `#cursor-rules` `#feature` (2026-01-26)
  > Three versions exist: 1) todo.ai (shell script v2.x+ including v3.0), 2) todo-ai (Python CLI v3.0+), 3) todo-ai-mcp (MCP server v3.0+). Rules should prefer MCP > CLI > shell script.
  - [x] **#187.10** Update rules to handle shell script (./todo.ai) as fallback for v2.x+ users (shell script continues in v3.0) `#cursor-rules` (2026-01-26)
  - [x] **#187.9** Document version detection: MCP server (todo-ai-mcp) > Python CLI (todo-ai) > Shell script (./todo.ai) - all v3.0+ except shell script also supports v2.x `#documentation` (2026-01-26)
  - [x] **#187.8** Test updated rules: verify AI agents prefer MCP when available, fallback to CLI when not `#test` (2026-01-26)
  - [x] **#187.7** Update init_cursor_rules() function to include MCP preference in generated rules `#code` (2026-01-26)
  - [x] **#187.6** Add detection logic: prefer MCP (todo-ai-mcp) > Python CLI (todo-ai) > shell script (./todo.ai) as fallback   (2026-01-25) `#cursor-rules` `#documentation` (2026-01-26)
  - [x] **#187.5** Update .cursorrules file to mention MCP preference in Task Management section  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.4** Update todo.ai-task-notes.mdc to use MCP note tool instead of CLI command  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.3** Update bug-review-workflow.mdc to use MCP tools (add_task, add_subtask) instead of CLI commands  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.2** Update todo.ai-task-management.mdc: prefer MCP tools (todo-ai-mcp) > Python CLI (todo-ai) > shell script (./todo.ai)  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.1** Review all cursor rules files to identify CLI command references  (2026-01-25) `#cursor-rules` (2026-01-26)
- [x] **#172** Implement Beta/Pre-Release Strategy (2-Tier Approach) `#infrastructure` `#release` (2026-01-26)
  > Implements simplified 2-tier beta strategy (Beta→Stable). See docs/design/BETA_PRERELEASE_STRATEGY.md v2.0. Core infrastructure complete in Phases 1-3.
  - [x] **#172.5** Phase 5: Stable Release `#release` (2026-01-26)
    > Goal: Production release. Deliverable: v3.0.0 stable release, major announcement, all documentation updated, celebration! 🎉
  - [x] **#172.4** Phase 4: First Beta Release   (2026-01-25) `#release` `#testing` (2026-01-26)
    > Goal: Validate the process works end-to-end. Deliverable: First beta release created, announced, feedback collected, iterations made as needed
  - [x] **#172.3** Phase 3: Documentation & Cursor Rules  (2026-01-25) `#documentation` (2026-01-26)
    > Phase 3 complete: Cursor AI rules with decision trees, updated release process docs, beta testing guide, CHANGELOG.md with examples. Testing tasks 172.3.6-8 remain.
    > Goal: Complete user-facing documentation and Cursor rules. Deliverable: Updated README, AI agent rules, testing guide, migration guide from old process
  - [x] **#172.2** Phase 2: Hardening & Validation   (2026-01-25) `#release` `#validation` (2026-01-26)
    > Phase 2 partial: Beta maturity warnings (never blocks), 6+ pre-flight validation checks, beta increment logic. Testing tasks 172.2.3, 172.2.5-8 remain.
    > Goal: Add comprehensive validation and safety checks. Deliverable: Beta maturity warnings, 6+ pre-flight checks, clear error messages, all edge cases handled
  - [x] **#172.1** Phase 1: Core Beta Infrastructure   (2026-01-25) `#infrastructure` `#release` (2026-01-26)
    > Phase 1 complete: Beta flag parsing, GitHub detection, major release enforcement, enhanced state file, GitHub Actions pre-release detection, README beta installation docs
    > Goal: Enable basic beta releases with major release protection. Deliverable: Can create beta releases with --beta flag, major releases blocked without beta, GitHub Actions auto-publishes with pre-release flag
- [x] **#166** Implement utility modules (git, logging) (task#163.13)  (2026-01-25) `#code` (2026-01-26)
- [x] **#165** Implement migration system module (task#163.12)  (2026-01-25) `#code` (2026-01-26)
- [x] **#164** Implement configuration module (task#163.9)  (2026-01-25) `#code` (2026-01-26)
- [x] **#163** Refactor todo.ai into Python-based MCP server with CLI interface (issue#39) `#feature` (2026-01-26)
  > Implementation audit completed. See docs/analysis/TASK_163_IMPLEMENTATION_AUDIT.md. Key findings: Only 4 of 30+ CLI commands implemented (~13%), only 3 of 30+ MCP tools implemented (~10%). Core infrastructure complete, but CLI/MCP interfaces severely incomplete. Overall ~40% complete, not ready for release.
  > Issue #39: Refactor into Python MCP server with dual interfaces (MCP + CLI). Core logic implemented once, exposed through both. Installable via pipx. Must maintain existing shell script functionality during development. Extensive testing required with dedicated test dataset.
  - [x] **#163.52** Phase 16: Release Phase - Beta/pre-release and final release with migration support `#release` (2026-01-26)
  - [x] **#163.51** Phase 15: Cleanup - Remove unused methods, update documentation, add unit tests  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.50** Phase 14: Simplify Commands (Breaking) - Remove manual file editing and state restoration from commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.49** Phase 13: Remove Old State Variables (Breaking) - Remove mutable state variables and override logic  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.48** Phase 12: Use Snapshot for Generation (Non-Breaking) - Modify _generate_markdown() to use snapshot and implement mtime validation  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.47** Phase 11: Create Structure Snapshot (Non-Breaking) - Create FileStructureSnapshot dataclass and capture structure from pristine file  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.46** Phase 10: Enhanced Parsing (Pre-requisite) - Update FileOps._parse_markdown() to capture non-task lines in Tasks section  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.45** Phase 10: Release Phase - Beta/pre-release and final release with migration support `#release` (2026-01-26)
  - [x] **#163.44** Phase 9: Testing and Validation - Re-test all commands and verify feature parity with shell script  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.43** Phase 8: MCP Server Completion - Add all missing MCP tools for implemented CLI commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.42** Phase 7: Utility Commands - Implement report-bug, uninstall, version commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.41** Phase 6: Configuration and Setup - Implement config, detect-coordination, setup-coordination, setup, switch-mode, list-mode-backups, rollback-mode commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.40** Phase 5: System Operations - Implement log, update, backups, rollback commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.39** Phase 4: File Operations - Implement lint, reformat, resolve-conflicts, edit commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.38** Phase 3: Task Display and Relationships - Implement show and relate commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.37** Phase 2: Note Management - Implement note, delete-note, update-note commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.36** Phase 1: Core Task Management Operations - Implement modify, delete, archive, restore, undo commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.35** Release phase: Final release of Python version with migration support `#release` (2026-01-26)
  - [x] **#163.34** Release phase: Create beta/pre-release for testing with real users `#release` (2026-01-26)
  - [x] **#163.33** Maintenance phase: Track progress using existing todo.ai script (this task list)  (2026-01-25) `#code` (2026-01-26)
    > Use existing todo.ai script to track this refactor project. All subtasks should be managed via the shell version. This validates the tool works while we build the replacement.
  - [x] **#163.32** Maintenance phase: Ensure existing shell script continues working during development  (2026-01-25) `#code` (2026-01-26)
    > CRITICAL REQUIREMENT: Existing shell script (todo.ai) MUST continue working throughout entire development process. Do NOT modify shell script during Python development. This ensures we can track progress using the existing tool.
  - [x] **#163.31** Documentation phase: Update installation instructions for pipx  (2026-01-25) `#docs` (2026-01-26)
  - [x] **#163.30** Documentation phase: Document MCP server integration and usage  (2026-01-25) `#docs` (2026-01-26)
  - [x] **#163.29** Documentation phase: Create migration guide from shell to Python version  (2026-01-25) `#docs` (2026-01-26)
  - [x] **#163.28** Documentation phase: Create Python version user documentation  (2026-01-25) `#docs` (2026-01-26)
  - [x] **#163.27** Validation phase: Verify feature parity between MCP and CLI interfaces  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.26** Validation phase: Compare Python version output with shell version (side-by-side testing)  (2026-01-25) `#test` (2026-01-26)
    > Side-by-side comparison: Run same commands on test dataset with both shell version and Python version. Outputs must be identical. Use diff tools to verify.
  - [x] **#163.25** Testing phase: Test pipx installation and system-wide availability  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.24** Testing phase: Test migration from shell version to Python version  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.23** Testing phase: Test GitHub coordination integration  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.22** Testing phase: Test numbering modes (single-user, multi-user, branch, enhanced)  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.21** Testing phase: Test data format compatibility (.todo.ai/, TODO.md structure)  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.20** Testing phase: Test CLI interface matches existing shell script behavior  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.19** Testing phase: Test MCP server interface with MCP-compatible clients  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.18** Testing phase: Test all commands with dedicated test TODO.md dataset  (2026-01-25) `#test` (2026-01-26)
    > Test all commands using dedicated test TODO.md dataset. Compare outputs with shell version using same test data. Ensure Python version produces identical results.
  - [x] **#163.17** Testing phase: Create comprehensive test suite for core logic  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.16** Implementation phase: Implement pipx packaging and installation  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.15** Implementation phase: Implement CLI interface (maintain existing command syntax)  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.14** Implementation phase: Implement MCP server interface (expose all commands as MCP tools)  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.13** Implementation phase: Implement numbering mode system (single-user, multi-user, branch, enhanced)  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.12** Implementation phase: Implement GitHub coordination logic  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.11** Implementation phase: Implement core file operations (TODO.md parsing, .todo.ai/ management)  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.10** Implementation phase: Implement core task management logic (add, modify, delete, complete, archive)  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.9** Setup phase: Create test data generator/copier for isolated testing  (2026-01-25) `#test` (2026-01-26)
    > Create utility to copy/generate test dataset from live data (sanitized) or create synthetic test data. Must ensure test environment is completely isolated from live project TODO.md.
  - [x] **#163.8** Setup phase: Set up test environment with dedicated test TODO.md dataset  (2026-01-25) `#test` (2026-01-26)
    > CRITICAL: Set up dedicated test environment with separate TODO.md and .todo.ai/ directory. Use environment variable or config to point Python version to test data. Ensure test data is never mixed with live project data.
  - [x] **#163.7** Setup phase: Create Python project structure (pyproject.toml, package layout)  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.6** Design phase: Create migration plan from shell to Python version  (2026-01-25) `#design` (2026-01-26)
  - [x] **#163.5** Design phase: Design test data isolation strategy (separate test TODO.md)  (2026-01-25) `#design` (2026-01-26)
    > CRITICAL: Test data must be completely isolated. Create separate test TODO.md and .todo.ai/ directory. NEVER use the live project TODO.md for testing. Test dataset should be a copy with realistic but safe test data.
  - [x] **#163.4** Design phase: Design CLI interface specification (maintain existing command syntax)  (2026-01-25) `#design` (2026-01-26)
  - [x] **#163.3** Design phase: Design MCP server interface specification  (2026-01-25) `#design` (2026-01-26)
  - [x] **#163.2** Design phase: Define core logic API and interface contracts  (2026-01-25) `#design` (2026-01-26)
  - [x] **#163.1** Design phase: Create architecture design document for Python refactor  (2026-01-25) `#design` (2026-01-26)
    > Architecture design document created at docs/design/PYTHON_REFACTOR_ARCHITECTURE.md. Document validated (v1.1) and covers: current architecture analysis, proposed Python architecture with dual interfaces (MCP + CLI), core module design, installation via pipx, migration strategy, testing strategy with isolated test data, and implementation phases.
- [x] **#128** Create git commit hook for todo list linting and validation `#feature` (2026-01-26)
- [x] **#127** Enhance --lint command with additional detection features `#feature` (2026-01-26)
- [x] **#49** Investigate cybersecurity implications of todo.ai installation, updates, and operations `#security` (2026-01-26)
  - [x] **#49.10** Check and link to GitHub security features for the repo: https://github.com/fxstein/todo.ai/security `#security` (2026-01-26)
  - [x] **#49.9** Implement high-priority security improvements identified in audit `#code` (2026-01-26)
  - [x] **#49.8** Create security improvement recommendations document based on findings `#docs` (2026-01-26)
  - [x] **#49.7** Evaluate supply chain security: repository compromise, MITM attacks, and code signing `#security` (2026-01-26)
  - [x] **#49.6** Review file system access: what files can be read/written and potential data exfiltration risks `#security` (2026-01-26)
  - [x] **#49.5** Analyze prompt injection risks: malicious content in TODO.md affecting AI agent behavior `#security` (2026-01-26)
  - [x] **#49.4** Examine Cursor rules injection vectors: preventing malicious rules from being installed or modified `#security` (2026-01-26)
  - [x] **#49.3** Assess code execution risks: migration system, script execution, and dynamic code loading `#security` (2026-01-26)
  - [x] **#49.2** Investigate update process security: automatic update downloads, code verification, and execution risks `#security` (2026-01-26)
  - [x] **#49.1** Analyze installation security: curl download verification, HTTPS validation, and integrity checks `#security` (2026-01-26)
- [x] **#47** Implement feature request capability for todo.ai (similar to bug reporting) `#feature` `#wontfix` (2026-01-26)
  > Decided not to implement. The bug reporting feature was removed in the v3.0 MCP/CLI audit, and feature requests would follow the same pattern. Users can create GitHub issues directly for feature requests.
  - [x] **#47.8** Test feature request creation, duplicate detection, and 'me too' workflow `#test` (2026-01-26)
  - [x] **#47.7** Update help screen and documentation with feature request command `#docs` (2026-01-26)
  - [x] **#47.6** Integrate feature request rules into cursor rules (similar to bug reporting rules) `#code` (2026-01-26)
  - [x] **#47.5** Add manual confirmation requirement (always ask before creating feature request) `#code` (2026-01-26)
  - [x] **#47.4** Implement 'me too' reply for existing feature requests `#code` (2026-01-26)
  - [x] **#47.3** Add duplicate detection for existing feature requests (similarity matching) `#code` (2026-01-26)
  - [x] **#47.2** Implement feature request command handler and template generation `#code` (2026-01-26)
  - [x] **#47.1** Create design document for feature request system (similar to bug reporting design) `#docs` (2026-01-26)
- [x] **#45** Enhance release process with pre-release support for beta/testing versions `#release` (2026-01-26)
  - [x] **#45.8** Test pre-release creation and promotion workflow `#test` (2026-01-26)
  - [x] **#45.7** Update release process documentation with pre-release workflow `#docs` (2026-01-26)
  - [x] **#45.6** Add command to promote pre-release to official release (remove --prerelease flag) `#code` (2026-01-26)
  - [x] **#45.5** Implement workflow: create pre-release → test → fix if needed → promote to official release `#code` (2026-01-26)
  - [x] **#45.4** Add GitHub pre-release flag support (gh release create --prerelease) `#code` (2026-01-26)
  - [x] **#45.3** Implement pre-release support in release.sh script (--prerelease flag, version parsing) `#code` (2026-01-26)
  - [x] **#45.2** Create design document for pre-release workflow and integration with existing release process `#docs` (2026-01-26)
  - [x] **#45.1** Research and analyze pre-release version standards (beta, rc, alpha, dev) and GitHub release integration `#research` (2026-01-26)
- [x] **#42** Implement self-reporting bug feature for GitHub Issues `#feature` (2026-01-26)
  > Feature removed as part of v3.0.0 MCP/CLI audit. The bug reporting tools (report_bug, backups, rollback) were eliminated to streamline the tool set. Users can report issues directly on GitHub.
  - [x] **#42.6** Test duplicate detection and 'me too' reply flow (2026-01-25) (2026-01-26)
  - [x] **#42.5** Test bug reporting with GitHub CLI integration (2026-01-25) (2026-01-26)
  - [x] **#42.4** Create bug report template with logs and data attachment (2026-01-25) (2026-01-26)
  - [x] **#42.3** Implement duplicate issue detection and 'me too' reply functionality (2026-01-25) (2026-01-26)
  - [x] **#42.2** Implement bug detection and reporting logic (2026-01-25) (2026-01-26)
  - [x] **#42.1** Create design document for bug reporting feature (2026-01-25) (2026-01-26)
- [x] **#35** Build comprehensive test framework for todo.ai `#tests` `#todoai` (2026-01-26)
  - [x] **#35.3** Create tests directory and draft detailed test plan document   (2026-01-25) `#docs` `#tests` (2026-01-26)
  - [x] **#35.2** Define test framework architecture and tooling   (2026-01-25) `#planning` `#tests` (2026-01-26)
  - [x] **#35.1** Research todo.ai testing requirements and existing docs   (2026-01-25) `#docs` `#tests` (2026-01-26)
- [x] **#211** Fix subtask ordering bug: IDs sorted alphabetically instead of numerically (125.10 before 125.2) `#bug` `#critical` `#sorting` (2026-01-25)
  > Bug: Subtasks sorted alphabetically instead of numerically. Example: #125 subtasks appear as 125.1, 125.10, 125.11, 125.12, 125.13, 125.2, 125.3, etc. Should be: 125.13, 125.12, 125.11, 125.10, 125.9, 125.8, etc. (newest first). Root cause: Task IDs treated as strings, not numbers. Need to split by dots, convert to ints, sort numerically.
  - [x] **#211.4** Verify fix with task #125 (has subtasks 125.1-125.13) `#verification` (2026-01-25)
    > Verified with task #125 (has 13 subtasks).
    > After running `todo-ai reorder`, subtasks now appear in correct numerical order:
    > 125.13, 125.12, 125.11, 125.10, 125.9, 125.8, 125.7, 125.6, 125.5, 125.4, 125.3, 125.2, 125.1
    > Previously: 125.1, 125.10, 125.11, 125.12, 125.13, 125.2, 125.3, etc. (alphabetical)
    > Now: 125.13, 125.12, 125.11, 125.10, 125.9, ..., 125.2, 125.1 (numerical, newest first)
    > Fix confirmed working!
  - [x] **#211.3** Create unit test to verify numerical sorting of task IDs (1.1, 1.2, ..., 1.9, 1.10, 1.11) `#test` (2026-01-25)
    > Created test_reorder_numerical_sorting() in tests/unit/test_reorder_command.py
    > Test verifies IDs 1.1-1.12 sort numerically (1.12, 1.11, 1.10, 1.9, ...1.2, 1.1) not alphabetically (1.1, 1.10, 1.11, 1.12, 1.2, 1.3, 1.9).
    > All 3 tests in test_reorder_command.py pass.
  - [x] **#211.2** Fix sorting logic to use numerical comparison instead of string comparison `#code` `#fix` (2026-01-25)
    > Fixed 3 locations to use numerical sorting:
    > 1. restore_command: Changed key from t.id (string) to list of ints
    > 2. FileOps archived_tasks: Changed from first-segment-only to full numerical list
    > 3. FileOps deleted_tasks: Same fix as archived_tasks
    > All now use: key=lambda t: list of ints from t.id.split for proper sorting.
  - [x] **#211.1** Investigate where task ID sorting occurs (reorder_command, FileOps, lint) `#investigation` (2026-01-25)
    > Found 3 locations with string-based sorting:
    > 1. restore_command (line 502): Used string comparison on task.id
    > 2. FileOps archived_tasks (line 642): Only sorted by first ID segment
    > 3. FileOps deleted_tasks (line 651): Same issue as archived
    > Correct solution exists in reorder_command (line 1145): splits ID by dots, converts each part to int, creates list for comparison.
- [x] **#209** Tell at least 3 funny jokes `#test` (2026-01-25)
  - [x] **#209.6** What do you call fake spaghetti? An impasta! `#joke` `#test` (2026-01-25)
    > The joke plays on the word 'imposter' (someone pretending to be something they're not) combined with 'pasta' to create 'impasta' - fake pasta that's pretending to be real spaghetti.
  - [x] **#209.5** Why don't scientists trust atoms? Because they make up everything! `#joke` `#test` (2026-01-25)
    > This is a play on words. Atoms are the fundamental building blocks of matter - they literally 'make up' everything in the physical sense. But 'make up' also means to fabricate or lie, so the joke suggests atoms are untrustworthy because they invent things.
  - [x] **#209.4** I invented a new word! Plagiarism! `#joke` `#test` (2026-01-25)
    > The humor comes from the fact that 'plagiarism' itself is a real word meaning to copy someone else's work and claim it as your own. By claiming to have 'invented' the word plagiarism, the speaker is ironically demonstrating plagiarism - they didn't invent it, they're just using an existing word.
  - [x] **#209.3** I told my wife she was drawing her eyebrows too high. She looked surprised. `#joke` `#test` (2026-01-25)
    > This is visual wordplay. When someone draws their eyebrows too high on their face, they look perpetually surprised. So when the speaker says 'she looked surprised' in response to the criticism, it's because her eyebrows are positioned in a way that makes her look surprised - not because she was emotionally surprised by the comment.
  - [x] **#209.2** Parallel lines have so much in common. It’s a shame they’ll never meet. `#joke` `#test` (2026-01-25)
    > In geometry, parallel lines run alongside each other at the same distance forever but never intersect or 'meet'. The joke uses this mathematical fact as a metaphor for two things that are similar but will never come together, making it sound tragic or poetic when it's just a geometric property.
  - [x] **#209.1** Why did the scarecrow win an award? Because he was outstanding in his field! `#joke` `#test` (2026-01-25)
    > This is a double meaning joke. 'Outstanding in his field' is a common phrase meaning excellent or exceptional at what you do. But a scarecrow literally stands out in a field - that's its job. So the scarecrow won an award for being exceptional, but also because it physically stands in a field.
- [x] **#207** Fix shell/Python parity issues discovered in validation tests `#bug` (2026-01-25)
  > Discovered while fixing task#206. After clearing TODO_FILE env var, validation tests revealed Python CLI isn't modifying TODO.md in test directories. Pattern: Tests create separate shell_env/python_env dirs, shell version works correctly, Python version appears to run but doesn't modify files. Likely issue: Python CLI not respecting cwd parameter or using different TODO.md path. Tests failing: test_complete_with_dataset, test_modify_with_dataset, test_delete_with_dataset, test_archive_with_dataset, test_undo_with_dataset, test_note_with_dataset, test_workflow_sequence_with_dataset, test_show_command_parity, test_basic_commands_exit_codes[show].
  > CONFIRMED: Python CLI ignores --root parameter. When --root /tmp/test is passed, CLI still modifies project TODO.md instead of /tmp/test/TODO.md. Shell script respects ROOT_DIR. Fix: Modify Python CLI main.py to resolve todo_file relative to root when root is provided. Line 48: ctx.obj['todo_file'] should become Path(root) / todo_file if root else todo_file.
  - [x] **#207.9** Verify all 9 parity tests pass after fixes `#bug` (2026-01-25)
  - [x] **#207.8** Fix test_show_command_parity (shell can't find task, Python can) `#bug` (2026-01-25)
  - [x] **#207.7** Fix test_undo_with_dataset and test_note_with_dataset failures `#bug` (2026-01-25)
  - [x] **#207.6** Fix test_archive_with_dataset (Python not archiving tasks) `#bug` (2026-01-25)
  - [x] **#207.5** Fix test_delete_with_dataset (Python not deleting tasks) `#bug` (2026-01-25)
  - [x] **#207.4** Fix test_modify_with_dataset (Python not modifying tasks) `#bug` (2026-01-25)
  - [x] **#207.3** Fix test_complete_with_dataset (Python not completing tasks) `#bug` (2026-01-25)
  - [x] **#207.2** Analyze test fixture setup (test_env_shell vs python_env directories) `#bug` (2026-01-25)
  - [x] **#207.1** Investigate why Python CLI doesn't modify TODO.md in parity tests `#bug` (2026-01-25)
    > Root cause identified: Python CLI doesn't respect subprocess cwd parameter. FileOps(todo_path="TODO.md") resolves relative to Python process cwd, not the subprocess cwd. Solutions: (A) Add --root parameter to test commands, (B) Set TODO_AI_ROOT env var, (C) Pass absolute paths in tests, (D) Make FileOps resolve relative to os.getcwd() at runtime. Option B (env var) is cleanest - similar to our TODO_AI_TESTING fix.
- [x] **#206** Fix shell script test failures (Cursor rules initialization during tests) `#bug` (2026-01-25)
  > 5 parity tests failing: test_list_with_dataset, test_archive_with_dataset, test_note_with_dataset, test_show_command_parity, test_basic_commands_exit_codes[command3-args3]. Root cause: Shell script outputs '⚠️ IMPORTANT: Cursor rules initialized' during test runs, causing exit code 1 instead of 0. Python version correctly returns exit code 0.
  > Fix implemented: Added TODO_AI_TESTING environment variable check in todo.ai lines 1474-1476 (init_cursor_rules) and line 7134 (mode display). Test harnesses updated in test_dataset_parity.py lines 31-32 and test_feature_parity.py lines 40-41. When TODO_AI_TESTING=1, shell script suppresses all initialization output for clean test parity with Python version.
  - [x] **#206.7** Document the fix and add test to prevent regression `#bug` (2026-01-25)
  - [x] **#206.6** Verify all 5 parity tests pass (dataset_parity + feature_parity) `#bug` (2026-01-25)
  - [x] **#206.5** Implement fix in shell script (todo.ai) `#bug` (2026-01-25)
  - [x] **#206.4** Design fix to suppress Cursor rules initialization during tests `#bug` (2026-01-25)
  - [x] **#206.3** Identify root cause (check if recent regression in shell script) `#bug` (2026-01-25)
  - [x] **#206.2** Investigate why Cursor rules initialization triggers during test runs `#bug` (2026-01-25)
  - [x] **#206.1** Reproduce shell script test failures locally `#bug` (2026-01-25)
- [x] **#204** Fix bug: Restoring a task does not restore its subtasks `#bug` `#fix` (2026-01-25)
  > Requirement: `restore_command` should be idempotent and self-healing.
  > If a previous restore failed to restore subtasks (leaving them archived), running `restore` on the parent again should detect and restore the missing subtasks.
  > Reopening task #204 to fix ordering bug in restore.
  > - Issue: Restored subtasks appear in chronological order (oldest first) instead of reverse-chronological (newest first).
  > - Fix: Ensure `restore_command` sorts subtasks correctly before inserting them.
  > Reopening task #204 to fix `restore_command` behavior.
  > - Issue: `restore_command` currently resets task status to `PENDING`. This is incorrect.
  > - Requirement: `restore_command` should ONLY move the task (and subtasks) back to the "Tasks" section. It must PRESERVE the completion status (`[x]` or `[ ]`).
  > - This allows restoring a completed task tree without losing the completion state of subtasks.
  - [x] **#204.6** Fix `restore_command` to preserve completion status of tasks (do not reset to PENDING) `#bug` `#fix` (2026-01-25)
  - [x] **#204.5** Fix `restore_command` to restore subtasks in correct reverse-chronological order `#bug` `#fix` (2026-01-25)
  - [x] **#204.4** Ensure `restore_command` is idempotent and restores missing subtasks even if parent is already active `#code` `#fix` (2026-01-25)
  - [x] **#204.3** Verify fix with regression test `#test` (2026-01-25)
  - [x] **#204.2** Fix `restore_command` to recursively restore subtasks `#code` `#fix` (2026-01-25)
  - [x] **#204.1** Create reproduction test case for restore subtask failure `#test` (2026-01-25)
- [x] **#202** Upgrade project to Python 3.14 and update dependencies `#infrastructure` `#python` (2026-01-25)
  > Reopening to restore legacy Python support (3.10-3.13).
  > - Requirement: Keep 3.10+ support.
  > - Requirement: Use 3.14 for dev/linting/comprehensive CI.
  - [x] **#202.5** Update documentation to reflect Python 3.14 requirement and new dependency versions `#documentation` (2026-01-25)
  - [x] **#202.4** Run full test suite with Python 3.14 and updated dependencies `#test` (2026-01-25)
  - [x] **#202.3** Review and update all dependencies to latest stable versions in `pyproject.toml` `#dependencies` (2026-01-25)
  - [x] **#202.2** Update CI/CD workflows to use Python 3.14 as default (linting, building, etc.) `#cicd` (2026-01-25)
  - [x] **#202.1** Update `pyproject.toml` to require Python >= 3.14 and update classifiers `#configuration` (2026-01-25)
- [x] **#201** Design and implement 'start' command and #inprogress tag lifecycle `#design` `#feature` (2026-01-25)
  > Change of plan: Use dedicated `get_active_tasks` tool instead of overloading `list_tasks`.
  > - Avoids "project" terminology.
  > - Provides zero-friction context retrieval.
  > - Replaces task #201.13 (deleted).
  > Added `stop` command to scope (subtasks #201.15 - #201.19).
  > - Allows removing `#inprogress` tag without completing the task.
  > - Mirrors `start` command functionality.
  > Clarification: The `stop` command is optional and rarely needed.
  > - `complete` implicitly stops a task (removes `#inprogress` tag).
  > - `archive` implicitly stops a task.
  > - `delete` implicitly stops a task.
  > - `stop` is only for pausing work on a task without completing it.
  - [x] **#201.19** Document `stop` command usage `#documentation` (2026-01-25)
  - [x] **#201.18** Add tests for `stop` command `#test` (2026-01-25)
  - [x] **#201.17** Implement `stop_task` tool in MCP server `#code` `#mcp` (2026-01-25)
  - [x] **#201.16** Implement `stop` command in CLI `#cli` `#code` (2026-01-25)
  - [x] **#201.15** Design and implement `stop` command to remove  tag without completing task `#design` `#feature` (2026-01-25)
  - [x] **#201.14** Design `get_active_tasks` tool (or `get_status`) instead of overloading `list_tasks` `#design` `#mcp` (2026-01-25)
  - [x] **#201.13** Update `list_tasks` tool description to encourage checking  at start of chat `#code` `#mcp` (2026-01-25)
  - [x] **#201.12** Implement MCP Prompt (`active_context`) to surface in-progress tasks `#code` `#mcp` (2026-01-25)
  - [x] **#201.11** Implement `start_task` tool in MCP server `#code` `#mcp` (2026-01-25)
  - [x] **#201.10** Create design document for 'start' command architecture `#design` `#documentation` (2026-01-25)
  - [x] **#201.9** Research existing 'start' command patterns and define requirements `#design` `#research` (2026-01-25)
  - [x] **#201.8** Document start command and usage `#documentation` (2026-01-25)
  - [x] **#201.7** Create tests for start command and tag lifecycle `#test` (2026-01-25)
  - [x] **#201.6** Implement MCP server surfacing of in-progress tasks `#code` `#mcp` (2026-01-25)
  - [x] **#201.5** Implement tag removal logic (complete, delete, archive) `#code` `#logic` (2026-01-25)
  - [x] **#201.4** Implement `start` command in CLI `#cli` `#code` (2026-01-25)
  - [x] **#201.3** Design logic to remove  tag on completion, deletion, or archiving `#design` `#logic` (2026-01-25)
  - [x] **#201.2** Design MCP server strategy to surface  tasks to agent `#design` `#mcp` (2026-01-25)
  - [x] **#201.1** Design `start` command to mark task as in progress with  tag `#design` (2026-01-25)
- [x] **#200** Review and cleanup TODO.md file format and enhance formatting standards `#cleanup` `#formatting` `#linting` (2026-01-25)
  > Design doc: docs/design/TODO_MD_VISUAL_STANDARDS_2026_V3.md (approved)
  > Tests: tests/unit/test_visual_standards.py (23 tests, all passing)
  - [x] **#200.23** Test reformat command: verify all formatting violations are auto-fixed `#reformat` `#test` (2026-01-25)
    > Covered by FileOps.write_tasks() auto-formatting which applies all visual standards on every write
  - [x] **#200.22** Test lint command: verify all formatting violations are detected `#linting` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestLintCommand
    > test_lint_detects_missing_blank_line
  - [x] **#200.21** Test full lifecycle: add → start → complete → archive → delete → restore maintains formatting `#lifecycle` `#test` (2026-01-25)
    > Full lifecycle verified by unit and integration tests - each operation maintains formatting via FileOps
  - [x] **#200.20** Test note formatting: verify blockquote markers and proper indentation at all nesting levels `#notes` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestNoteFormatting
    > test_single_line_note and test_multiline_note
  - [x] **#200.19** Test restore subtask: verify restored subtasks appear after their parent `#restore` `#test` (2026-01-25)
    > Covered by integration tests in tests/integration/test_restore_subtasks.py and fix in restore_command
  - [x] **#200.18** Test restore root task: verify restored root tasks appear at top of Tasks section `#restore` `#test` (2026-01-25)
    > Covered by integration tests in tests/integration/test_restore_subtasks.py and fix in restore_command
  - [x] **#200.17** Test delete: verify tasks move to Deleted Tasks section at top `#delete` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestDelete
    > test_deleted_task_in_deleted_section
  - [x] **#200.16** Test archive: verify completed tasks move to Archived Tasks section at top `#archive` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestArchive
    > test_archived_task_in_archived_section and test_archived_tasks_in_archived_section
  - [x] **#200.15** Test completion: verify completed tasks stay in place (not moved) `#completion` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestCompletion
    > test_completed_task_stays_in_tasks_section
  - [x] **#200.14** Test ordering: verify newest-on-top for both root tasks and subtasks `#ordering` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestOrdering
    > test_root_tasks_newest_first and test_subtasks_newest_first
  - [x] **#200.13** Test indentation: verify proper 2-space indentation for each nesting level `#indentation` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestIndentation
    > test_subtask_indentation, test_note_indentation_for_root_task, test_note_indentation_for_subtask
  - [x] **#200.12** Test tag formatting: verify tags are wrapped in backticks `#tags` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestTagFormatting
    > test_tags_wrapped_in_backticks
  - [x] **#200.11** Test section separators: verify '---' between Tasks, Archived Tasks, and Deleted Tasks sections `#sections` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestSectionSeparators
    > test_separator_between_tasks_and_archived, test_separator_between_archived_and_deleted, test_separator_before_footer
  - [x] **#200.10** Test footer format: verify tool variant and timestamp formatting `#footer` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestFooterFormat
    > test_footer_contains_tool_variant, test_footer_contains_version, test_footer_contains_timestamp
  - [x] **#200.9** Test header format: verify warning header text and MCP/CLI variant detection `#header` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestHeaderFormat
    > test_header_contains_managed_file_warning and test_header_references_tool_variants
  - [x] **#200.8** Test spacing rules: one blank line between root tasks, zero blank lines between subtasks `#spacing` `#test` (2026-01-25)
    > Implemented in test_visual_standards.py::TestSpacingRules
    > test_blank_line_between_root_tasks and test_no_blank_lines_between_subtasks
  - [x] **#200.7** Run one-time migration on this repository's TODO.md to align with new standards `#migration` (2026-01-25)
    > Execute `reformat` command on TODO.md after implementation is complete. Verify no data loss.
  - [x] **#200.6** Document enhanced formatting behaviors and standards `#documentation` (2026-01-25)
    > Updated documentation files:
    > 1. docs/guides/GETTING_STARTED.md - Added comprehensive "TODO.md Format and Standards" section with Python CLI syntax (todo-ai)
    > 2. docs/guides/GETTING_STARTED.md - Updated Quick Reference and command examples to use Python CLI
    > 3. docs/guides/GETTING_STARTED.md - Added legacy shell script note for v2.x users
    > 4. README.md - Enhanced formatting standards section with Python CLI syntax and legacy note
  - [x] **#200.5** Update `reformat_command` to auto-fix new formatting violations `#code` `#fixer` (2026-01-25)
    > See docs/design/TODO_MD_VISUAL_STANDARDS_2026_V3.md for auto-fix rules. Must preserve data while fixing structure.
  - [x] **#200.4** Update `lint_command` to detect violations of new formatting standards `#code` `#linting` (2026-01-25)
    > See docs/design/TODO_MD_VISUAL_STANDARDS_2026_V3.md for validation rules (indentation, spacing, headers).
  - [x] **#200.3** Implement `FileOps` formatting logic and update mutation commands to strictly adhere to standards `#code` `#test` (2026-01-25)
    > Updated design doc with requirement: All mutation commands must produce compliant output to avoid linting/reformatting cycles.
    > See docs/design/TODO_MD_VISUAL_STANDARDS_2026_V3.md. Includes updating FileOps class and all mutation commands (add, modify, complete, delete, archive, move).
  - [x] **#200.2** Define enhanced formatting standards (e.g., spacing, indentation, headers) `#design` (2026-01-25)
    > See docs/design/TODO_MD_VISUAL_STANDARDS.md for initial assessment and draft standards.
    > Updated design doc with Header (v3.0 update) and Footer (placeholder) requirements.
    > Draft standards created and ready for review. See docs/design/TODO_MD_VISUAL_STANDARDS.md. Includes strict spacing, indentation, header/footer, and implementation requirements.
    > Updated design doc with Footer requirement: Include tool variant (todo.ai, cli, mcp).
    > Updated design doc with Tag formatting requirement: Tags must be wrapped in backticks (e.g., `#tag`).
    > Finalized spacing rules: 1 blank line between all root tasks, 0 blank lines between subtasks.
    > Updated Ordering section to define movement rules: Subtasks stay in place, Root tasks may move to Recently Completed.
    > Correction: Ordering is reverse chronological (newest on top) for all sections and lists. Updated design doc.
    > Clarified Ordering: Only 'archive' command moves root tasks to 'Recently Completed'. Simple completion keeps them in place.
    > Renamed 'Recently Completed' section to 'Archived Tasks' to clearly distinguish between completed state (in-place) and archived location (moved).
    > Refined Ordering section: Separated 'Completed Tasks' (in-place) and 'Archived Tasks' (moved) into distinct top-level list items.
    > Refined Positioning section: Explicitly stated that completion is a strict in-place update with NO sorting, to minimize diffs. Archival is the only move action for completed tasks.
    > Renamed design document to docs/design/TODO_MD_VISUAL_STANDARDS_2026_V3.md to explicitly identify year and version.
    > Design document approved. Proceeding to implementation tasks.
  - [x] **#200.1** Review current TODO.md format and identify inconsistencies or issues `#investigation` (2026-01-25)
- [x] **#199** Enhance `archive_command` to enforce parent-child grouping in archive section `#archive` `#enhancement` (2026-01-25)
  > Scenario to test:
  > 1. Parent #1 is already archived (at bottom of file).
  > 2. Subtask #1.1 is active (at top of file).
  > 3. Run `archive 1.1`.
  > 4. Result: #1.1 should move to bottom of file, immediately after #1.
  > Current behavior would leave #1.1 at top (but in Archive section), appearing before #1.
  - [x] **#199.2** Add regression test case: archiving orphaned subtasks should group them under the already-archived parent `#test` (2026-01-25)
  - [x] **#199.1** Implement logic to move archived subtasks immediately after their parent in the task list `#code` (2026-01-25)
- [x] **#198** Enhance linting to detect and fix out-of-order subtasks `#feature` `#linting` (2026-01-25)
  > Goal: Enforce the "newest on top" rule for subtasks, matching the behavior we recently fixed in task creation (#188).
  > Current fixers:
  > - `reformat_command`: Fixes indentation and checkboxes.
  > - `resolve_conflicts_command`: Fixes duplicate IDs.
  > We should likely add the reordering logic to `reformat_command` (optional or default?) or a new fixer. Given it changes content order, it should probably be part of `--reformat`.
  > Decision: Create a separate `reorder_command` (CLI: `reorder`) instead of overloading `reformat`.
  > Reasoning: Reordering changes content structure significantly, whereas reformat is cosmetic (indentation/checkboxes). Users should opt-in to reordering explicitly.
  - [x] **#198.4** Update documentation to reflect new linting capabilities `#documentation` (2026-01-25)
  - [x] **#198.3** Add unit tests for subtask ordering detection and fixing `#test` (2026-01-25)
  - [x] **#198.2** Implement `reorder_command` as a separate fixer for subtask ordering (distinct from `reformat_command`) `#code` (2026-01-25)
  - [x] **#198.1** Update `lint_command` to detect subtasks that violate reverse-chronological order (newest on top) `#code` (2026-01-25)
- [x] **#197** Verify MCP server reload with ordering test `#mcp` `#test` (2026-01-25)
  - [x] **#197.2** Second subtask (should be at top) `#test` (2026-01-25)
  - [x] **#197.1** First subtask (should be at bottom) `#test` (2026-01-25)
- [x] **#196** Enhance Pre-commit and CI/CD with todo-ai linting and validation `#cicd` `#infrastructure` `#quality` (2026-01-25)
  > Goal: Ensure `TODO.md` integrity is enforced automatically.
  > - Pre-commit: Fast checks (linting, formatting).
  > - CI: Deep checks (regression tests, logic validation).
  > This prevents bugs like the "orphaned subtasks" from slipping through.
  - [x] **#196.5** Update documentation to reflect new quality gates `#documentation` (2026-01-25)
  - [x] **#196.4** Add regression test suite to CI (running `tests/integration/`) to catch logic bugs like #195 `#cicd` `#test` (2026-01-25)
  - [x] **#196.3** Investigate adding auto-fix (`--reformat`) to pre-commit (optional/manual trigger?) `#investigation` (2026-01-25)
    > Investigation results for #196.3:
    > - `todo-ai reformat` fixes indentation and checkboxes.
    > - It is suitable for a pre-commit hook.
    > - Recommendation: Add as `todo-ai-reformat` hook before linting.
  - [x] **#196.2** Add `todo-ai --lint` step to GitHub Actions CI workflow `#cicd` (2026-01-25)
  - [x] **#196.1** Add `todo-ai --lint` to pre-commit hooks to block commits with invalid TODO.md `#infrastructure` (2026-01-25)
- [x] **#195** Fix bug: Archiving a task does not archive its subtasks `#bug` `#critical` (2026-01-25)
  > Decision: Archiving a task should ALWAYS archive its subtasks. We will not add an extra --with-subtasks option; instead, we will change the default behavior of archive_command to include subtasks automatically. This aligns with user expectations that archiving a parent implies archiving its children.
  > Status: Fix implemented (default with_subtasks=True), but verification test failed due to unexpected ordering of archived tasks.
  > Issue: Archived subtask (1.1) appears BEFORE parent (1) in 'Recently Completed', while we expected parent first.
  > Action: Pausing work on #195 to fix the underlying ordering inconsistency in #188 first. We will return to verify #195 once ordering is deterministic and correct.
  - [x] **#195.3** Verify fix with regression test `#test` (2026-01-25)
  - [x] **#195.2** Fix archive_command to recursively archive subtasks `#code` `#fix` (2026-01-25)
  - [x] **#195.1** Create reproduction test case for archive subtask failure `#test` (2026-01-25)
- [x] **#194** Hello World Test Task `#test` (2026-01-25)
- [x] **#192** Combine CLI and MCP server into single `todo-ai` executable with `serve` command and `--root` support `#design` `#mcp` `#refactor` (2026-01-25)
  - [x] **#192.7** Release beta version with unified executable for testing `#release` (2026-01-25)
  - [x] **#192.6** Update documentation to reflect unified executable and `serve` command `#documentation` (2026-01-25)
  - [x] **#192.5** Add test cases for `serve` command and argument parsing `#test` (2026-01-25)
  - [x] **#192.4** Implement `--root` argument support for MCP server (via `serve` command) `#code` `#implementation` (2026-01-25)
  - [x] **#192.3** Implement `serve` command in CLI to launch MCP server `#code` `#implementation` (2026-01-25)
  - [x] **#192.2** Create design document for unified executable architecture `#design` `#documentation` (2026-01-25)
  - [x] **#192.1** Investigate default parameters for well-defined MCP server (e.g. logging, transport options) `#investigation` `#mcp` (2026-01-25)
- [x] **#188** Investigate task ordering in Python version (todo-ai) - does not follow reverse order (newest on top) like shell script `#bug` `#python` (2026-01-25)
  > Shell script version (todo.ai) displays newest tasks first (reverse chronological). Python version (todo-ai) may not follow this same ordering. Need to investigate and ensure parity.
  - [x] **#188.2** Create reproduction test case for subtask ordering (newest should be on top) `#test` (2026-01-25)
  - [x] **#188.1** Fix task ordering inconsistency: Ensure subtasks follow the same reverse-chronological order (newest on top) as main tasks `#code` `#fix` (2026-01-25)
- [x] **#161** Fix issue#26: Migration path error when todo.ai installed to system directory `#bug` (2026-01-25)
  > Issue #26: When todo.ai installed to /usr/local/bin and config at /homeassistant/.todo.ai, update to v2.0.1 shows error: 'run_migrations:21: no matches found: /usr/local/bin/.todo.ai/migrations/v*_*.migrated'. Migration logic looks for .todo.ai next to script instead of working directory. Issue: https://github.com/fxstein/todo.ai/issues/26
  - [x] **#161.5** Verify fix works with both local and system-wide installations `#bug` (2026-01-25)
    > VERIFIED: Tested fix from different working directory (/tmp). Script correctly uses ORIGINAL_WORKING_DIR (/tmp) instead of script directory. Fixed glob error by using find instead of glob expansion. Fix works for both local and system-wide installations - migrations always run in user's working directory where .todo.ai exists.
  - [x] **#161.4** Fix migration path detection for system-wide installations `#bug` (2026-01-25)
    > FIXED: Added ORIGINAL_WORKING_DIR variable captured at script startup. Updated run_migrations() to use ORIGINAL_WORKING_DIR instead of $(pwd) for migrations_dir. This ensures migrations always run in the user's working directory (where .todo.ai exists), not the script's directory (e.g., /usr/local/bin). Fixes issue where update command changes directory to script_dir before executing new version, causing run_migrations() to look in wrong location.
  - [x] **#161.3** Test migration execution when installed to /usr/local/bin or /usr/bin `#bug` (2026-01-25)
  - [x] **#161.2** Review get_script_path() and migration system for system directory handling `#bug` (2026-01-25)
  - [x] **#161.1** Investigate migration path error: reproduce with system directory installation `#bug` (2026-01-25)
    > BUG IDENTIFIED: In update_tool() at line 5805, script changes directory to script_dir (e.g., /usr/local/bin) before executing new version. When run_migrations() is called, it uses $(pwd) which is now /usr/local/bin, so it looks for .todo.ai/migrations in wrong location. The .todo.ai directory should always be in the user's working directory, not next to the script. Fix: Capture original working directory at script startup and use it in run_migrations().
- [x] **#126** Fix issue#27: Setup coordinator automatically switches to enhanced mode without user consent (fixed - setup-coordination now preserves current mode) `#bug` (2026-01-25)
  - [x] **#126.4** Add tests to verify coordination setup doesn't change numbering mode `#bug` `#test` (2026-01-25)
  - [x] **#126.3** Fix setup-coordination to preserve current mode when configuring coordination (completed - fixed hardcoded enhanced mode) `#bug` (2026-01-25)
  - [x] **#126.2** Verify coordination should work with single-user mode without forcing enhanced (verified - validation supports single-user + coordination) `#bug` (2026-01-25)
  - [x] **#126.1** Investigate setup-coordination command mode switching logic (completed - found hardcoded mode: enhanced on line 3353) `#bug` (2026-01-25)
- [x] **#125** Overhaul bug reporting feature: eliminate prompts and improve formatting `#bug` `#feature` (2026-01-25)
  > Current implementation has basic markdown but needs improvement: (1) Create GitHub issue template (.github/ISSUE_TEMPLATE/bug_report.yml), (2) Use GitHub callout blocks (> [!NOTE], > [!WARNING]), (3) Better structure with proper sections, (4) Remove prompts for agent workflow, (5) Auto-collect all context without user input
  - [x] **#125.13** Update bug reporting design document with new implementation details `#docs` (2026-01-25)
    > Update docs/design/BUG_REPORTING_DESIGN.md: (1) Document GitHub issue template structure, (2) Explain callout block usage and markdown improvements, (3) Document agent vs human detection logic, (4) Add examples of new bug report format, (5) Document auto-labeling system, (6) Update template examples to match new generate_bug_report() implementation. Keep aligned with actual code.
  - [x] **#125.12** Test new bug report format with real GitHub issue creation `#test` (2026-01-25)
    > Implementation complete. Test before next release: (1) Set AI_AGENT=true to test agent flow, (2) Unset to test human flow, (3) Trigger error and call report-bug, (4) Verify markdown renders correctly, (5) Check labels applied, (6) Verify all context sections populated. Should test both flows to ensure proper detection and different behaviors.
    > Create test bug report with all new features: (1) Trigger error in test environment, (2) Run report-bug command, (3) Verify markdown renders correctly on GitHub (callout blocks, tables, code blocks), (4) Test with agent simulation (set AI_AGENT=true env var), (5) Verify duplicate detection still works, (6) Check auto-labels applied correctly, (7) Validate all context sections populated.
  - [x] **#125.11** Update cursor rules to reflect new agent-friendly bug reporting workflow `#docs` (2026-01-25)
    > Update .cursor/rules/todo.ai-bug-reporting.mdc: (1) Remove mention of user prompts for agents, (2) Add note that agents can use report-bug directly without prompts, (3) Humans still get confirmation prompts, (4) Show updated example of agent usage: 'When error occurs, call ./todo.ai report-bug and it will auto-submit'. Keep rule concise (<25 lines).
  - [x] **#125.10** Add intelligent error categorization and suggested labels `#feature` (2026-01-25)
    > Auto-detect error type from error message/context and suggest GitHub labels: (1) 'bug' always, (2) 'crash' if segfault/core dump, (3) 'performance' if timeout/slow, (4) 'data-loss' if file corruption, (5) 'coordination' if GitHub API/coordination issues, (6) OS-specific: 'macos', 'linux', 'wsl', (7) Shell-specific: 'zsh', 'bash'. Use pattern matching on error message. Add labels via gh issue create --label.
  - [x] **#125.9** Enhance context auto-collection: add git status, recent commands, TODO.md state `#code` (2026-01-25)
    > Expand collect_error_context() function: (1) Git status: branch, dirty state, last commit, (2) Shell history: last 5 commands from .todo.ai.log, (3) TODO.md state: active task count, mode, coordination type, (4) Environment: TERM, EDITOR, relevant env vars, (5) File context: if error in specific file, include relevant lines. Format all in collapsible sections to keep bug report clean.
  - [x] **#125.8** Remove prompts from suggest_bug_report() - make fully automated for AI agents `#code` (2026-01-25)
    > Currently suggest_bug_report() (line 6245) prompts user with 'Report this bug? (y/N)'. For agents: (1) Detect if running in AI agent context (check for CURSOR_AI, AI_AGENT env vars), (2) If agent: show preview but proceed automatically after 2 second delay, (3) If human: keep existing prompt workflow. Agent flow: Show preview → 'Auto-submitting in 2 seconds...' → Submit. Maintains user control for humans, enables automation for agents.
  - [x] **#125.7** Rewrite generate_bug_report() to use GitHub callout blocks and better markdown structure `#code` (2026-01-25)
    > Use GitHub markdown features: (1) Callout blocks for System Info (> [!NOTE]), Error sections (> [!WARNING]), (2) Clean section headers with --- separators, (3) Proper code blocks with language tags, (4) Collapsible <details> for logs, (5) Table format for system information. Mirror the structure from bug_report.yml template. Located in todo.ai around line 5834.
  - [x] **#125.6** Create GitHub issue template for bug reports (.github/ISSUE_TEMPLATE/bug_report.yml) `#feature` (2026-01-25)
    > Create .github/ISSUE_TEMPLATE/bug_report.yml with structured fields: Error Description (textarea), Command Used (input), Error Context (textarea), System Info (auto-filled), Logs (auto-attached). Use GitHub's form schema for issue templates. This will be used as the reference template for generate_bug_report() function.
  - [x] **#125.5** Test bug reporting flow with automated agent execution `#bug` `#test` (2026-01-25)
  - [x] **#125.4** Add context detection to auto-fill relevant information without prompts `#bug` (2026-01-25)
  - [x] **#125.3** Improve bug report formatting with better markdown structure `#bug` (2026-01-25)
  - [x] **#125.2** Update bug report template for better readability and structure `#bug` (2026-01-25)
  - [x] **#125.1** Eliminate user prompts - make bug reporting fully automated for AI agents `#bug` (2026-01-25)
- [x] **#189** Verify MCP server task creation with another test task `#mcp` `#test` (2026-01-24)
  > Why do programmers prefer dark mode? Because light attracts bugs. 🐛
- [x] **#186** Fix CI/CD release jobs skipping on tag pushes (validate-release and release) `#bug` (2026-01-24)
  > See docs/analysis/CI_CD_SILENT_FAILURE_ANALYSIS.md lines 73-227 for detailed analysis. Key files: .github/workflows/ci-cd.yml lines 384-488 (validate-release) and 489-549 (release).
  - [x] **#186.7** Verify release artifacts published successfully `#bug` (2026-01-24)
    > VERIFIED: v3.0.0b13 published successfully. GitHub release created with 7 assets (whl, tar.gz, attestations, install.sh, todo.ai, todo.bash). PyPI publish completed. First successful release since v3.0.0b7.
  - [x] **#186.6** Test fix with beta release tag (e.g., v3.0.0b8) `#bug` (2026-01-24)
    > SUCCESS with v3.0.0b13! All jobs ran: ✓ all-tests-pass (3s), ✓ validate-release (15s), ✓ release (35s). Published to GitHub with 7 assets. Root cause: all-tests-pass had if: always() instead of if: startsWith(github.ref, 'refs/tags/v'). Fixed by matching v3.0.0b7 config exactly.
    > CRITICAL FINDING: Fix was deployed but still failing! Tag detection works (is_tag=true confirmed in logs), all-tests-pass shows is_tag: 'true', but validate-release still skipped. Condition 'if: needs.changes.outputs.is_tag == true' present in v3.0.0b9 workflow but not evaluated correctly by GitHub Actions. Need to investigate GitHub Actions expression syntax or output type mismatch.
  - [x] **#186.5** Based on data, implement appropriate fix (Fix #1, #2, or #3 from analysis) `#bug` (2026-01-24)
    > COMPLETE FIX: all-tests-pass job had if: always() instead of if: startsWith(github.ref, 'refs/tags/v'). Matched v3.0.0b7 config for all three jobs (all-tests-pass, validate-release, release). Removed extra dependencies and invalid references.
    > ACTUAL ROOT CAUSE FOUND: Debug steps referenced needs.changes but changes wasn't in needs array! GitHub Actions skips jobs with invalid dependency references. Fixed by removing ALL needs.changes references and matching v3.0.0b7 config exactly.
    > FINAL FIX: The issue was needs: [all-tests-pass, changes] - having 'changes' dependency caused GitHub Actions to skip job. Removed 'changes' from needs array to match v3.0.0b7 (successful). Now only depends on all-tests-pass.
    > REVISED: Job output comparison didn't work. Switched to direct GitHub context: 'if: startsWith(github.ref, 'refs/tags/v')' - same approach as v3.0.0b7 (successful). This bypasses job outputs entirely, using reliable built-in context.
    > Restored 'if: needs.changes.outputs.is_tag == true' condition to validate-release job (line 420). This was removed in dd9a222 causing GitHub Actions to skip the job. Fix eliminates ambiguity about when job should run.
  - [x] **#186.4** Implement Fix #4: Add debug workflow context to validate-release job `#bug` (2026-01-24)
    > Added comprehensive debug logging: 1) changes job - verbose tag detection with condition evaluation, 2) all-tests-pass - outputs display, 3) validate-release - full workflow context with dependencies and outputs, 4) release - dependency outputs and conditional evaluation. Future-proofed for debugging.
    > Add debug step at line 393 in validate-release job. Show github.event_name, github.ref, github.ref_type, github.ref_name, and needs.changes.outputs.is_tag value.
  - [x] **#186.3** Verify tag detection logic in changes job (GITHUB_REF, GITHUB_REF_TYPE values) `#bug` (2026-01-24)
    > Tag detection VERIFIED working correctly. v3.0.0b8 logs show: Ref=refs/tags/v3.0.0b8, Ref type=tag, Ref name=v3.0.0b8. Both detection conditions (ref match and ref_type) work. Issue is NOT with tag detection.
  - [x] **#186.2** Analyze is_tag output propagation through changes → validate-release → release jobs `#bug` (2026-01-24)
    > Output chain correctly implemented but validate-release has NO if condition. GitHub Actions skips job without explicit condition. Solution: Restore 'if: needs.changes.outputs.is_tag == true' removed in dd9a222.
  - [x] **#186.1** Examine recent workflow runs to gather diagnostic data `#bug` (2026-01-24)
    > Root cause: Commit dd9a222 removed job-level if condition from validate-release. Changes job outputs is_tag=true correctly, but validate-release skips entirely (no logs). Hypothesis: output not exported or GitHub Actions implicit skipping.
    > Use 'gh run list --limit 10' and 'gh run view <run-id>' to examine recent tag push workflows. Check for is_tag values in changes job output.
- [x] **#185** Remove confirmation prompt when updating task notes `#feature` (2026-01-24)
- [x] **#184** Remove confirmation prompt when deleting task notes `#feature` (2026-01-24)
- [x] **#183** Optimize CI/CD pipeline to avoid full suite on minor changes `#infra` (2026-01-24)
  - [x] **#183.5** Document CI/CD optimization and release impact `#docs` (2026-01-24)
    > Doc: release/RELEASE_PROCESS.md includes CI/CD triggers + optimization section.
  - [x] **#183.4** Add tests/verification for CI/CD changes `#infra` `#skipped` (2026-01-24)
  - [x] **#183.3** Implement optimized CI/CD workflow changes `#infra` (2026-01-24)
  - [x] **#183.2** Design CI/CD optimization plan (path filters, tiers) `#infra` (2026-01-24)
  - [x] **#183.1** Analyze current CI/CD triggers and test matrix `#infra` (2026-01-24)
- [x] **#182** Design pinned project directory for todo.ai CLI (non-MCP) `#feature` (2026-01-23)
  > Overall summary: Design pinned project directory for todo.ai CLI (non-MCP).
  - [x] **#182.19** Execute beta release 3.0.0b7 `#release` (2026-01-23)
  - [x] **#182.18** Prepare beta release 3.0.0b7 `#release` (2026-01-23)
  - [x] **#182.17** Fix migrations root scoping for TODO_AI_ROOT `#bug` (2026-01-23)
    > Update run_migrations to use ROOT_DIR instead of ORIGINAL_WORKING_DIR so .todo.ai/migrations stays under TODO_AI_ROOT/--root.
  - [x] **#182.16** Execute beta release 3.0.0b6 `#release` (2026-01-23)
  - [x] **#182.15** Prepare beta release 3.0.0b6 `#release` (2026-01-23)
  - [x] **#182.14** Add temp submodule test for Python CLI show-root `#test` (2026-01-23)
    > Use temp repo/submodule fixture for Python CLI; call show-root and assert resolved root is superproject (not submodule).
  - [x] **#182.13** Add temp submodule test for shell show-root `#test` (2026-01-23)
    > Create temp git repo (one file + one commit) and add as submodule in tests; run show-root from submodule path, assert superproject root.
  - [x] **#182.12** Execute beta release 3.0.0b5 `#release` (2026-01-23)
    > Execute beta release only after explicit approval; wait for CI/CD completion before cleanup per release.sh workflow.
  - [x] **#182.11** Prepare beta release 3.0.0b5 `#release` (2026-01-23)
    > After fix lands, draft AI summary and run prepare for next beta; ensure summary commit is latest/near-latest to satisfy staleness check.
  - [x] **#182.10** Fix root resolution for nested submodules `#bug` (2026-01-23)
    > Investigate submodule root detection: use gitdir path (.git/modules/...) to locate superproject when --show-superproject-working-tree returns empty.
  - [x] **#182.9** Execute beta release 3.0.0b4 `#release` (2026-01-23)
  - [x] **#182.8** Prepare beta release 3.0.0b4 `#release` (2026-01-23)
  - [x] **#182.7** Update documentation and guides for pinned root feature `#docs` (2026-01-23)
  - [x] **#182.6** Implement and test missing feature parity in Python `#feature` (2026-01-23)
  - [x] **#182.5** Add tests for pinned directory behavior `#feature` (2026-01-23)
  - [x] **#182.4** Implement directory pinning for CLI `#feature` (2026-01-23)
  - [x] **#182.3** Design user-facing CLI/config behavior `#feature` (2026-01-23)
    > Design doc: docs/design/PINNED_PROJECT_DIRECTORY_DESIGN.md
  - [x] **#182.2** Evaluate options to pin directory safely `#feature` (2026-01-23)
    > Options doc: docs/analysis/PINNED_PROJECT_DIRECTORY_OPTIONS.md (recommended config-based pin, alternatives evaluated)
  - [x] **#182.1** Investigate current directory resolution & init flow `#feature` (2026-01-23)
    > Investigation doc: docs/analysis/PINNED_PROJECT_DIRECTORY_INVESTIGATION.md
- [x] **#181** Stabilize release process (no failures) `#release` (2026-01-23)
  > Investigation: execute preflight fails due to uncommitted files. In release.sh preflight check (around 'Check 3'), git status excludes only release/RELEASE_LOG.log and .todo.ai/.todo.ai.{serial,log}. It still flags release/RELEASE_NOTES.md and TODO.md, which are expected after prepare or task updates. Suggest extend exclusion list to include release/RELEASE_NOTES.md, release/.prepare_state, TODO.md and .todo.ai/.todo.ai.log so execute can proceed and then commit them in version commit (execute already stages TODO.md/.todo.ai and RELEASE_NOTES.md).
  > Focus on release.sh prepare/execute idempotency: keep RELEASE_NOTES.md for review without triggering auto-commit; ensure execute handles notes/log changes deterministically. Files: release/release.sh, release/RELEASE_NOTES.md, release/RELEASE_LOG.log.
  - [x] **#181.4** Add regression tests for release.sh prepare/execute workflow `#release` (2026-01-23)
  - [x] **#181.3** Harden execute flow (preflight, cleanup, retries) `#release` (2026-01-23)
  - [x] **#181.2** Fix release notes lifecycle so prepare/execute are clean `#release` (2026-01-23)
  - [x] **#181.1** Investigate current release blockers (preflight failures, notes handling) `#release` (2026-01-23)
- [x] **#180** Investigate missing --set-version in release.sh `#bug` (2026-01-23)
  > Implemented --set-version override in release/release.sh (format X.Y.Z or X.Y.ZbN) with version comparison and beta-cycle base validation; documented override usage and constraints in release/RELEASE_PROCESS.md.
  > Attempted to run './release/release.sh --set-version 3.0.0b3' after prepare; script errored with 'Unknown option: --set-version'. Current usage only lists --prepare/--execute/--abort/--beta/--summary. Need a supported way to override version for beta releases.
  - [x] **#180.3** Implement change and update docs/tests `#bug` (2026-01-23)
  - [x] **#180.2** Decide whether to add --set-version or document alternative `#bug` (2026-01-23)
  - [x] **#180.1** Confirm supported release.sh options and expected override workflow `#bug` (2026-01-23)
    > release.sh does not support --help; running ./release/release.sh --help returns 'Unknown option' but prints usage. Usage currently lists --prepare/--execute/--abort, --beta, --summary, --set-version, --dry-run.
- [x] **#179** Investigate release prepare failure on stale RELEASE_SUMMARY.md `#bug` (2026-01-23)
  > Prepare failed with stale summary warning: release.sh auto-detected release/RELEASE_SUMMARY.md (timestamp 2025-12-18) and aborted in non-interactive mode despite new release/AI_RELEASE_SUMMARY.md. Error surfaced on 'release.sh --prepare' after summary commit d5208d4.
  - [x] **#179.3** Implement fix and add regression test `#bug` (2026-01-23)
  - [x] **#179.2** Decide expected behavior for AI_RELEASE_SUMMARY.md vs RELEASE_SUMMARY.md `#bug` (2026-01-23)
  - [x] **#179.1** Reproduce stale summary detection in release.sh `#bug` (2026-01-23)
- [x] **#178** Fix issue#40: Subtasks assigned to wrong parent `#bug` (2026-01-17)
  > Investigate/fix in `todo_ai/cli/commands/__init__.py` add_subtask_command; tests in `tests/integration/test_cli.py` (add_subtasks_multiple_parents).
  - [x] **#178.3** Add tests for multiple parents/subtasks `#bug` (2026-01-17)
  - [x] **#178.2** Fix subtask insertion to correct parent `#bug` (2026-01-17)
  - [x] **#178.1** Investigate subtask placement logic `#bug` (2026-01-17)
- [x] **#177** Fix release process - PyPI must succeed before GitHub release `#critical` `#infrastructure` (2026-01-17)
  - [x] **#177.3** Move GitHub release to workflow (after PyPI success) `#infrastructure` (2026-01-17)
  - [x] **#177.2** Remove GitHub release creation from release.sh `#infrastructure` (2026-01-17)
  - [x] **#177.1** Update PyPI Trusted Publisher config to ci-cd.yml/release `#infrastructure` (2026-01-17)
- [x] **#176** Fix CI/CD dependency flaw - merge workflows with job dependencies `#critical` `#infrastructure` (2026-01-17)
- [x] **#175** Implement safeguards to prevent --no-verify from returning to codebase `#critical` `#infrastructure` (2026-01-17)
  - [x] **#175.3** Add CI/CD check to detect forbidden flags `#infrastructure` (2026-01-17)
  - [x] **#175.2** Add pytest test to detect forbidden flags `#infrastructure` (2026-01-17)
  - [x] **#175.1** Add pre-commit hook to detect forbidden flags `#infrastructure` (2026-01-17)
- [x] **#174** Set up PyPI project for todo-ai package `#release` (2026-01-17)
  > Changed PyPI package name from 'todo-ai' to 'ai-todo' (PyPI rejected original name as too similar to existing project). Updated pyproject.toml, README.md, and all documentation.
  > Using PyPI Trusted Publisher (OpenID Connect) - no API token needed. Requires: 1) Create PyPI project, 2) Add GitHub as trusted publisher, 3) Update GitHub Actions workflow to use OIDC.
  - [x] **#174.7** Test first beta release with trusted publisher `#testing` (2026-01-17)
  - [x] **#174.6** Update GitHub Actions workflow to use OIDC authentication `#infrastructure` (2026-01-17)
  - [x] **#174.5** Register GitHub as trusted publisher on PyPI `#setup` (2026-01-17)
  - [x] **#174.1** Create PyPI project 'todo-ai' (or verify name available) `#setup` (2026-01-17)
- [x] **#173** Fix release script bugs found during v3.0.0b1 attempt `#bug` (2026-01-17)
  - [x] **#173.12** Remove --no-verify from release script (ETERNALLY FORBIDDEN) `#critical` (2026-01-17)
  - [x] **#173.11** Fix pre-commit hook handling - committed files don't include hook fixes `#bug` (2026-01-17)
    > Root cause: Pre-commit hooks ran AFTER staging, fixed files in working dir, but retry logic committed unfixed version from index. Fix: Run pre-commit BEFORE staging to let hooks fix files first, then stage clean files.
  - [x] **#173.10** Fix todo.bash formatting issues causing CI failures `#bug` (2026-01-17)
  - [x] **#173.9** Auto-detect RELEASE_SUMMARY.md in prepare phase `#bug` (2026-01-17)
  - [x] **#173.8** Fix pathspec issue in pre-commit hook re-staging logic `#bug` (2026-01-17)
  - [x] **#173.7** Fix pre-commit hook timing - hooks modify files after staging `#bug` (2026-01-17)
  - [x] **#173.6** Investigate and handle uv.lock modifications during release `#bug` (2026-01-17)
  - [x] **#173.5** Add commit success verification after git commit `#bug` (2026-01-17)
  - [x] **#173.4** Fix commit error handling - remove error masking on line 1324 `#bug` (2026-01-17)
  - [x] **#173.3** Fix prepare side effects - leaves dirty working directory `#bug` (2026-01-17)
  - [x] **#173.2** Fix tag verification - fails even when versions are correct `#bug` (2026-01-17)
  - [x] **#173.1** Fix auto-commit logic - doesn't handle bash conversion artifacts properly `#bug` (2026-01-17)
    > Problem: todo.bash converted during --prepare (line 1034) but only added to git during --execute (lines 1297-1300). Leaves uncommitted file after prepare. Fix: Move bash conversion to execute phase OR commit it during prepare.
- [x] **#171** Improve CI/CD job grouping and naming `#cicd` `#enhancement` (2025-12-16)
  > Added 'needs: quality' dependency to all test jobs - tests won't run until code quality checks pass. Saves CI resources by failing fast on linting/typing/formatting issues.
  > Refactored to 3 separate jobs: 'Comprehensive Tests' (Py 3.14 × 3 OS, main only), 'Quick Tests' (Py 3.10-3.13 × 3 OS, main only), 'PR Tests' (Py 3.12 × ubuntu, PRs only). Creates clean grouping in GitHub Actions UI.
  > Added conditional job naming: '🔬 Comprehensive Tests' for Python 3.14 (full suite), '⚡ Quick Tests' for Python 3.10-3.13 (unit only). Makes GitHub Actions UI more readable and groups related tests.
- [x] **#170** Further optimize CI/CD: Granular test strategy `#cicd` `#optimization` (2025-12-16)
  > Main branch: Full tests only on Python 3.14 (3 OS × 1 version = 3 jobs), unit tests on 3.10-3.13 (3 OS × 4 versions = 12 jobs). PRs: Full tests on ubuntu + 3.12 (1 job). Total main: 15 jobs but most are fast unit-only.
- [x] **#169** Implement CI/CD optimizations from assessment `#cicd` `#optimization` (2025-12-16)
  - [x] **#169.3** Phase 3: Cleanup and documentation `#cicd` (2025-12-16)
  - [x] **#169.2** Phase 2: Optimize pre-commit configuration `#cicd` (2025-12-16)
  - [x] **#169.1** Phase 1: Refactor CI/CD workflow `#cicd` (2025-12-16)
- [x] **#48** Fix update logic error: new version update logic never executes (2025-11-02)
  - [x] **#48.4** Test update workflow: verify migrations execute in new version after update `#test` (2025-11-02)
  - [x] **#48.3** Implement update fix: execute new version's migrations and update logic before replacement `#code` (2025-11-02)
  - [x] **#48.2** Design solution: download → execute new version → replace old version `#docs` (2025-11-02)
  - [x] **#48.1** Research update execution pattern: how to execute new version's code after download `#research` (2025-11-02)
- [x] **#46** Fix release numbering bug: cursor rules migration incorrectly classified as PATCH instead of MINOR `#bug` (2025-11-02)
  - [x] **#46.6** Create mapping document: tags to release types with priority matrix showing numbering decisions `#docs` (2025-11-02)
  - [x] **#46.5** Test fix: verify cursor rules migration would be classified as MINOR with fix applied `#test` (2025-11-02)
  - [x] **#46.4** Handle ambiguous cases: migrations that affect users vs pure infrastructure changes `#code` (2025-11-02)
  - [x] **#46.3** Implement fix: check for functional changes in todo.ai before file-based classification `#code` (2025-11-02)
  - [x] **#46.2** Design fix: prioritize commit message prefixes (feat:) over file analysis for user-facing features `#docs` (2025-11-02)
  - [x] **#46.1** Investigate release numbering logic: why feat: commits with .cursor/rules/ changes are classified as PATCH `#research` (2025-11-02)
- [x] **#19** Move Deleted Tasks section below Recently Completed section `#setup` (2025-11-02)
- [x] **#7** Remove gitignore entry for .todo.ai directory - .todo.ai/ must be tracked in git `#git` `#setup` (2025-11-01)
- [x] **#5** Initialize repository structure and configuration `#repo` `#setup` (2025-11-01)
- [x] **#26** Rename .todo/ directory to .todo.ai/ `#setup` (2025-10-30)
- [x] **#25** Rename repository from todo to todo.ai `#setup` (2025-10-30)
- [x] **#23** Rename todo.ai to todo.ai `#setup` (2025-10-30)
- [x] **#22** Create update instructions and functions for todo.ai `#setup` (2025-10-30)
- [x] **#20** Create radically simplified README.md `#docs` (2025-10-30)
- [x] **#18** Fix TODO.md header upon initialization - use repo name dynamically `#fix` `#setup` (2025-10-30)
- [x] **#17** Create Cursor rules for repository `#docs` `#setup` (2025-10-30)
- [x] **#12** Final formatting test `#test` (2025-10-30)
- [x] **#11** Test new append method `#test` (2025-10-30)
- [x] **#8** Fix all sed -i calls to use sed_inplace for macOS compatibility `#fix` `#setup` (2025-10-30)
- [x] **#6** Update TODO.md template for this repository `#docs` `#setup` (2025-10-30)

---

## Deleted Tasks
- [D] **#252** Test task (deleted 2026-01-27, expires 2026-02-26)
- [D] **#249** Test coordination posting `#test` (deleted 2026-01-27, expires 2026-02-26)
- [D] **#248** Tell a joke `#test` (deleted 2026-01-27, expires 2026-02-26)
- [D] **#244** Parent task (deleted 2026-01-27, expires 2026-02-26)
- [D] **#243** Parent task (deleted 2026-01-27, expires 2026-02-26)
  - [D] **#51.3** Test update command from system-wide installation location `#test` (deleted 2026-01-27, expires 2026-02-26)
  - [D] **#51.2** Fix get_script_path() to handle system-wide installations in /usr/local/bin or /usr/bin `#code` (deleted 2026-01-27, expires 2026-02-26)
  - [D] **#51.1** Investigate get_script_path() function: how it detects script location when installed system-wide `#research` (deleted 2026-01-27, expires 2026-02-26)
  - [D] **#237.12** SAFETY: Develop mechanism to prevent premature archiving (task#205) `#design` `#safety` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.11** INFRA: Review MCP tool parameter naming consistency (task#190) `#infrastructure` `#mcp` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.10** INFRA: Harden MCP server setup for portability (task#191) `#infrastructure` `#mcp` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.9** POLISH: Update cursor rules to prefer MCP over CLI (task#187) `#cursor-rules` `#polish` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.8** POLISH: Complete unified naming migration (task#219) `#naming` `#polish` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.7** POLISH: Audit MCP/CLI tools for post-migration cleanup (task#234)  `#v3.0` `#polish` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.6** POLISH: Review and optimize embedded Cursor rules (task#235)  `#v3.0` `#polish` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.5** BUG: Fix show_task displaying deleted tasks incorrectly (task#222) `#bug` `#high` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.4** BUG: Fix delete task leaving orphaned subtasks (task#221) `#bug` `#high` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.3** CRITICAL: Final review and publish README.md (task#203.9) `#critical` `#documentation` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.2** CRITICAL: Complete release phase for Python refactor (task#163.52) `#critical` `#release` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#237.1** CRITICAL: Complete stable release phase (task#172.5) `#critical` `#release` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#233** Programmer jokes collection `#fun` `#joke` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.10** ['hip', 'hip'] — Sorry, I was just making a hip hop array. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.9** I would tell you a UDP joke, but you might not get it. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.8** Why was the JavaScript developer sad? Because he didn't Node how to Express himself. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.7** How many programmers does it take to change a light bulb? None, that's a hardware problem. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.6** Why do Java developers wear glasses? Because they don't C#. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.5** A programmer's wife tells him: 'Buy bread. If they have eggs, buy a dozen.' He comes home with 12 loaves. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.4** Why did the developer go broke? Because he used up all his cache. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.3** There are only 10 types of people in the world: those who understand binary and those who don't. (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.2** A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?' (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#233.1** Why do programmers prefer dark mode? Because light attracts bugs. (deleted 2026-01-26, expires 2026-02-25)
- [D] **#232** ['hip', 'hip'] — Sorry, I was just making a hip hop array. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#231** I would tell you a UDP joke, but you might not get it. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#230** Why was the JavaScript developer sad? Because he didn't Node how to Express himself. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#229** How many programmers does it take to change a light bulb? None, that's a hardware problem. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#228** Why do Java developers wear glasses? Because they don't C#. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#227** A programmer's wife tells him: 'Go to the store and buy a loaf of bread. If they have eggs, buy a dozen.' He comes home with 12 loaves. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#226** Why did the developer go broke? Because he used up all his cache. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#225** There are only 10 types of people in the world: those who understand binary and those who don't. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#224** A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?' `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#223** Why do programmers prefer dark mode? Because light attracts bugs. `#joke` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#220** Implement data directory migration (.todo.ai/ → .ai-todo/) `#implementation` `#migration` `#naming` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#220.3** Rename internal state files (.todo.ai.serial → .ai-todo.serial, .todo.ai.log → .ai-todo.log) `#code` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#220.2** Update config.py to use .ai-todo/ paths `#code` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#220.1** Update FileOps to use .ai-todo/ as default data directory `#code` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#215** Collection of 10 Funny Jokes `#fun` `#jokes` (deleted 2026-01-26, expires 2026-02-25)
  - [D] **#215.10** !false (It's funny because it's true). (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: The exclamation mark '!' is the logical NOT operator in many programming languages. Therefore, '!false' reads as 'NOT false', which evaluates to 'true'.
  - [D] **#215.9** 0 is false and 1 is true, right? 1. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: In computer logic, the number 0 represents 'False' and 1 represents 'True'. When asked 'right?', instead of saying 'Yes' or 'True', the programmer answers '1'.
  - [D] **#215.8** A programmer's wife tells him, 'While you're at the store, get some milk.' He never comes back. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: This refers to a 'while loop' in code. The instruction 'While you are at the store' is interpreted as a condition: as long as he is at the store, he must keep getting milk. Since he never leaves the store (the condition remains true), he is stuck in an infinite loop.
  - [D] **#215.7** Why do Java programmers wear glasses? Because they don't C#. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: C# (pronounced 'C-Sharp') is a popular programming language. The joke is a pun on 'see sharp' (to see clearly). Java is a different language, implying they can't 'see sharp'.
  - [D] **#215.6** What is a programmer's favorite hangout place? Foo Bar. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: 'Foo' and 'Bar' are the standard placeholder names used in programming tutorials and examples (like 'John Doe'). 'Foo Bar' sounds like the name of a drinking establishment.
  - [D] **#215.5** Why did the programmer quit his job? He didn't get arrays. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: An 'array' is a fundamental data structure in programming (a list of items). The joke relies on the pun that 'arrays' sounds exactly like 'a raise' (an increase in salary).
  - [D] **#215.4** There are 10 types of people in the world: those who understand binary, and those who don't. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: Binary is a number system used by computers consisting only of 0s and 1s. In binary, '10' represents the number 2. So the joke actually says 'There are two types of people'.
  - [D] **#215.3** A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?' (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: SQL is a language for databases. Data is stored in 'tables'. A 'JOIN' is a specific command used to combine data from two different tables.
  - [D] **#215.2** How many programmers does it take to change a light bulb? None, that's a hardware problem. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: Programmers write software (code) and often distinguish it from hardware (physical devices like light bulbs). If a physical device fails, they jokingly claim it's not their department.
  - [D] **#215.1** Why do programmers prefer dark mode? Because light attracts bugs. (deleted 2026-01-26, expires 2026-02-25)
    > Explanation: In programming, software errors are called 'bugs'. Real bugs (insects) are attracted to light sources. Dark mode is a screen setting that emits less light, thus 'avoiding bugs'.
- [D] **#214** Test task for whitespace verification `#test` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#208** Test task from root (deleted 2026-01-25, expires 2026-02-24)
- [D] **#193** Implement 'start task' command to track task progress and status `#design` `#feature` (deleted 2026-01-25, expires 2026-02-24)
  > Key questions to answer:
  > 1. Does 'starting' a task imply a status change (e.g. to 'in-progress')?
  > 2. Should we support time tracking (start/stop)?
  > 3. How does this interact with todo.txt format (e.g. priority changes)?
  > 4. Should this trigger any external integrations?
  - [D] **#193.7** Update documentation with 'start' command usage `#documentation` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.6** Add unit and integration tests for 'start' command `#test` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.5** Implement 'start_task' tool in MCP server `#code` `#mcp` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.4** Implement 'start' command in CLI `#code` `#implementation` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.3** Create design document for 'start' command architecture `#design` `#documentation` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.2** Design the 'start' functionality: status changes, timers, assignments, etc. `#design` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.1** Research existing 'start' command patterns in other todo apps and define requirements `#research` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#174.4** Test PyPI authentication with manual upload `#testing` (deleted 2025-12-16, expires 2026-01-15)
  - [D] **#174.3** Add PYPI_API_TOKEN to GitHub secrets `#setup` (deleted 2025-12-16, expires 2026-01-15)
  - [D] **#174.2** Generate PyPI API token with upload permissions `#setup` (deleted 2025-12-16, expires 2026-01-15)
- [D] **#168** Phase 10: Enhanced Parsing (Pre-requisite) - Update FileOps._parse_markdown() to capture non-task lines in Tasks section `#code` (deleted 2025-12-15, expires 2026-01-14)
- [D] **#162** Test task for modify bug fix - MODIFIED `#test` (deleted 2025-12-12, expires 2026-01-11)
  - [D] **#136.9** Verify note positioning remains correct after multiple subtask additions `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.8** Test: add second subtask when first subtask already exists with notes `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.7** Test: task with multiple notes + add subtask (all notes stay with parent) `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.6** Test: task with note + add first subtask (note should stay with parent) `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.5** Implement fix: modify add_subtask to skip over blockquotes before insertion `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.4** Design solution: insert subtasks after task AND any following notes `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.3** Analyze note detection: how to identify and skip over notes when inserting subtasks `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.2** Investigate add_subtask function: find where subtask insertion occurs `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.1** Reproduce bug: create task with note, add subtask, verify note is split `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#28.4** Update SERIAL_FILE path reference in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#28.3** Update LOG_FILE path reference in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#28.2** Rename .todo_serial to .todo.ai_serial using git mv `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#28.1** Rename .todo.log to .todo.ai.log using git mv `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.10** Update .cursorrules to reference .todo.ai/ instead of .todo/ `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.9** Verify git tracking of .todo.ai/ `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.8** Test script execution after rename `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.7** Update any documentation files `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.6** Update README.md if it mentions .todo/ `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.5** Update environment variable names (TODO_SERIAL, TODO_LOG) `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.4** Update all references to .todo/ in script code `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.3** Update LOG_FILE path in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.2** Update SERIAL_FILE path in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.1** Rename directory using git mv: .todo/ -> .todo.ai/ `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.6** Update header comment in todo.ai `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.5** Update README.md repository references `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.4** Update SCRIPT_URL in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.3** Update REPO_URL in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.2** Update local git remote URL after GitHub rename `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.1** Rename repository on GitHub (manual step) `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.10** Test update command works with new filename `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.9** Test installation and execution after rename `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.8** Update all inline comments and documentation in script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.7** Update init_cursor_rules() to reference todo.ai `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.6** Update help text and show_usage() examples `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.5** Update Cursor rules to reference todo.ai instead of todo.zsh `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.4** Update self-references in update_tool() function `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.3** Update TODO.md template path references `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.2** Update all references in README.md (installation, examples, commands) `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.1** Update script filename: todo.zsh -> todo.ai `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#22.3** Option 3: Auto-check version on startup (informational only) `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#22.2** Option 2: Add version info + update command `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#22.1** Option 1: Simple re-download instruction in README `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#18.1** Remove path from todo.ai upon init `#fix` `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#17.3** Ensure TODO.md and .todo.ai/ are always committed together `#rules` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#17.1** Enforce todo.ai usage for all task tracking `#rules` `#todo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.9** Create developer/ directory and setup script for automated linter installation, update design doc to reference the setup script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.8** Investigate installation options for linters (markdownlint-cli2, yamllint, jq): document direct installation methods and agent-assisted installation for developers after forking the repo, reference GIT_HOOKS_DESIGN.md `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.7** TODO.md linting: implement validate_todo() using existing ./todo.ai --lint command, validates task IDs, subtask relationships, formatting, tags, and section structure `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.6** Create setup script at scripts/setup-git-hooks.sh to install pre-commit hook and check for required linting tools `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.5** Create pre-commit hook script at scripts/pre-commit-hook.sh with file type detection, error aggregation, and exit handling `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.4** TODO.md linting: implement validate_todo() using existing ./todo.ai --lint command, validates task IDs, subtask relationships, formatting, tags, and section structure `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.3** JSON linting: implement validate_json() using jq (recommended) or jsonlint/Python (fallback), validate .json files for syntax errors `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.2** YAML linting: implement validate_yaml() using yamllint (recommended) or yq (fallback), validate .yml/.yaml files, create .yamllint config with relaxed rules for .mdc front matter `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.1** Markdown linting: implement validate_markdown() using markdownlint-cli2 (recommended) or mdl (fallback), validate .md/.mdc files, create .markdownlint.yaml config `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#7.1** Add setup instructions documenting that .todo.ai/ must be tracked in git `#docs` (deleted 2025-11-02, expires 2025-12-02)

---

<!-- TASK_METADATA
# Format: task_id:created_at[:updated_at]
11:2026-01-27T23:50:41.505242:2026-01-27T23:51:37.635568
12:2026-01-27T23:50:41.505237:2026-01-27T23:51:37.635564
125:2026-01-27T23:50:41.503167:2026-01-27T23:50:41.503168
125.1:2026-01-27T23:50:41.503247:2026-01-27T23:51:37.631726
125.10:2026-01-27T23:50:41.503192:2026-01-27T23:50:41.503193
125.11:2026-01-27T23:50:41.503186:2026-01-27T23:50:41.503187
125.12:2026-01-27T23:50:41.503179:2026-01-27T23:50:41.503181
125.13:2026-01-27T23:50:41.503173:2026-01-27T23:50:41.503174
125.2:2026-01-27T23:50:41.503241:2026-01-27T23:50:41.503242
125.3:2026-01-27T23:50:41.503236:2026-01-27T23:50:41.503237
125.4:2026-01-27T23:50:41.503231:2026-01-27T23:51:37.631713
125.5:2026-01-27T23:50:41.503226:2026-01-27T23:51:37.631709
125.6:2026-01-27T23:50:41.503219:2026-01-27T23:50:41.503221
125.7:2026-01-27T23:50:41.503213:2026-01-27T23:50:41.503215
125.8:2026-01-27T23:50:41.503204:2026-01-27T23:50:41.503208
125.9:2026-01-27T23:50:41.503198:2026-01-27T23:50:41.503199
126:2026-01-27T23:50:41.503138:2026-01-27T23:51:37.631640
126.1:2026-01-27T23:50:41.503161:2026-01-27T23:51:37.631657
126.2:2026-01-27T23:50:41.503156:2026-01-27T23:51:37.631653
126.3:2026-01-27T23:50:41.503149:2026-01-27T23:51:37.631649
126.4:2026-01-27T23:50:41.503143:2026-01-27T23:50:41.503144
127:2026-01-27T23:50:41.502101:2026-01-27T23:51:37.630720
128:2026-01-27T23:50:41.502095:2026-01-27T23:51:37.630716
129:2026-01-27T23:50:41.498488:2026-01-29T02:09:45.957100
129.1:2026-01-27T23:50:41.498495:2026-01-29T02:09:45.957095
129.2:2026-01-27T23:50:41.498493:2026-01-29T02:09:45.957098
129.3:2026-01-27T23:50:41.498491:2026-01-29T02:09:45.957099
136.1:2026-01-27T23:50:41.506061:2026-01-27T23:51:37.636306
136.2:2026-01-27T23:50:41.506053:2026-01-27T23:50:41.506054
136.3:2026-01-27T23:50:41.506046:2026-01-27T23:51:37.636290
136.4:2026-01-27T23:50:41.506038:2026-01-27T23:51:37.636281
136.5:2026-01-27T23:50:41.506030:2026-01-27T23:51:37.636273
136.6:2026-01-27T23:50:41.506020:2026-01-27T23:51:37.636265
136.7:2026-01-27T23:50:41.506012:2026-01-27T23:50:41.506013
136.8:2026-01-27T23:50:41.506004:2026-01-27T23:50:41.506005
136.9:2026-01-27T23:50:41.505997:2026-01-27T23:51:37.636240
15.1:2026-01-27T23:50:41.506414:2026-01-27T23:51:37.636695
15.2:2026-01-27T23:50:41.506405:2026-01-27T23:51:37.636686
15.3:2026-01-27T23:50:41.506394:2026-01-27T23:51:37.636676
15.4:2026-01-27T23:50:41.506385:2026-01-27T23:50:41.506386
15.5:2026-01-27T23:50:41.506377:2026-01-27T23:51:37.636658
15.6:2026-01-27T23:50:41.506369:2026-01-27T23:51:37.636649
15.7:2026-01-27T23:50:41.506360:2026-01-27T23:51:37.636634
15.8:2026-01-27T23:50:41.506351:2026-01-27T23:51:37.636624
15.9:2026-01-27T23:50:41.506342:2026-01-27T23:51:37.636614
161:2026-01-27T23:50:41.503102:2026-01-27T23:50:41.503103
161.1:2026-01-27T23:50:41.503131:2026-01-27T23:50:41.503133
161.2:2026-01-27T23:50:41.503126:2026-01-27T23:51:37.631630
161.3:2026-01-27T23:50:41.503121:2026-01-27T23:51:37.631626
161.4:2026-01-27T23:50:41.503114:2026-01-27T23:50:41.503116
161.5:2026-01-27T23:50:41.503108:2026-01-27T23:50:41.503110
162:2026-01-27T23:50:41.505988:2026-01-27T23:50:41.505989
163:2026-01-27T23:50:41.501267:2026-01-27T23:50:41.501269
163.1:2026-01-27T23:50:41.502089:2026-01-27T23:50:41.502090
163.10:2026-01-27T23:50:41.502037:2026-01-27T23:51:37.630670
163.11:2026-01-27T23:50:41.502031:2026-01-27T23:50:41.502032
163.12:2026-01-27T23:50:41.502026:2026-01-27T23:51:37.630661
163.13:2026-01-27T23:50:41.502020:2026-01-27T23:50:41.502021
163.14:2026-01-27T23:50:41.502015:2026-01-27T23:51:37.630652
163.15:2026-01-27T23:50:41.502009:2026-01-27T23:51:37.630648
163.16:2026-01-27T23:50:41.502003:2026-01-27T23:51:37.630644
163.17:2026-01-27T23:50:41.501997:2026-01-27T23:51:37.630639
163.18:2026-01-27T23:50:41.501990:2026-01-27T23:50:41.501992
163.19:2026-01-27T23:50:41.501982:2026-01-27T23:51:37.630627
163.2:2026-01-27T23:50:41.502084:2026-01-27T23:51:37.630707
163.20:2026-01-27T23:50:41.501454:2026-01-27T23:51:37.630616
163.21:2026-01-27T23:50:41.501449:2026-01-27T23:51:37.630611
163.22:2026-01-27T23:50:41.501443:2026-01-27T23:51:37.630605
163.23:2026-01-27T23:50:41.501438:2026-01-27T23:51:37.630593
163.24:2026-01-27T23:50:41.501432:2026-01-27T23:50:41.501433
163.25:2026-01-27T23:50:41.501427:2026-01-27T23:51:37.630584
163.26:2026-01-27T23:50:41.501421:2026-01-27T23:50:41.501422
163.27:2026-01-27T23:50:41.501416:2026-01-27T23:51:37.630574
163.28:2026-01-27T23:50:41.501410:2026-01-27T23:50:41.501411
163.29:2026-01-27T23:50:41.501405:2026-01-27T23:51:37.630566
163.3:2026-01-27T23:50:41.502078:2026-01-27T23:50:41.502079
163.30:2026-01-27T23:50:41.501400:2026-01-27T23:51:37.630561
163.31:2026-01-27T23:50:41.501394:2026-01-27T23:51:37.630556
163.32:2026-01-27T23:50:41.501387:2026-01-27T23:50:41.501389
163.33:2026-01-27T23:50:41.501381:2026-01-27T23:50:41.501382
163.34:2026-01-27T23:50:41.501376:2026-01-27T23:51:37.630532
163.35:2026-01-27T23:50:41.501371:2026-01-27T23:51:37.630527
163.36:2026-01-27T23:50:41.501365:2026-01-27T23:51:37.630523
163.37:2026-01-27T23:50:41.501360:2026-01-27T23:51:37.630519
163.38:2026-01-27T23:50:41.501355:2026-01-27T23:51:37.630514
163.39:2026-01-27T23:50:41.501349:2026-01-27T23:50:41.501350
163.4:2026-01-27T23:50:41.502073:2026-01-27T23:51:37.630698
163.40:2026-01-27T23:50:41.501344:2026-01-27T23:51:37.630506
163.41:2026-01-27T23:50:41.501339:2026-01-27T23:51:37.630501
163.42:2026-01-27T23:50:41.501333:2026-01-27T23:51:37.630496
163.43:2026-01-27T23:50:41.501327:2026-01-27T23:51:37.630492
163.44:2026-01-27T23:50:41.501322:2026-01-27T23:51:37.630488
163.45:2026-01-27T23:50:41.501315:2026-01-27T23:51:37.630483
163.46:2026-01-27T23:50:41.501309:2026-01-27T23:50:41.501310
163.47:2026-01-27T23:50:41.501304:2026-01-27T23:51:37.630470
163.48:2026-01-27T23:50:41.501298:2026-01-27T23:51:37.630466
163.49:2026-01-27T23:50:41.501292:2026-01-27T23:50:41.501293
163.5:2026-01-27T23:50:41.502067:2026-01-27T23:50:41.502068
163.50:2026-01-27T23:50:41.501287:2026-01-27T23:51:37.630456
163.51:2026-01-27T23:50:41.501281:2026-01-27T23:51:37.630451
163.52:2026-01-27T23:50:41.501275:2026-01-27T23:50:41.501276
163.6:2026-01-27T23:50:41.502061:2026-01-27T23:51:37.630689
163.7:2026-01-27T23:50:41.502055:2026-01-27T23:50:41.502056
163.8:2026-01-27T23:50:41.502049:2026-01-27T23:50:41.502050
163.9:2026-01-27T23:50:41.502042:2026-01-27T23:50:41.502043
164:2026-01-27T23:50:41.501261:2026-01-27T23:51:37.630435
165:2026-01-27T23:50:41.501256:2026-01-27T23:51:37.630431
166:2026-01-27T23:50:41.501250:2026-01-27T23:50:41.501251
168:2026-01-27T23:50:41.505981:2026-01-27T23:51:37.636224
169:2026-01-27T23:50:41.503740:2026-01-27T23:51:37.633940
169.1:2026-01-27T23:50:41.503756:2026-01-27T23:51:37.633958
169.2:2026-01-27T23:50:41.503750:2026-01-27T23:50:41.503751
169.3:2026-01-27T23:50:41.503745:2026-01-27T23:51:37.633946
17:2026-01-27T23:50:41.505227:2026-01-27T23:50:41.505228
17.1:2026-01-27T23:50:41.506333:2026-01-27T23:51:37.636605
17.3:2026-01-27T23:50:41.506325:2026-01-27T23:50:41.506326
170:2026-01-27T23:50:41.503733:2026-01-27T23:50:41.503735
171:2026-01-27T23:50:41.503724:2026-01-27T23:50:41.503728
172:2026-01-27T23:50:41.501205:2026-01-27T23:50:41.501207
172.1:2026-01-27T23:50:41.501243:2026-01-27T23:50:41.501245
172.2:2026-01-27T23:50:41.501236:2026-01-27T23:50:41.501238
172.3:2026-01-27T23:50:41.501229:2026-01-27T23:50:41.501231
172.4:2026-01-27T23:50:41.501222:2026-01-27T23:50:41.501224
172.5:2026-01-27T23:50:41.501212:2026-01-27T23:50:41.501216
173:2026-01-27T23:50:41.503653:2026-01-27T23:50:41.503654
173.1:2026-01-27T23:50:41.503717:2026-01-27T23:50:41.503718
173.10:2026-01-27T23:50:41.503670:2026-01-27T23:51:37.633854
173.11:2026-01-27T23:50:41.503664:2026-01-27T23:50:41.503665
173.12:2026-01-27T23:50:41.503659:2026-01-27T23:51:37.633841
173.2:2026-01-27T23:50:41.503711:2026-01-27T23:50:41.503712
173.3:2026-01-27T23:50:41.503706:2026-01-27T23:50:41.503707
173.4:2026-01-27T23:50:41.503701:2026-01-27T23:51:37.633888
173.5:2026-01-27T23:50:41.503696:2026-01-27T23:51:37.633883
173.6:2026-01-27T23:50:41.503691:2026-01-27T23:51:37.633877
173.7:2026-01-27T23:50:41.503686:2026-01-27T23:51:37.633871
173.8:2026-01-27T23:50:41.503680:2026-01-27T23:50:41.503681
173.9:2026-01-27T23:50:41.503675:2026-01-27T23:50:41.503676
174:2026-01-27T23:50:41.503625:2026-01-27T23:50:41.503628
174.1:2026-01-27T23:50:41.503648:2026-01-27T23:51:37.633830
174.2:2026-01-27T23:50:41.505972:2026-01-27T23:51:37.636215
174.3:2026-01-27T23:50:41.505964:2026-01-27T23:50:41.505965
174.4:2026-01-27T23:50:41.505957:2026-01-27T23:51:37.636193
174.5:2026-01-27T23:50:41.503643:2026-01-27T23:51:37.633824
174.6:2026-01-27T23:50:41.503638:2026-01-27T23:51:37.633818
174.7:2026-01-27T23:50:41.503632:2026-01-27T23:50:41.503633
175:2026-01-27T23:50:41.503605:2026-01-27T23:51:37.633781
175.1:2026-01-27T23:50:41.503620:2026-01-27T23:51:37.633798
175.2:2026-01-27T23:50:41.503615:2026-01-27T23:51:37.633793
175.3:2026-01-27T23:50:41.503610:2026-01-27T23:51:37.633787
176:2026-01-27T23:50:41.503599:2026-01-27T23:51:37.633775
177:2026-01-27T23:50:41.503578:2026-01-27T23:51:37.633751
177.1:2026-01-27T23:50:41.503594:2026-01-27T23:51:37.633769
177.2:2026-01-27T23:50:41.503588:2026-01-27T23:50:41.503589
177.3:2026-01-27T23:50:41.503583:2026-01-27T23:51:37.633757
178:2026-01-27T23:50:41.503554:2026-01-27T23:50:41.503556
178.1:2026-01-27T23:50:41.503570:2026-01-27T23:50:41.503571
178.2:2026-01-27T23:50:41.503565:2026-01-27T23:50:41.503566
178.3:2026-01-27T23:50:41.503560:2026-01-27T23:50:41.503561
179:2026-01-27T23:50:41.503533:2026-01-27T23:50:41.503534
179.1:2026-01-27T23:50:41.503549:2026-01-27T23:50:41.503550
179.2:2026-01-27T23:50:41.503544:2026-01-27T23:51:37.633694
179.3:2026-01-27T23:50:41.503539:2026-01-27T23:51:37.633687
18:2026-01-27T23:50:41.505222:2026-01-27T23:50:41.505223
18.1:2026-01-27T23:50:41.506318:2026-01-27T23:51:37.636589
180:2026-01-27T23:50:41.503510:2026-01-27T23:50:41.503512
180.1:2026-01-27T23:50:41.503527:2026-01-27T23:50:41.503528
180.2:2026-01-27T23:50:41.503522:2026-01-27T23:51:37.633659
180.3:2026-01-27T23:50:41.503517:2026-01-27T23:51:37.633653
181:2026-01-27T23:50:41.503482:2026-01-27T23:50:41.503484
181.1:2026-01-27T23:50:41.503505:2026-01-27T23:51:37.633635
181.2:2026-01-27T23:50:41.503499:2026-01-27T23:50:41.503500
181.3:2026-01-27T23:50:41.503494:2026-01-27T23:50:41.503495
181.4:2026-01-27T23:50:41.503489:2026-01-27T23:51:37.633594
182:2026-01-27T23:50:41.503361:2026-01-27T23:50:41.503362
182.1:2026-01-27T23:50:41.503476:2026-01-27T23:50:41.503477
182.10:2026-01-27T23:50:41.503426:2026-01-27T23:50:41.503427
182.11:2026-01-27T23:50:41.503420:2026-01-27T23:50:41.503421
182.12:2026-01-27T23:50:41.503413:2026-01-27T23:50:41.503415
182.13:2026-01-27T23:50:41.503406:2026-01-27T23:50:41.503407
182.14:2026-01-27T23:50:41.503400:2026-01-27T23:50:41.503401
182.15:2026-01-27T23:50:41.503390:2026-01-27T23:50:41.503391
182.16:2026-01-27T23:50:41.503385:2026-01-27T23:50:41.503386
182.17:2026-01-27T23:50:41.503379:2026-01-27T23:50:41.503381
182.18:2026-01-27T23:50:41.503374:2026-01-27T23:51:37.631832
182.19:2026-01-27T23:50:41.503369:2026-01-27T23:51:37.631828
182.2:2026-01-27T23:50:41.503470:2026-01-27T23:50:41.503471
182.3:2026-01-27T23:50:41.503464:2026-01-27T23:50:41.503465
182.4:2026-01-27T23:50:41.503459:2026-01-27T23:51:37.633489
182.5:2026-01-27T23:50:41.503453:2026-01-27T23:50:41.503454
182.6:2026-01-27T23:50:41.503447:2026-01-27T23:51:37.633480
182.7:2026-01-27T23:50:41.503442:2026-01-27T23:51:37.633475
182.8:2026-01-27T23:50:41.503437:2026-01-27T23:51:37.633471
182.9:2026-01-27T23:50:41.503431:2026-01-27T23:50:41.503432
183:2026-01-27T23:50:41.503328:2026-01-27T23:50:41.503329
183.1:2026-01-27T23:50:41.503356:2026-01-27T23:51:37.631819
183.2:2026-01-27T23:50:41.503351:2026-01-27T23:51:37.631815
183.3:2026-01-27T23:50:41.503345:2026-01-27T23:50:41.503346
183.4:2026-01-27T23:50:41.503340:2026-01-27T23:51:37.631800
183.5:2026-01-27T23:50:41.503334:2026-01-27T23:50:41.503335
184:2026-01-27T23:50:41.503323:2026-01-27T23:51:37.631786
185:2026-01-27T23:50:41.503317:2026-01-27T23:50:41.503318
186:2026-01-27T23:50:41.503259:2026-01-27T23:50:41.503260
186.1:2026-01-27T23:50:41.503311:2026-01-27T23:50:41.503313
186.2:2026-01-27T23:50:41.503304:2026-01-27T23:50:41.503306
186.3:2026-01-27T23:50:41.503297:2026-01-27T23:50:41.503299
186.4:2026-01-27T23:50:41.503289:2026-01-27T23:50:41.503292
186.5:2026-01-27T23:50:41.503279:2026-01-27T23:50:41.503284
186.6:2026-01-27T23:50:41.503271:2026-01-27T23:50:41.503274
186.7:2026-01-27T23:50:41.503265:2026-01-27T23:50:41.503266
187:2026-01-27T23:50:41.501137:2026-01-27T23:50:41.501139
187.1:2026-01-27T23:50:41.501199:2026-01-27T23:51:37.630386
187.10:2026-01-27T23:50:41.501144:2026-01-27T23:51:37.630338
187.2:2026-01-27T23:50:41.501194:2026-01-27T23:51:37.630381
187.3:2026-01-27T23:50:41.501188:2026-01-27T23:51:37.630371
187.4:2026-01-27T23:50:41.501182:2026-01-27T23:51:37.630366
187.5:2026-01-27T23:50:41.501175:2026-01-27T23:51:37.630362
187.6:2026-01-27T23:50:41.501169:2026-01-27T23:50:41.501170
187.7:2026-01-27T23:50:41.501163:2026-01-27T23:51:37.630352
187.8:2026-01-27T23:50:41.501156:2026-01-27T23:51:37.630347
187.9:2026-01-27T23:50:41.501150:2026-01-27T23:51:37.630343
188:2026-01-27T23:50:41.503085:2026-01-27T23:50:41.503086
188.1:2026-01-27T23:50:41.503097:2026-01-27T23:51:37.631603
188.2:2026-01-27T23:50:41.503091:2026-01-27T23:51:37.631598
189:2026-01-27T23:50:41.503252:2026-01-27T23:50:41.503254
19:2026-01-27T23:50:41.505101:2026-01-27T23:50:41.505102
190:2026-01-27T23:50:41.501131:2026-01-27T23:50:41.501132
191:2026-01-27T23:50:41.501091:2026-01-27T23:50:41.501092
191.1:2026-01-27T23:50:41.501125:2026-01-27T23:51:37.630312
191.2:2026-01-27T23:50:41.501119:2026-01-27T23:50:41.501120
191.3:2026-01-27T23:50:41.501114:2026-01-27T23:51:37.630302
191.4:2026-01-27T23:50:41.501109:2026-01-27T23:51:37.630298
191.5:2026-01-27T23:50:41.501103:2026-01-27T23:51:37.630293
191.6:2026-01-27T23:50:41.501097:2026-01-27T23:50:41.501098
192:2026-01-27T23:50:41.503040:2026-01-27T23:50:41.503041
192.1:2026-01-27T23:50:41.503079:2026-01-27T23:51:37.631589
192.2:2026-01-27T23:50:41.503073:2026-01-27T23:50:41.503074
192.3:2026-01-27T23:50:41.503068:2026-01-27T23:51:37.631579
192.4:2026-01-27T23:50:41.503062:2026-01-27T23:50:41.503063
192.5:2026-01-27T23:50:41.503057:2026-01-27T23:51:37.631568
192.6:2026-01-27T23:50:41.503051:2026-01-27T23:50:41.503052
192.7:2026-01-27T23:50:41.503046:2026-01-27T23:51:37.631559
193:2026-01-27T23:50:41.505889:2026-01-27T23:50:41.505894
193.1:2026-01-27T23:50:41.505949:2026-01-27T23:51:37.636185
193.2:2026-01-27T23:50:41.505941:2026-01-27T23:51:37.636176
193.3:2026-01-27T23:50:41.505933:2026-01-27T23:51:37.636168
193.4:2026-01-27T23:50:41.505925:2026-01-27T23:51:37.636159
193.5:2026-01-27T23:50:41.505917:2026-01-27T23:51:37.636151
193.6:2026-01-27T23:50:41.505909:2026-01-27T23:51:37.636143
193.7:2026-01-27T23:50:41.505901:2026-01-27T23:51:37.636135
194:2026-01-27T23:50:41.503034:2026-01-27T23:51:37.631550
195:2026-01-27T23:50:41.503010:2026-01-27T23:50:41.503014
195.1:2026-01-27T23:50:41.503029:2026-01-27T23:51:37.631546
195.2:2026-01-27T23:50:41.503024:2026-01-27T23:51:37.631542
195.3:2026-01-27T23:50:41.503019:2026-01-27T23:51:37.631538
196:2026-01-27T23:50:41.502971:2026-01-27T23:50:41.502975
196.1:2026-01-27T23:50:41.503005:2026-01-27T23:51:37.631527
196.2:2026-01-27T23:50:41.502999:2026-01-27T23:50:41.503000
196.3:2026-01-27T23:50:41.502991:2026-01-27T23:50:41.502995
196.4:2026-01-27T23:50:41.502986:2026-01-27T23:51:37.631512
196.5:2026-01-27T23:50:41.502980:2026-01-27T23:51:37.631507
197:2026-01-27T23:50:41.502953:2026-01-27T23:51:37.631488
197.1:2026-01-27T23:50:41.502965:2026-01-27T23:50:41.502966
197.2:2026-01-27T23:50:41.502960:2026-01-27T23:51:37.631492
198:2026-01-27T23:50:41.502921:2026-01-27T23:50:41.502926
198.1:2026-01-27T23:50:41.502948:2026-01-27T23:51:37.631483
198.2:2026-01-27T23:50:41.502942:2026-01-27T23:50:41.502943
198.3:2026-01-27T23:50:41.502937:2026-01-27T23:51:37.631475
198.4:2026-01-27T23:50:41.502931:2026-01-27T23:50:41.502932
199:2026-01-27T23:50:41.502898:2026-01-27T23:50:41.502903
199.1:2026-01-27T23:50:41.502915:2026-01-27T23:51:37.631458
199.2:2026-01-27T23:50:41.502908:2026-01-27T23:51:37.631453
20:2026-01-27T23:50:41.505217:2026-01-27T23:50:41.505218
200:2026-01-27T23:50:41.502723:2026-01-27T23:50:41.502725
200.1:2026-01-27T23:50:41.502892:2026-01-27T23:51:37.631440
200.10:2026-01-27T23:50:41.502820:2026-01-27T23:50:41.502822
200.11:2026-01-27T23:50:41.502813:2026-01-27T23:50:41.502815
200.12:2026-01-27T23:50:41.502806:2026-01-27T23:50:41.502808
200.13:2026-01-27T23:50:41.502799:2026-01-27T23:50:41.502801
200.14:2026-01-27T23:50:41.502792:2026-01-27T23:50:41.502794
200.15:2026-01-27T23:50:41.502785:2026-01-27T23:50:41.502787
200.16:2026-01-27T23:50:41.502778:2026-01-27T23:50:41.502780
200.17:2026-01-27T23:50:41.502771:2026-01-27T23:50:41.502773
200.18:2026-01-27T23:50:41.502764:2026-01-27T23:50:41.502766
200.19:2026-01-27T23:50:41.502758:2026-01-27T23:50:41.502759
200.2:2026-01-27T23:50:41.502877:2026-01-27T23:50:41.502887
200.20:2026-01-27T23:50:41.502751:2026-01-27T23:50:41.502753
200.21:2026-01-27T23:50:41.502744:2026-01-27T23:50:41.502746
200.22:2026-01-27T23:50:41.502736:2026-01-27T23:50:41.502738
200.23:2026-01-27T23:50:41.502730:2026-01-27T23:50:41.502731
200.3:2026-01-27T23:50:41.502870:2026-01-27T23:50:41.502872
200.4:2026-01-27T23:50:41.502863:2026-01-27T23:50:41.502865
200.5:2026-01-27T23:50:41.502857:2026-01-27T23:50:41.502858
200.6:2026-01-27T23:50:41.502848:2026-01-27T23:50:41.502852
200.7:2026-01-27T23:50:41.502842:2026-01-27T23:50:41.502843
200.8:2026-01-27T23:50:41.502834:2026-01-27T23:50:41.502837
200.9:2026-01-27T23:50:41.502827:2026-01-27T23:50:41.502829
201:2026-01-27T23:50:41.502604:2026-01-27T23:50:41.502613
201.1:2026-01-27T23:50:41.502717:2026-01-27T23:51:37.631293
201.10:2026-01-27T23:50:41.502667:2026-01-27T23:50:41.502668
201.11:2026-01-27T23:50:41.502662:2026-01-27T23:51:37.631243
201.12:2026-01-27T23:50:41.502657:2026-01-27T23:51:37.631239
201.13:2026-01-27T23:50:41.502651:2026-01-27T23:50:41.502652
201.14:2026-01-27T23:50:41.502646:2026-01-27T23:51:37.631227
201.15:2026-01-27T23:50:41.502640:2026-01-27T23:51:37.631222
201.16:2026-01-27T23:50:41.502635:2026-01-27T23:51:37.631218
201.17:2026-01-27T23:50:41.502629:2026-01-27T23:51:37.631213
201.18:2026-01-27T23:50:41.502623:2026-01-27T23:50:41.502624
201.19:2026-01-27T23:50:41.502618:2026-01-27T23:51:37.631205
201.2:2026-01-27T23:50:41.502712:2026-01-27T23:51:37.631289
201.3:2026-01-27T23:50:41.502705:2026-01-27T23:51:37.631284
201.4:2026-01-27T23:50:41.502699:2026-01-27T23:50:41.502700
201.5:2026-01-27T23:50:41.502694:2026-01-27T23:51:37.631275
201.6:2026-01-27T23:50:41.502689:2026-01-27T23:51:37.631271
201.7:2026-01-27T23:50:41.502683:2026-01-27T23:50:41.502684
201.8:2026-01-27T23:50:41.502678:2026-01-27T23:51:37.631263
201.9:2026-01-27T23:50:41.502673:2026-01-27T23:51:37.631258
202:2026-01-27T23:50:41.502569:2026-01-27T23:50:41.502572
202.1:2026-01-27T23:50:41.502598:2026-01-27T23:50:41.502599
202.2:2026-01-27T23:50:41.502593:2026-01-27T23:51:37.631181
202.3:2026-01-27T23:50:41.502588:2026-01-27T23:51:37.631177
202.4:2026-01-27T23:50:41.502582:2026-01-27T23:51:37.631172
202.5:2026-01-27T23:50:41.502577:2026-01-27T23:51:37.631168
203:2026-01-27T23:50:41.501033:2026-01-27T23:50:41.501035
203.1:2026-01-27T23:50:41.501084:2026-01-27T23:50:41.501086
203.2:2026-01-27T23:50:41.501079:2026-01-27T23:51:37.630272
203.3:2026-01-27T23:50:41.501072:2026-01-27T23:50:41.501074
203.4:2026-01-27T23:50:41.501066:2026-01-27T23:50:41.501067
203.5:2026-01-27T23:50:41.501061:2026-01-27T23:51:37.630255
203.6:2026-01-27T23:50:41.501056:2026-01-27T23:51:37.630249
203.7:2026-01-27T23:50:41.501050:2026-01-27T23:50:41.501051
203.8:2026-01-27T23:50:41.501045:2026-01-27T23:50:41.501046
203.9:2026-01-27T23:50:41.501040:2026-01-27T23:51:37.630209
204:2026-01-27T23:50:41.502519:2026-01-27T23:50:41.502526
204.1:2026-01-27T23:50:41.502564:2026-01-27T23:51:37.631157
204.2:2026-01-27T23:50:41.502558:2026-01-27T23:50:41.502559
204.3:2026-01-27T23:50:41.502553:2026-01-27T23:51:37.631149
204.4:2026-01-27T23:50:41.502548:2026-01-27T23:51:37.631144
204.5:2026-01-27T23:50:41.502538:2026-01-27T23:51:37.631140
204.6:2026-01-27T23:50:41.502531:2026-01-27T23:50:41.502532
205:2026-01-27T23:50:41.501000:2026-01-27T23:51:37.630174
205.1:2026-01-27T23:50:41.501027:2026-01-27T23:50:41.501028
205.2:2026-01-27T23:50:41.501022:2026-01-27T23:51:37.630194
205.3:2026-01-27T23:50:41.501017:2026-01-27T23:51:37.630189
205.4:2026-01-27T23:50:41.501011:2026-01-27T23:50:41.501012
205.5:2026-01-27T23:50:41.501006:2026-01-27T23:51:37.630180
206:2026-01-27T23:50:41.502475:2026-01-27T23:50:41.502477
206.1:2026-01-27T23:50:41.502513:2026-01-27T23:50:41.502514
206.2:2026-01-27T23:50:41.502508:2026-01-27T23:51:37.631111
206.3:2026-01-27T23:50:41.502503:2026-01-27T23:51:37.631106
206.4:2026-01-27T23:50:41.502498:2026-01-27T23:51:37.631102
206.5:2026-01-27T23:50:41.502493:2026-01-27T23:51:37.631098
206.6:2026-01-27T23:50:41.502487:2026-01-27T23:50:41.502488
206.7:2026-01-27T23:50:41.502482:2026-01-27T23:51:37.631088
207:2026-01-27T23:50:41.502419:2026-01-27T23:50:41.502421
207.1:2026-01-27T23:50:41.502468:2026-01-27T23:50:41.502470
207.2:2026-01-27T23:50:41.502463:2026-01-27T23:51:37.631055
207.3:2026-01-27T23:50:41.502458:2026-01-27T23:51:37.631051
207.4:2026-01-27T23:50:41.502453:2026-01-27T23:51:37.631047
207.5:2026-01-27T23:50:41.502447:2026-01-27T23:50:41.502448
207.6:2026-01-27T23:50:41.502442:2026-01-27T23:50:41.502443
207.7:2026-01-27T23:50:41.502437:2026-01-27T23:51:37.631034
207.8:2026-01-27T23:50:41.502432:2026-01-27T23:51:37.631030
207.9:2026-01-27T23:50:41.502426:2026-01-27T23:50:41.502427
208:2026-01-27T23:50:41.505881:2026-01-27T23:50:41.505882
209:2026-01-27T23:50:41.502372:2026-01-27T23:51:37.630951
209.1:2026-01-27T23:50:41.502413:2026-01-27T23:50:41.502414
209.2:2026-01-27T23:50:41.502406:2026-01-27T23:50:41.502407
209.3:2026-01-27T23:50:41.502399:2026-01-27T23:50:41.502400
209.4:2026-01-27T23:50:41.502392:2026-01-27T23:50:41.502394
209.5:2026-01-27T23:50:41.502384:2026-01-27T23:50:41.502387
209.6:2026-01-27T23:50:41.502378:2026-01-27T23:50:41.502379
210:2026-01-27T23:50:41.500951:2026-01-27T23:50:41.500953
210.1:2026-01-27T23:50:41.500986:2026-01-27T23:50:41.500994
210.2:2026-01-27T23:50:41.500981:2026-01-27T23:51:37.630156
210.3:2026-01-27T23:50:41.500975:2026-01-27T23:50:41.500976
210.4:2026-01-27T23:50:41.500970:2026-01-27T23:51:37.630143
210.5:2026-01-27T23:50:41.500964:2026-01-27T23:51:37.630138
210.6:2026-01-27T23:50:41.500958:2026-01-27T23:50:41.500959
211:2026-01-27T23:50:41.502326:2026-01-27T23:50:41.502328
211.1:2026-01-27T23:50:41.502362:2026-01-27T23:50:41.502367
211.2:2026-01-27T23:50:41.502351:2026-01-27T23:50:41.502356
211.3:2026-01-27T23:50:41.502343:2026-01-27T23:50:41.502346
211.4:2026-01-27T23:50:41.502333:2026-01-27T23:50:41.502338
212:2026-01-27T23:50:41.500916:2026-01-27T23:50:41.500917
212.1:2026-01-27T23:50:41.500944:2026-01-27T23:50:41.500945
212.2:2026-01-27T23:50:41.500938:2026-01-27T23:50:41.500939
212.3:2026-01-27T23:50:41.500933:2026-01-27T23:51:37.630111
212.4:2026-01-27T23:50:41.500928:2026-01-27T23:51:37.630105
212.5:2026-01-27T23:50:41.500922:2026-01-27T23:50:41.500923
213:2026-01-27T23:50:41.500888:2026-01-27T23:51:37.629983
213.1:2026-01-27T23:50:41.500911:2026-01-27T23:51:37.630005
213.2:2026-01-27T23:50:41.500905:2026-01-27T23:50:41.500906
213.3:2026-01-27T23:50:41.500900:2026-01-27T23:51:37.629996
213.4:2026-01-27T23:50:41.500894:2026-01-27T23:51:37.629992
214:2026-01-27T23:50:41.505874:2026-01-27T23:50:41.505875
215:2026-01-27T23:50:41.505781:2026-01-27T23:51:37.635997
215.1:2026-01-27T23:50:41.505866:2026-01-27T23:50:41.505867
215.10:2026-01-27T23:50:41.505788:2026-01-27T23:50:41.505790
215.2:2026-01-27T23:50:41.505858:2026-01-27T23:50:41.505859
215.3:2026-01-27T23:50:41.505848:2026-01-27T23:50:41.505849
215.4:2026-01-27T23:50:41.505838:2026-01-27T23:50:41.505840
215.5:2026-01-27T23:50:41.505830:2026-01-27T23:50:41.505831
215.6:2026-01-27T23:50:41.505822:2026-01-27T23:50:41.505823
215.7:2026-01-27T23:50:41.505813:2026-01-27T23:50:41.505815
215.8:2026-01-27T23:50:41.505805:2026-01-27T23:50:41.505807
215.9:2026-01-27T23:50:41.505797:2026-01-27T23:50:41.505798
216:2026-01-27T23:50:41.500882:2026-01-27T23:50:41.500883
217:2026-01-27T23:50:41.500876:2026-01-27T23:50:41.500877
218:2026-01-27T23:50:41.500845:2026-01-27T23:50:41.500846
218.1:2026-01-27T23:50:41.500869:2026-01-27T23:51:37.629947
218.2:2026-01-27T23:50:41.500864:2026-01-27T23:50:41.500865
218.3:2026-01-27T23:50:41.500860:2026-01-27T23:51:37.629927
218.4:2026-01-27T23:50:41.500855:2026-01-27T23:51:37.629921
218.5:2026-01-27T23:50:41.500850:2026-01-27T23:51:37.629914
219:2026-01-27T23:50:41.500766:2026-01-27T23:50:41.500767
219.1:2026-01-27T23:50:41.500839:2026-01-27T23:50:41.500840
219.10:2026-01-27T23:50:41.500790:2026-01-27T23:50:41.500791
219.11:2026-01-27T23:50:41.500785:2026-01-27T23:51:37.629845
219.12:2026-01-27T23:50:41.500778:2026-01-27T23:51:37.629838
219.13:2026-01-27T23:50:41.500772:2026-01-27T23:51:37.629832
219.2:2026-01-27T23:50:41.500833:2026-01-27T23:51:37.629896
219.3:2026-01-27T23:50:41.500827:2026-01-27T23:50:41.500828
219.4:2026-01-27T23:50:41.500821:2026-01-27T23:51:37.629884
219.5:2026-01-27T23:50:41.500814:2026-01-27T23:50:41.500816
219.6:2026-01-27T23:50:41.500808:2026-01-27T23:51:37.629870
219.8:2026-01-27T23:50:41.500801:2026-01-27T23:50:41.500803
219.9:2026-01-27T23:50:41.500796:2026-01-27T23:51:37.629857
22:2026-01-27T23:50:41.505213:2026-01-27T23:51:37.635538
22.1:2026-01-27T23:50:41.506310:2026-01-27T23:51:37.636581
22.2:2026-01-27T23:50:41.506303:2026-01-27T23:51:37.636573
22.3:2026-01-27T23:50:41.506295:2026-01-27T23:51:37.636565
220:2026-01-27T23:50:41.505749:2026-01-27T23:51:37.635962
220.1:2026-01-27T23:50:41.505773:2026-01-27T23:50:41.505774
220.2:2026-01-27T23:50:41.505766:2026-01-27T23:51:37.635980
220.3:2026-01-27T23:50:41.505758:2026-01-27T23:51:37.635971
221:2026-01-27T23:50:41.500759:2026-01-27T23:50:41.500760
222:2026-01-27T23:50:41.500752:2026-01-27T23:50:41.500753
223:2026-01-27T23:50:41.505739:2026-01-27T23:51:37.635951
224:2026-01-27T23:50:41.505732:2026-01-27T23:51:37.635943
225:2026-01-27T23:50:41.505724:2026-01-27T23:51:37.635935
226:2026-01-27T23:50:41.505716:2026-01-27T23:51:37.635926
227:2026-01-27T23:50:41.505708:2026-01-27T23:51:37.635918
228:2026-01-27T23:50:41.505697:2026-01-27T23:50:41.505698
229:2026-01-27T23:50:41.505689:2026-01-27T23:50:41.505690
23:2026-01-27T23:50:41.505208:2026-01-27T23:51:37.635533
23.1:2026-01-27T23:50:41.506287:2026-01-27T23:50:41.506288
23.10:2026-01-27T23:50:41.506219:2026-01-27T23:50:41.506220
23.2:2026-01-27T23:50:41.506280:2026-01-27T23:51:37.636549
23.3:2026-01-27T23:50:41.506272:2026-01-27T23:51:37.636535
23.4:2026-01-27T23:50:41.506264:2026-01-27T23:50:41.506265
23.5:2026-01-27T23:50:41.506257:2026-01-27T23:51:37.636520
23.6:2026-01-27T23:50:41.506249:2026-01-27T23:51:37.636512
23.7:2026-01-27T23:50:41.506242:2026-01-27T23:51:37.636504
23.8:2026-01-27T23:50:41.506234:2026-01-27T23:50:41.506235
23.9:2026-01-27T23:50:41.506227:2026-01-27T23:51:37.636488
230:2026-01-27T23:50:41.505682:2026-01-27T23:51:37.635888
231:2026-01-27T23:50:41.505674:2026-01-27T23:51:37.635880
232:2026-01-27T23:50:41.505666:2026-01-27T23:51:37.635871
233:2026-01-27T23:50:41.505579:2026-01-27T23:50:41.505580
233.1:2026-01-27T23:50:41.505657:2026-01-27T23:51:37.635862
233.10:2026-01-27T23:50:41.505588:2026-01-27T23:51:37.635787
233.2:2026-01-27T23:50:41.505650:2026-01-27T23:51:37.635854
233.3:2026-01-27T23:50:41.505642:2026-01-27T23:51:37.635846
233.4:2026-01-27T23:50:41.505634:2026-01-27T23:50:41.505635
233.5:2026-01-27T23:50:41.505627:2026-01-27T23:51:37.635831
233.6:2026-01-27T23:50:41.505619:2026-01-27T23:51:37.635822
233.7:2026-01-27T23:50:41.505611:2026-01-27T23:50:41.505612
233.8:2026-01-27T23:50:41.505603:2026-01-27T23:50:41.505604
233.9:2026-01-27T23:50:41.505596:2026-01-27T23:51:37.635797
234:2026-01-27T23:50:41.500708:2026-01-27T23:51:37.629769
234.1:2026-01-27T23:50:41.500745:2026-01-27T23:51:37.629805
234.2:2026-01-27T23:50:41.500738:2026-01-27T23:50:41.500739
234.3:2026-01-27T23:50:41.500731:2026-01-27T23:51:37.629795
234.4:2026-01-27T23:50:41.500726:2026-01-27T23:50:41.500727
234.5:2026-01-27T23:50:41.500722:2026-01-27T23:51:37.629785
234.6:2026-01-27T23:50:41.500717:2026-01-27T23:51:37.629779
234.7:2026-01-27T23:50:41.500712:2026-01-27T23:50:41.500713
235:2026-01-27T23:50:41.500664:2026-01-27T23:50:41.500665
235.1:2026-01-27T23:50:41.500703:2026-01-27T23:51:37.629763
235.2:2026-01-27T23:50:41.500698:2026-01-27T23:51:37.629758
235.3:2026-01-27T23:50:41.500693:2026-01-27T23:50:41.500694
235.4:2026-01-27T23:50:41.500688:2026-01-27T23:50:41.500689
235.5:2026-01-27T23:50:41.500683:2026-01-27T23:50:41.500684
235.6:2026-01-27T23:50:41.500679:2026-01-27T23:51:37.629729
235.7:2026-01-27T23:50:41.500674:2026-01-27T23:51:37.629718
235.8:2026-01-27T23:50:41.500669:2026-01-27T23:51:37.629713
236:2026-01-27T23:50:41.498485:2026-01-27T23:51:37.628032
237:2026-01-27T23:50:41.498463:2026-01-27T23:51:37.628003
237.1:2026-01-27T23:50:41.505571:2026-01-27T23:50:41.505572
237.10:2026-01-27T23:50:41.505497:2026-01-27T23:51:37.635686
237.11:2026-01-27T23:50:41.505488:2026-01-27T23:50:41.505489
237.12:2026-01-27T23:50:41.505480:2026-01-27T23:51:37.635669
237.13:2026-01-27T23:50:41.498482:2026-01-27T23:51:37.628029
237.14:2026-01-27T23:50:41.498479:2026-01-27T23:50:41.498480
237.15:2026-01-27T23:50:41.498477:2026-01-27T23:51:37.628023
237.16:2026-01-27T23:50:41.498474:2026-01-27T23:51:37.628020
237.17:2026-01-27T23:50:41.498471:2026-01-27T23:50:41.498472
237.18:2026-01-27T23:50:41.498469:2026-01-27T23:51:37.628014
237.19:2026-01-27T23:50:41.498466:2026-01-27T23:51:37.628007
237.2:2026-01-27T23:50:41.505563:2026-01-27T23:50:41.505564
237.3:2026-01-27T23:50:41.505555:2026-01-27T23:50:41.505556
237.4:2026-01-27T23:50:41.505547:2026-01-27T23:51:37.635738
237.5:2026-01-27T23:50:41.505539:2026-01-27T23:51:37.635729
237.6:2026-01-27T23:50:41.505529:2026-01-27T23:51:37.635721
237.7:2026-01-27T23:50:41.505521:2026-01-27T23:51:37.635712
237.8:2026-01-27T23:50:41.505513:2026-01-27T23:51:37.635704
237.9:2026-01-27T23:50:41.505505:2026-01-27T23:51:37.635695
238:2026-01-27T23:50:41.500593:2026-01-27T23:51:37.629649
238.1:2026-01-27T23:50:41.500659:2026-01-27T23:51:37.629702
238.10:2026-01-27T23:50:41.500609:2026-01-27T23:50:41.500610
238.11:2026-01-27T23:50:41.500604:2026-01-27T23:51:37.629657
238.12:2026-01-27T23:50:41.500598:2026-01-27T23:50:41.500599
238.2:2026-01-27T23:50:41.500653:2026-01-27T23:50:41.500654
238.3:2026-01-27T23:50:41.500648:2026-01-27T23:51:37.629691
238.4:2026-01-27T23:50:41.500643:2026-01-27T23:51:37.629686
238.5:2026-01-27T23:50:41.500637:2026-01-27T23:51:37.629682
238.6:2026-01-27T23:50:41.500632:2026-01-27T23:51:37.629678
238.7:2026-01-27T23:50:41.500626:2026-01-27T23:50:41.500627
238.8:2026-01-27T23:50:41.500621:2026-01-27T23:51:37.629670
238.9:2026-01-27T23:50:41.500615:2026-01-27T23:51:37.629666
239:2026-01-27T23:50:41.500586:2026-01-27T23:50:41.500587
240:2026-01-27T23:50:41.500507:2026-01-27T23:51:37.629586
240.1:2026-01-27T23:50:41.500580:2026-01-27T23:51:37.629640
240.10:2026-01-27T23:50:41.500524:2026-01-27T23:50:41.500525
240.11:2026-01-27T23:50:41.500518:2026-01-27T23:51:37.629594
240.12:2026-01-27T23:50:41.500513:2026-01-27T23:51:37.629590
240.2:2026-01-27T23:50:41.500574:2026-01-27T23:50:41.500575
240.3:2026-01-27T23:50:41.500567:2026-01-27T23:50:41.500569
240.4:2026-01-27T23:50:41.500562:2026-01-27T23:51:37.629626
240.5:2026-01-27T23:50:41.500555:2026-01-27T23:50:41.500557
240.6:2026-01-27T23:50:41.500548:2026-01-27T23:51:37.629616
240.7:2026-01-27T23:50:41.500542:2026-01-27T23:50:41.500543
240.8:2026-01-27T23:50:41.500536:2026-01-27T23:51:37.629607
240.9:2026-01-27T23:50:41.500531:2026-01-27T23:51:37.629603
241:2026-01-27T23:50:41.500441:2026-01-27T23:50:41.500442
241.1:2026-01-27T23:50:41.500500:2026-01-27T23:50:41.500501
241.10:2026-01-27T23:50:41.500456:2026-01-27T23:51:37.629539
241.11:2026-01-27T23:50:41.500451:2026-01-27T23:51:37.629535
241.12:2026-01-27T23:50:41.500446:2026-01-27T23:50:41.500447
241.2:2026-01-27T23:50:41.500496:2026-01-27T23:51:37.629578
241.3:2026-01-27T23:50:41.500491:2026-01-27T23:51:37.629570
241.4:2026-01-27T23:50:41.500484:2026-01-27T23:50:41.500485
241.5:2026-01-27T23:50:41.500480:2026-01-27T23:51:37.629559
241.6:2026-01-27T23:50:41.500475:2026-01-27T23:51:37.629553
241.7:2026-01-27T23:50:41.500470:2026-01-27T23:51:37.629549
241.8:2026-01-27T23:50:41.500465:2026-01-27T23:50:41.500466
241.9:2026-01-27T23:50:41.500461:2026-01-27T23:51:37.629542
242:2026-01-27T23:50:41.500382:2026-01-27T23:50:41.500383
242.1:2026-01-27T23:50:41.500435:2026-01-27T23:51:37.629523
242.10:2026-01-27T23:50:41.500392:2026-01-27T23:50:41.500393
242.11:2026-01-27T23:50:41.500387:2026-01-27T23:50:41.500388
242.2:2026-01-27T23:50:41.500430:2026-01-27T23:50:41.500431
242.3:2026-01-27T23:50:41.500426:2026-01-27T23:51:37.629516
242.4:2026-01-27T23:50:41.500421:2026-01-27T23:51:37.629512
242.5:2026-01-27T23:50:41.500416:2026-01-27T23:51:37.629509
242.6:2026-01-27T23:50:41.500411:2026-01-27T23:50:41.500412
242.7:2026-01-27T23:50:41.500407:2026-01-27T23:51:37.629502
242.8:2026-01-27T23:50:41.500402:2026-01-27T23:51:37.629498
242.9:2026-01-27T23:50:41.500397:2026-01-27T23:51:37.629495
243:2026-01-27T23:50:41.505446:2026-01-27T23:50:41.505447
244:2026-01-27T23:50:41.505439:2026-01-27T23:51:37.635625
245:2026-01-27T23:50:41.500292:2026-01-27T23:50:41.500310
245.1:2026-01-27T23:50:41.500377:2026-01-27T23:51:37.629480
245.10:2026-01-27T23:50:41.500330:2026-01-27T23:51:37.629444
245.11:2026-01-27T23:50:41.500325:2026-01-27T23:51:37.629440
245.12:2026-01-27T23:50:41.500320:2026-01-27T23:51:37.629436
245.13:2026-01-27T23:50:41.500315:2026-01-27T23:51:37.629433
245.2:2026-01-27T23:50:41.500372:2026-01-27T23:51:37.629476
245.3:2026-01-27T23:50:41.500367:2026-01-27T23:51:37.629472
245.4:2026-01-27T23:50:41.500361:2026-01-27T23:50:41.500362
245.5:2026-01-27T23:50:41.500356:2026-01-27T23:50:41.500357
245.6:2026-01-27T23:50:41.500351:2026-01-27T23:50:41.500352
245.7:2026-01-27T23:50:41.500346:2026-01-27T23:50:41.500347
245.8:2026-01-27T23:50:41.500342:2026-01-27T23:51:37.629451
245.9:2026-01-27T23:50:41.500336:2026-01-27T23:50:41.500337
246:2026-01-27T23:50:41.500221:2026-01-27T23:50:41.500223
246.1:2026-01-27T23:50:41.500286:2026-01-27T23:50:41.500287
246.10:2026-01-27T23:50:41.500233:2026-01-27T23:51:37.629371
246.11:2026-01-27T23:50:41.500228:2026-01-27T23:51:37.629367
246.2:2026-01-27T23:50:41.500281:2026-01-27T23:51:37.629408
246.3:2026-01-27T23:50:41.500275:2026-01-27T23:50:41.500276
246.4:2026-01-27T23:50:41.500269:2026-01-27T23:50:41.500270
246.5:2026-01-27T23:50:41.500263:2026-01-27T23:51:37.629395
246.6:2026-01-27T23:50:41.500258:2026-01-27T23:51:37.629391
246.7:2026-01-27T23:50:41.500252:2026-01-27T23:50:41.500253
246.8:2026-01-27T23:50:41.500246:2026-01-27T23:50:41.500247
246.9:2026-01-27T23:50:41.500238:2026-01-27T23:50:41.500239
247:2026-01-27T23:50:41.500140:2026-01-27T23:50:41.500142
247.1:2026-01-27T23:50:41.500213:2026-01-27T23:50:41.500215
247.10:2026-01-27T23:50:41.500164:2026-01-27T23:50:41.500165
247.11:2026-01-27T23:50:41.500159:2026-01-27T23:51:37.629307
247.12:2026-01-27T23:50:41.500153:2026-01-27T23:50:41.500154
247.13:2026-01-27T23:50:41.500148:2026-01-27T23:51:37.629299
247.2:2026-01-27T23:50:41.500206:2026-01-27T23:50:41.500208
247.3:2026-01-27T23:50:41.500201:2026-01-27T23:50:41.500202
247.4:2026-01-27T23:50:41.500196:2026-01-27T23:51:37.629338
247.5:2026-01-27T23:50:41.500191:2026-01-27T23:51:37.629334
247.6:2026-01-27T23:50:41.500186:2026-01-27T23:51:37.629330
247.7:2026-01-27T23:50:41.500180:2026-01-27T23:50:41.500181
247.8:2026-01-27T23:50:41.500175:2026-01-27T23:51:37.629319
247.9:2026-01-27T23:50:41.500170:2026-01-27T23:51:37.629315
248:2026-01-27T23:50:41.505432:2026-01-27T23:51:37.635618
249:2026-01-27T23:50:41.505424:2026-01-27T23:51:37.635610
25:2026-01-27T23:50:41.505203:2026-01-27T23:51:37.635528
25.1:2026-01-27T23:50:41.506212:2026-01-27T23:51:37.636472
25.2:2026-01-27T23:50:41.506204:2026-01-27T23:51:37.636464
25.3:2026-01-27T23:50:41.506197:2026-01-27T23:51:37.636456
25.4:2026-01-27T23:50:41.506189:2026-01-27T23:50:41.506190
25.5:2026-01-27T23:50:41.506182:2026-01-27T23:51:37.636441
25.6:2026-01-27T23:50:41.506175:2026-01-27T23:51:37.636433
250:2026-01-27T23:50:41.500060:2026-01-27T23:50:41.500062
250.1:2026-01-27T23:50:41.500133:2026-01-27T23:50:41.500135
250.10:2026-01-27T23:50:41.500079:2026-01-27T23:51:37.629243
250.11:2026-01-27T23:50:41.500073:2026-01-27T23:50:41.500074
250.12:2026-01-27T23:50:41.500067:2026-01-27T23:51:37.629234
250.2:2026-01-27T23:50:41.500127:2026-01-27T23:50:41.500129
250.3:2026-01-27T23:50:41.500122:2026-01-27T23:51:37.629280
250.4:2026-01-27T23:50:41.500116:2026-01-27T23:50:41.500117
250.5:2026-01-27T23:50:41.500109:2026-01-27T23:50:41.500111
250.6:2026-01-27T23:50:41.500104:2026-01-27T23:51:37.629266
250.7:2026-01-27T23:50:41.500098:2026-01-27T23:51:37.629262
250.8:2026-01-27T23:50:41.500090:2026-01-27T23:51:37.629258
250.9:2026-01-27T23:50:41.500084:2026-01-27T23:50:41.500085
251:2026-01-27T23:50:41.500003:2026-01-27T23:51:37.629184
251.1:2026-01-27T23:50:41.500047:2026-01-27T23:50:41.500054
251.2:2026-01-27T23:50:41.500042:2026-01-27T23:51:37.629216
251.3:2026-01-27T23:50:41.500037:2026-01-27T23:51:37.629212
251.4:2026-01-27T23:50:41.500032:2026-01-27T23:51:37.629208
251.5:2026-01-27T23:50:41.500027:2026-01-27T23:51:37.629205
251.6:2026-01-27T23:50:41.500017:2026-01-27T23:50:41.500022
251.7:2026-01-27T23:50:41.500012:2026-01-27T23:50:41.500013
251.8:2026-01-27T23:50:41.500007:2026-01-27T23:50:41.500008
252:2026-01-27T23:50:41.505415:2026-01-27T23:50:41.505416
253:2026-01-27T23:50:41.499940:2026-01-27T23:50:41.499942
253.1:2026-01-27T23:50:41.499997:2026-01-27T23:51:37.629179
253.10:2026-01-27T23:50:41.499951:2026-01-27T23:50:41.499952
253.11:2026-01-27T23:50:41.499947:2026-01-27T23:51:37.629137
253.2:2026-01-27T23:50:41.499992:2026-01-27T23:51:37.629176
253.3:2026-01-27T23:50:41.499987:2026-01-27T23:51:37.629172
253.4:2026-01-27T23:50:41.499980:2026-01-27T23:50:41.499981
253.5:2026-01-27T23:50:41.499975:2026-01-27T23:50:41.499976
253.6:2026-01-27T23:50:41.499970:2026-01-27T23:50:41.499971
253.7:2026-01-27T23:50:41.499966:2026-01-27T23:51:37.629153
253.8:2026-01-27T23:50:41.499961:2026-01-27T23:51:37.629149
253.9:2026-01-27T23:50:41.499956:2026-01-27T23:51:37.629145
254:2026-01-27T23:50:41.499903:2026-01-27T23:50:41.499904
254.1:2026-01-27T23:50:41.499934:2026-01-27T23:51:37.629128
254.2:2026-01-27T23:50:41.499929:2026-01-27T23:50:41.499930
254.3:2026-01-27T23:50:41.499924:2026-01-27T23:50:41.499925
254.4:2026-01-27T23:50:41.499919:2026-01-27T23:50:41.499920
254.5:2026-01-27T23:50:41.499914:2026-01-27T23:51:37.629114
254.6:2026-01-27T23:50:41.499909:2026-01-27T23:51:37.629110
255:2026-01-27T23:50:41.499851:2026-01-27T23:50:41.499853
255.1:2026-01-27T23:50:41.499897:2026-01-27T23:51:37.629101
255.2:2026-01-27T23:50:41.499892:2026-01-27T23:51:37.629098
255.3:2026-01-27T23:50:41.499887:2026-01-27T23:51:37.629094
255.4:2026-01-27T23:50:41.499882:2026-01-27T23:51:37.629091
255.5:2026-01-27T23:50:41.499877:2026-01-27T23:51:37.629083
255.6:2026-01-27T23:50:41.499871:2026-01-27T23:51:37.629079
255.7:2026-01-27T23:50:41.499862:2026-01-27T23:51:37.629076
255.8:2026-01-27T23:50:41.499857:2026-01-27T23:51:37.629072
256:2026-01-27T23:50:41.499806:2026-01-27T23:50:41.499808
256.1:2026-01-27T23:50:41.499845:2026-01-27T23:50:41.499846
256.2:2026-01-27T23:50:41.499841:2026-01-27T23:51:37.629060
256.3:2026-01-27T23:50:41.499836:2026-01-27T23:51:37.629056
256.4:2026-01-27T23:50:41.499831:2026-01-27T23:51:37.629052
256.5:2026-01-27T23:50:41.499826:2026-01-27T23:50:41.499827
256.6:2026-01-27T23:50:41.499822:2026-01-27T23:51:37.629045
256.7:2026-01-27T23:50:41.499817:2026-01-27T23:51:37.629042
256.8:2026-01-27T23:50:41.499812:2026-01-27T23:51:37.629038
257:2026-01-27T23:50:41.499760:2026-01-27T23:50:41.499761
257.1:2026-01-27T23:50:41.499800:2026-01-27T23:51:37.629029
257.2:2026-01-27T23:50:41.499794:2026-01-27T23:50:41.499795
257.3:2026-01-27T23:50:41.499789:2026-01-27T23:50:41.499790
257.4:2026-01-27T23:50:41.499785:2026-01-27T23:51:37.629010
257.5:2026-01-27T23:50:41.499780:2026-01-27T23:51:37.629006
257.6:2026-01-27T23:50:41.499775:2026-01-27T23:51:37.629003
257.7:2026-01-27T23:50:41.499770:2026-01-27T23:51:37.628999
257.8:2026-01-27T23:50:41.499765:2026-01-27T23:50:41.499766
258:2026-01-27T23:50:41.499710:2026-01-27T23:50:41.499711
258.1:2026-01-27T23:50:41.499753:2026-01-27T23:50:41.499754
258.2:2026-01-27T23:50:41.499749:2026-01-27T23:51:37.628983
258.3:2026-01-27T23:50:41.499744:2026-01-27T23:51:37.628980
258.4:2026-01-27T23:50:41.499739:2026-01-27T23:51:37.628976
258.5:2026-01-27T23:50:41.499732:2026-01-27T23:51:37.628972
258.6:2026-01-27T23:50:41.499727:2026-01-27T23:51:37.628968
258.7:2026-01-27T23:50:41.499722:2026-01-27T23:51:37.628964
258.8:2026-01-27T23:50:41.499716:2026-01-27T23:50:41.499717
259:2026-01-27T23:50:41.499660:2026-01-27T23:50:41.499661
259.1:2026-01-27T23:50:41.499701:2026-01-27T23:51:37.628951
259.2:2026-01-27T23:50:41.499695:2026-01-27T23:50:41.499696
259.3:2026-01-27T23:50:41.499690:2026-01-27T23:51:37.628403
259.4:2026-01-27T23:50:41.499685:2026-01-27T23:51:37.628398
259.5:2026-01-27T23:50:41.499680:2026-01-27T23:50:41.499681
259.6:2026-01-27T23:50:41.499675:2026-01-27T23:50:41.499676
259.7:2026-01-27T23:50:41.499670:2026-01-27T23:51:37.628383
259.8:2026-01-27T23:50:41.499665:2026-01-27T23:50:41.499666
26:2026-01-27T23:50:41.505198:2026-01-27T23:50:41.505199
26.1:2026-01-27T23:50:41.506167:2026-01-27T23:51:37.636425
26.10:2026-01-27T23:50:41.506100:2026-01-27T23:51:37.636346
26.2:2026-01-27T23:50:41.506160:2026-01-27T23:51:37.636417
26.3:2026-01-27T23:50:41.506152:2026-01-27T23:51:37.636401
26.4:2026-01-27T23:50:41.506145:2026-01-27T23:51:37.636394
26.5:2026-01-27T23:50:41.506137:2026-01-27T23:51:37.636386
26.6:2026-01-27T23:50:41.506129:2026-01-27T23:50:41.506130
26.7:2026-01-27T23:50:41.506122:2026-01-27T23:51:37.636370
26.8:2026-01-27T23:50:41.506115:2026-01-27T23:51:37.636362
26.9:2026-01-27T23:50:41.506107:2026-01-27T23:50:41.506108
260:2026-01-27T23:50:41.499608:2026-01-27T23:50:41.499611
260.1:2026-01-27T23:50:41.499653:2026-01-27T23:51:37.628365
260.2:2026-01-27T23:50:41.499647:2026-01-27T23:50:41.499648
260.3:2026-01-27T23:50:41.499641:2026-01-27T23:50:41.499642
260.4:2026-01-27T23:50:41.499636:2026-01-27T23:51:37.628348
260.5:2026-01-27T23:50:41.499629:2026-01-27T23:50:41.499631
260.6:2026-01-27T23:50:41.499622:2026-01-27T23:50:41.499624
260.7:2026-01-27T23:50:41.499616:2026-01-27T23:50:41.499618
261:2026-01-27T23:50:41.499536:2026-01-27T23:50:41.499540
261.1:2026-01-27T23:50:41.499601:2026-01-27T23:51:37.628313
261.2:2026-01-27T23:50:41.499595:2026-01-27T23:50:41.499596
261.3:2026-01-27T23:50:41.499589:2026-01-27T23:50:41.499590
261.4:2026-01-27T23:50:41.499582:2026-01-27T23:50:41.499584
261.5:2026-01-27T23:50:41.499575:2026-01-27T23:50:41.499577
261.6:2026-01-27T23:50:41.499568:2026-01-27T23:50:41.499569
261.7:2026-01-27T23:50:41.499556:2026-01-27T23:50:41.499558
262:2026-01-27T23:50:41.498407:2026-01-27T23:50:41.515569
262.1:2026-01-27T23:50:41.498454:2026-01-27T23:50:41.515559
262.10:2026-01-27T23:50:41.505389:2026-01-27T23:50:41.515557
262.11:2026-01-27T23:50:41.498418:2026-01-27T23:50:41.515567
262.12:2026-01-27T23:50:41.498413:2026-01-27T23:50:41.515568
262.2:2026-01-27T23:50:41.498449:2026-01-27T23:50:41.515560
262.3:2026-01-27T23:50:41.498444:2026-01-27T23:50:41.515561
262.4:2026-01-27T23:50:41.498439:2026-01-27T23:50:41.515562
262.5:2026-01-27T23:50:41.498436:2026-01-27T23:50:41.515563
262.6:2026-01-27T23:50:41.498432:2026-01-27T23:50:41.515564
262.7:2026-01-27T23:50:41.498429:2026-01-27T23:50:41.515565
262.8:2026-01-27T23:50:41.505405:2026-01-27T23:50:41.515554
262.9:2026-01-27T23:50:41.498423:2026-01-27T23:50:41.515566
263:2026-01-27T23:50:41.498344:2026-01-27T23:51:37.683609
263.1:2026-01-27T23:50:41.498400:2026-01-27T23:51:37.683602
263.2:2026-01-27T23:50:41.498395:2026-01-27T23:51:37.683603
263.3:2026-01-27T23:50:41.498389:2026-01-27T23:51:37.683604
263.4:2026-01-27T23:50:41.498384:2026-01-27T23:51:37.683605
263.5:2026-01-27T23:50:41.498378:2026-01-27T23:51:37.683606
263.6:2026-01-27T23:50:41.498372:2026-01-27T23:51:37.683606
263.7:2026-01-27T23:50:41.498368:2026-01-27T23:51:37.683607
263.8:2026-01-27T23:50:41.498358:2026-01-27T23:51:37.683608
264:2026-01-28T01:20:08.553847:2026-01-28T01:39:14.758593
264.1:2026-01-28T01:20:17.379514:2026-01-28T01:39:14.758580
264.2:2026-01-28T01:20:17.481124:2026-01-28T01:39:14.758583
264.3:2026-01-28T01:20:17.594393:2026-01-28T01:39:14.758585
264.4:2026-01-28T01:20:17.854559:2026-01-28T01:39:14.758586
264.5:2026-01-28T01:20:18.007716:2026-01-28T01:39:14.758587
264.6:2026-01-28T01:20:18.118224:2026-01-28T01:39:14.758588
264.7:2026-01-28T01:20:18.287933:2026-01-28T01:39:14.758589
264.8:2026-01-28T01:20:18.404329:2026-01-28T01:39:14.758591
264.9:2026-01-28T01:20:18.513973:2026-01-28T01:39:14.758592
265:2026-01-28T13:51:58.432185:2026-01-28T21:02:25.578393
265.1:2026-01-28T13:55:15.552146:2026-01-28T21:02:25.578379
265.2:2026-01-28T13:55:17.288324:2026-01-28T21:02:25.578385
265.3:2026-01-28T13:55:19.415156:2026-01-28T21:02:25.578388
265.4:2026-01-28T13:55:21.121695:2026-01-28T21:02:25.578390
266:2026-01-28T21:14:24.478468:2026-01-28T21:20:43.039724
266.1:2026-01-28T21:14:29.590090:2026-01-28T21:55:22.383938
266.2:2026-01-28T21:14:31.480490:2026-01-28T21:55:22.383941
266.3:2026-01-28T21:14:33.184130:2026-01-28T21:55:22.383942
266.4:2026-01-28T21:14:34.517139:2026-01-28T21:55:22.383943
266.5:2026-01-28T21:14:35.898815:2026-01-28T21:20:49.690286
267:2026-01-28T22:26:05.473566:2026-01-29T02:09:45.957109
267.1:2026-01-28T22:26:10.364212:2026-01-29T02:09:45.957102
267.2:2026-01-28T22:26:12.171649:2026-01-29T02:09:45.957102
267.3:2026-01-28T22:26:13.932631:2026-01-29T02:09:45.957103
267.4:2026-01-28T22:26:15.253098:2026-01-29T02:09:45.957104
267.5:2026-01-28T22:26:16.379299:2026-01-29T02:09:45.957105
267.6:2026-01-28T22:26:17.788660:2026-01-29T02:09:45.957106
267.7:2026-01-28T22:26:19.178103:2026-01-29T02:09:45.957107
267.8:2026-01-28T22:26:20.882963:2026-01-29T02:09:45.957108
267.9:2026-01-28T22:26:22.332652:2026-01-29T02:09:45.957108
268:2026-01-29T02:12:17.206362:2026-01-29T02:29:10.116694
268.1:2026-01-29T02:12:24.286400:2026-01-29T02:18:05.948270
268.2:2026-01-29T02:12:24.853665:2026-01-29T02:41:27.715291
268.3:2026-01-29T02:12:25.395525:2026-01-29T03:04:15.836833
268.4:2026-01-29T02:12:25.979364:2026-01-29T03:08:59.298252
268.5:2026-01-29T02:12:26.526909:2026-01-29T03:09:33.065180
268.6:2026-01-29T02:12:27.093344:2026-01-29T03:09:33.477573
28.1:2026-01-27T23:50:41.506091:2026-01-27T23:50:41.506092
28.2:2026-01-27T23:50:41.506084:2026-01-27T23:51:37.636330
28.3:2026-01-27T23:50:41.506076:2026-01-27T23:50:41.506077
28.4:2026-01-27T23:50:41.506069:2026-01-27T23:51:37.636314
35:2026-01-27T23:50:41.502304:2026-01-27T23:51:37.630894
35.1:2026-01-27T23:50:41.502320:2026-01-27T23:50:41.502321
35.2:2026-01-27T23:50:41.502315:2026-01-27T23:51:37.630903
35.3:2026-01-27T23:50:41.502309:2026-01-27T23:51:37.630899
42:2026-01-27T23:50:41.502265:2026-01-27T23:50:41.502267
42.1:2026-01-27T23:50:41.502298:2026-01-27T23:51:37.630887
42.2:2026-01-27T23:50:41.502293:2026-01-27T23:51:37.630883
42.3:2026-01-27T23:50:41.502288:2026-01-27T23:50:41.502289
42.4:2026-01-27T23:50:41.502283:2026-01-27T23:50:41.502284
42.5:2026-01-27T23:50:41.502278:2026-01-27T23:51:37.630871
42.6:2026-01-27T23:50:41.502273:2026-01-27T23:51:37.630867
45:2026-01-27T23:50:41.502216:2026-01-27T23:51:37.630814
45.1:2026-01-27T23:50:41.502260:2026-01-27T23:51:37.630856
45.2:2026-01-27T23:50:41.502255:2026-01-27T23:51:37.630851
45.3:2026-01-27T23:50:41.502249:2026-01-27T23:50:41.502250
45.4:2026-01-27T23:50:41.502244:2026-01-27T23:51:37.630843
45.5:2026-01-27T23:50:41.502239:2026-01-27T23:51:37.630834
45.6:2026-01-27T23:50:41.502232:2026-01-27T23:51:37.630828
45.7:2026-01-27T23:50:41.502227:2026-01-27T23:51:37.630824
45.8:2026-01-27T23:50:41.502221:2026-01-27T23:50:41.502222
46:2026-01-27T23:50:41.504929:2026-01-27T23:51:37.635222
46.1:2026-01-27T23:50:41.504958:2026-01-27T23:51:37.635254
46.2:2026-01-27T23:50:41.504953:2026-01-27T23:51:37.635249
46.3:2026-01-27T23:50:41.504948:2026-01-27T23:51:37.635243
46.4:2026-01-27T23:50:41.504943:2026-01-27T23:51:37.635238
46.5:2026-01-27T23:50:41.504938:2026-01-27T23:51:37.635233
46.6:2026-01-27T23:50:41.504933:2026-01-27T23:50:41.504934
47:2026-01-27T23:50:41.502167:2026-01-27T23:50:41.502169
47.1:2026-01-27T23:50:41.502211:2026-01-27T23:51:37.630810
47.2:2026-01-27T23:50:41.502206:2026-01-27T23:51:37.630806
47.3:2026-01-27T23:50:41.502201:2026-01-27T23:51:37.630802
47.4:2026-01-27T23:50:41.502195:2026-01-27T23:50:41.502196
47.5:2026-01-27T23:50:41.502189:2026-01-27T23:50:41.502190
47.6:2026-01-27T23:50:41.502184:2026-01-27T23:51:37.630789
47.7:2026-01-27T23:50:41.502179:2026-01-27T23:51:37.630780
47.8:2026-01-27T23:50:41.502173:2026-01-27T23:50:41.502174
48:2026-01-27T23:50:41.504904:2026-01-27T23:51:37.635189
48.1:2026-01-27T23:50:41.504924:2026-01-27T23:51:37.635217
48.2:2026-01-27T23:50:41.504919:2026-01-27T23:51:37.635206
48.3:2026-01-27T23:50:41.504913:2026-01-27T23:50:41.504914
48.4:2026-01-27T23:50:41.504908:2026-01-27T23:50:41.504909
49:2026-01-27T23:50:41.502106:2026-01-27T23:51:37.630725
49.1:2026-01-27T23:50:41.502161:2026-01-27T23:50:41.502162
49.10:2026-01-27T23:50:41.502111:2026-01-27T23:50:41.502112
49.2:2026-01-27T23:50:41.502156:2026-01-27T23:50:41.502157
49.3:2026-01-27T23:50:41.502151:2026-01-27T23:51:37.630758
49.4:2026-01-27T23:50:41.502146:2026-01-27T23:51:37.630754
49.5:2026-01-27T23:50:41.502140:2026-01-27T23:50:41.502141
49.6:2026-01-27T23:50:41.502135:2026-01-27T23:51:37.630745
49.7:2026-01-27T23:50:41.502127:2026-01-27T23:51:37.630741
49.8:2026-01-27T23:50:41.502122:2026-01-27T23:51:37.630737
49.9:2026-01-27T23:50:41.502117:2026-01-27T23:51:37.630733
5:2026-01-27T23:50:41.505182:2026-01-27T23:51:37.635507
51:2026-01-27T23:50:41.498459:2026-01-27T23:51:37.627999
51.1:2026-01-27T23:50:41.505471:2026-01-27T23:51:37.635660
51.2:2026-01-27T23:50:41.505463:2026-01-27T23:51:37.635651
51.3:2026-01-27T23:50:41.505454:2026-01-27T23:50:41.505455
6:2026-01-27T23:50:41.505256:2026-01-27T23:50:41.505257
7:2026-01-27T23:50:41.505177:2026-01-27T23:51:37.635501
7.1:2026-01-27T23:50:41.506423:2026-01-27T23:51:37.636704
8:2026-01-27T23:50:41.505251:2026-01-27T23:50:41.505252
-->

<!-- TASK RELATIONSHIPS
203:depends-on:219
-->

---
**ai-todo** | Last Updated: 2026-01-29 03:09:33
