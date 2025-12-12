# todo.ai ToDo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**

## Tasks
- [ ] **#129** Implement --prune function to remove old archived tasks based on git history `#feature`
  - [ ] **#129.3** Add prune command with --days and --from-task options `#feature`
  - [ ] **#129.2** Implement git history analysis to identify archive dates for tasks `#feature`
  - [ ] **#129.1** Design prune function with 30-day default and task ID targeting options `#feature`
- [ ] **#128** Create git commit hook for todo list linting and validation `#feature`
- [ ] **#127** Enhance --lint command with additional detection features `#feature`
- [x] **#125** Overhaul bug reporting feature: eliminate prompts and improve formatting `#bug` `#feature`
  > Current implementation has basic markdown but needs improvement: (1) Create GitHub issue template (.github/ISSUE_TEMPLATE/bug_report.yml), (2) Use GitHub callout blocks (> [!NOTE], > [!WARNING]), (3) Better structure with proper sections, (4) Remove prompts for agent workflow, (5) Auto-collect all context without user input
  - [x] **#125.13** Update bug reporting design document with new implementation details `#docs`
    > Update docs/design/BUG_REPORTING_DESIGN.md: (1) Document GitHub issue template structure, (2) Explain callout block usage and markdown improvements, (3) Document agent vs human detection logic, (4) Add examples of new bug report format, (5) Document auto-labeling system, (6) Update template examples to match new generate_bug_report() implementation. Keep aligned with actual code.
  - [ ] **#125.12** Test new bug report format with real GitHub issue creation `#test`
    > Implementation complete. Test before next release: (1) Set AI_AGENT=true to test agent flow, (2) Unset to test human flow, (3) Trigger error and call report-bug, (4) Verify markdown renders correctly, (5) Check labels applied, (6) Verify all context sections populated. Should test both flows to ensure proper detection and different behaviors.
    > Create test bug report with all new features: (1) Trigger error in test environment, (2) Run report-bug command, (3) Verify markdown renders correctly on GitHub (callout blocks, tables, code blocks), (4) Test with agent simulation (set AI_AGENT=true env var), (5) Verify duplicate detection still works, (6) Check auto-labels applied correctly, (7) Validate all context sections populated.
  - [x] **#125.11** Update cursor rules to reflect new agent-friendly bug reporting workflow `#docs`
    > Update .cursor/rules/todo.ai-bug-reporting.mdc: (1) Remove mention of user prompts for agents, (2) Add note that agents can use report-bug directly without prompts, (3) Humans still get confirmation prompts, (4) Show updated example of agent usage: 'When error occurs, call ./todo.ai report-bug and it will auto-submit'. Keep rule concise (<25 lines).
  - [x] **#125.10** Add intelligent error categorization and suggested labels `#feature`
    > Auto-detect error type from error message/context and suggest GitHub labels: (1) 'bug' always, (2) 'crash' if segfault/core dump, (3) 'performance' if timeout/slow, (4) 'data-loss' if file corruption, (5) 'coordination' if GitHub API/coordination issues, (6) OS-specific: 'macos', 'linux', 'wsl', (7) Shell-specific: 'zsh', 'bash'. Use pattern matching on error message. Add labels via gh issue create --label.
  - [x] **#125.9** Enhance context auto-collection: add git status, recent commands, TODO.md state `#code`
    > Expand collect_error_context() function: (1) Git status: branch, dirty state, last commit, (2) Shell history: last 5 commands from .todo.ai.log, (3) TODO.md state: active task count, mode, coordination type, (4) Environment: TERM, EDITOR, relevant env vars, (5) File context: if error in specific file, include relevant lines. Format all in collapsible sections to keep bug report clean.
  - [x] **#125.8** Remove prompts from suggest_bug_report() - make fully automated for AI agents `#code`
    > Currently suggest_bug_report() (line 6245) prompts user with 'Report this bug? (y/N)'. For agents: (1) Detect if running in AI agent context (check for CURSOR_AI, AI_AGENT env vars), (2) If agent: show preview but proceed automatically after 2 second delay, (3) If human: keep existing prompt workflow. Agent flow: Show preview → 'Auto-submitting in 2 seconds...' → Submit. Maintains user control for humans, enables automation for agents.
  - [x] **#125.7** Rewrite generate_bug_report() to use GitHub callout blocks and better markdown structure `#code`
    > Use GitHub markdown features: (1) Callout blocks for System Info (> [!NOTE]), Error sections (> [!WARNING]), (2) Clean section headers with --- separators, (3) Proper code blocks with language tags, (4) Collapsible <details> for logs, (5) Table format for system information. Mirror the structure from bug_report.yml template. Located in todo.ai around line 5834.
  - [x] **#125.6** Create GitHub issue template for bug reports (.github/ISSUE_TEMPLATE/bug_report.yml) `#feature`
    > Create .github/ISSUE_TEMPLATE/bug_report.yml with structured fields: Error Description (textarea), Command Used (input), Error Context (textarea), System Info (auto-filled), Logs (auto-attached). Use GitHub's form schema for issue templates. This will be used as the reference template for generate_bug_report() function.
- [ ] **#51** Add contributor section to release summary: list all contributors for each release `#feature`
- [ ] **#49** Investigate cybersecurity implications of todo.ai installation, updates, and operations `#security`
  - [ ] **#49.10** Check and link to GitHub security features for the repo: https://github.com/fxstein/todo.ai/security `#security`
  - [ ] **#49.9** Implement high-priority security improvements identified in audit `#code`
  - [ ] **#49.8** Create security improvement recommendations document based on findings `#docs`
  - [ ] **#49.7** Evaluate supply chain security: repository compromise, MITM attacks, and code signing `#security`
  - [ ] **#49.6** Review file system access: what files can be read/written and potential data exfiltration risks `#security`
  - [ ] **#49.5** Analyze prompt injection risks: malicious content in TODO.md affecting AI agent behavior `#security`
  - [ ] **#49.4** Examine Cursor rules injection vectors: preventing malicious rules from being installed or modified `#security`
  - [ ] **#49.3** Assess code execution risks: migration system, script execution, and dynamic code loading `#security`
  - [ ] **#49.2** Investigate update process security: automatic update downloads, code verification, and execution risks `#security`
  - [ ] **#49.1** Analyze installation security: curl download verification, HTTPS validation, and integrity checks `#security`
- [ ] **#47** Implement feature request capability for todo.ai (similar to bug reporting) `#feature`
  - [ ] **#47.8** Test feature request creation, duplicate detection, and 'me too' workflow `#test`
  - [ ] **#47.7** Update help screen and documentation with feature request command `#docs`
  - [ ] **#47.6** Integrate feature request rules into cursor rules (similar to bug reporting rules) `#code`
  - [ ] **#47.5** Add manual confirmation requirement (always ask before creating feature request) `#code`
  - [ ] **#47.4** Implement 'me too' reply for existing feature requests `#code`
  - [ ] **#47.3** Add duplicate detection for existing feature requests (similarity matching) `#code`
  - [ ] **#47.2** Implement feature request command handler and template generation `#code`
  - [ ] **#47.1** Create design document for feature request system (similar to bug reporting design) `#docs`
- [ ] **#45** Enhance release process with pre-release support for beta/testing versions `#release`
  - [ ] **#45.8** Test pre-release creation and promotion workflow `#test`
  - [ ] **#45.7** Update release process documentation with pre-release workflow `#docs`
  - [ ] **#45.6** Add command to promote pre-release to official release (remove --prerelease flag) `#code`
  - [ ] **#45.5** Implement workflow: create pre-release → test → fix if needed → promote to official release `#code`
  - [ ] **#45.4** Add GitHub pre-release flag support (gh release create --prerelease) `#code`
  - [ ] **#45.3** Implement pre-release support in release.sh script (--prerelease flag, version parsing) `#code`
  - [ ] **#45.2** Create design document for pre-release workflow and integration with existing release process `#docs`
  - [ ] **#45.1** Research and analyze pre-release version standards (beta, rc, alpha, dev) and GitHub release integration `#research`
- [ ] **#42** Implement self-reporting bug feature for GitHub Issues `#feature`
  - [x] **#42.6** Test duplicate detection and 'me too' reply flow
  - [x] **#42.5** Test bug reporting with GitHub CLI integration
  - [x] **#42.4** Create bug report template with logs and data attachment
  - [x] **#42.3** Implement duplicate issue detection and 'me too' reply functionality
  - [x] **#42.2** Implement bug detection and reporting logic
  - [x] **#42.1** Create design document for bug reporting feature
- [ ] **#35** Build comprehensive test framework for todo.ai `#tests` `#todoai`
  - [x] **#35.3** Create tests directory and draft detailed test plan document `#tests` `#docs`
  - [x] **#35.2** Define test framework architecture and tooling `#tests` `#planning`
  - [x] **#35.1** Research todo.ai testing requirements and existing docs `#tests` `#docs`


------------------

## Recently Completed
- [x] **#147** Fix issue#36: Task show command fails for deeply nested subtasks `#bug` (2025-11-16)
  > Issue #36 reports that 'show 1.2.1' fails with 'Task not found' even though task exists. Commands work for 1-level (#1) and 2-level (#1.2) but fail at 3-level (#1.2.1). This affects show, modify, note commands. Need to find task ID parsing/resolution logic and fix for arbitrary nesting depth. All 7 subtasks under #1.2 (tasks #1.2.1 through #1.2.7) affected.
  - [x] **#147.8** Commit fix and close issue#36 with release reference `#bug` (2025-11-16)
    > Issue #36 auto-closed by GitHub when commit contained 'Closes #36'. Added detailed comment explaining root cause, solution, and verification. Issue closed at 2025-11-15 11:47:54 UTC. Comment: https://github.com/fxstein/todo.ai/issues/36#issuecomment-3536410881
  - [x] **#147.7** Update documentation if nesting limitations exist `#bug` (2025-11-16)
    > Nesting limit (2 levels) is enforced by add-subtask command with clear error message: 'Maximum nesting depth is 2 levels (main task → subtask → sub-subtask)'. This serves as documentation. No README update needed. Fix supports arbitrary depth if limit is ever increased.
  - [x] **#147.6** Verify show, modify, note, complete, delete commands work on deep tasks `#bug` (2025-11-16)
    > Verified all commands work on 3-level deep tasks (148.1.1):
    > - show: ✓ Works (displays task + notes correctly)
    > - note: ✓ Works (added note successfully)
    > - modify: ✓ Works (changed description)
    > - complete: Testing now...
    > - delete: Will test after complete
  - [x] **#147.5** Test with 3, 4, and 5 level nested subtasks `#bug` (2025-11-16)
    > System enforces maximum nesting depth of 2 levels (main → subtask → sub-subtask). Cannot test 4-5 levels as add-subtask rejects deeper nesting. Fix supports arbitrary depth in case limit is increased. Tested successfully:
    > - Level 0: Task #148 ✓
    > - Level 1: Task #148.1 ✓
    > - Level 2: Task #148.1.1 ✓ (was failing, now fixed)
  - [x] **#147.4** Fix task ID resolution to support arbitrary nesting depth `#bug` (2025-11-16)
    > Fixed show_task() function in todo.ai:
    >
    > Line 4145: Changed from '^- \[.\] ... \|^  - \[.\]' to '^[ ]*- \[.*\]' (arbitrary nesting)
    > Line 4150: Same fix for fallback search
    > Line 4168: Same fix for note line number search  
    > Line 4173: Fixed note display regex from '^"  > " \| ^"    > "' to '^[[:space:]]*\> '
    >
    > All changes support arbitrary nesting depth and handle malformed checkboxes.
  - [x] **#147.3** Identify where show/modify/note commands fail for deep nesting `#bug` (2025-11-16)
    > Affected locations in show_task() function:
    >
    > Line 4143: Main task search - missing 4+ space patterns
    > Line 4148: Fallback search - missing 4+ space patterns  
    > Line 4164: Note line number search - missing 4+ space patterns
    >
    > For comparison, these functions ALREADY support 3 levels (0,2,4 spaces):
    > - Lines 2559, 2664, 2693: Task operations
    > - Lines 3035, 3040, 3061: More operations
    > - Line 4331: Another operation
    >
    > Solution: Use flexible pattern '^[ ]*- \[.\] \*\*#' to match ANY indentation depth
  - [x] **#147.2** Reproduce the bug with 3-level nested subtasks (1.2.1 pattern) `#bug` (2025-11-16)
    > Bug confirmed: Task #148.1.1 exists in TODO.md with 4-space indentation but 'show 148.1.1' returns 'Task not found'. Tasks #148 (0 spaces) and #148.1 (2 spaces) work correctly.
  - [x] **#147.1** Investigate task ID parsing logic for nested subtasks `#bug` (2025-11-16)
    > Search for functions: find_task_by_id(), get_task_by_id(), parse_task_id(), or similar. Look in action handlers for 'show', 'modify', 'note' commands. Check how task IDs are split (1.2.1 -> [1,2,1]) and how TODO.md is traversed. Likely issue: regex pattern or nesting loop only handles 2 levels.
- [x] **#149** Fix multi-line note indentation bug in add_note() function `#bug` (2025-11-16)
  > When adding multi-line notes, only the first line gets the blockquote marker (>) and proper indentation. Subsequent lines are inserted as raw text without indentation or markers, breaking TODO.md structure. Affects tasks 147.3 (lines 36-45), 147.4 (lines 27-32), 147.5 (lines 21-23), 147.6 (lines 14-18). Example: First line is '  > Text' but second line is just 'More text' instead of '  > More text'.
  - [x] **#149.7** Commit fix and verify TODO.md structure is valid `#bug` (2025-11-16)
  - [x] **#149.6** Manually fix broken notes in TODO.md (tasks 147.3-147.6) `#bug` (2025-11-16)
    > Manually fix ALL broken multi-line notes in TODO.md by adding proper indentation and blockquote markers (2 spaces + > + space for level-1 subtasks):
    >
    > **Original broken notes (from bug #36 work):**
    > - Task 147.3: Lines 36-45 need '  > ' prefix
    > - Task 147.4: Lines 27-32 need '  > ' prefix  
    > - Task 147.5: Lines 21-23 need '  > ' prefix
    > - Task 147.6: Lines 14-18 need '  > ' prefix
    >
    > **Newly broken notes (from creating task #149):**
    > - Task 149: Main task note (multi-line, needs '  > ' prefix)
    > - Task 149.1: Multi-line note about expected vs current behavior
    > - Task 149.6: This very note! (multi-line, needs '  > ' prefix)
    >
    > After fix, verify with './todo.ai show 147.3', './todo.ai show 149', etc. to ensure all notes display correctly.
    > Manually fix 4 broken notes in TODO.md by adding proper indentation and blockquote markers:
    > - Task 147.3: Lines 36-45 need '  > ' prefix (2 spaces + > + space)
    > - Task 147.4: Lines 27-32 need '  > ' prefix
    > - Task 147.5: Lines 21-23 need '  > ' prefix
    > - Task 147.6: Lines 14-18 need '  > ' prefix
    > After fix, verify with './todo.ai show 147.3' etc. to ensure notes display correctly.
  - [x] **#149.5** Test fix with multi-line notes at different nesting levels `#bug` (2025-11-16)
    > Tested multi-line notes at all 3 nesting levels:
    > 
    > Level 0 (main task): 0 spaces + 2 space blockquote = '  >' ✓
    > Level 1 (subtask): 2 spaces + 2 space blockquote = '    >' ✓
    > Level 2 (sub-subtask): 4 spaces + 2 space blockquote = '      >' ✓
    > 
    > All lines properly formatted with indent + '  > ' prefix. Fix verified!
  - [x] **#149.4** Fix add_note() to properly indent all lines with blockquote markers `#bug` (2025-11-16)
  > Fixed add_note() function with 3 key changes:
  > 
  > Line 4336: Updated grep to '^[ ]*- \[.*\]' for arbitrary nesting depth
  > Lines 4343-4350: Dynamic indent detection using regex to extract leading spaces  
  > Lines 4354-4362: Multi-line processing loop that adds indent + '  > ' to EACH line
  > 
  > This note itself tests the fix - all lines should have proper blockquote markers!
  - [x] **#149.3** Identify how note lines are processed and where indentation fails `#bug` (2025-11-16)
    > Bug located at line 4355 in add_note() function:
    >
    > local note_line="${indent}  > ${note_text}"
    >
    > This creates a single line by concatenating indent + '  > ' + entire note_text.
    > When note_text contains newlines, they're inserted as raw text without formatting.
    >
    > Fix needed: Split note_text by newlines, prepend '${indent}  > ' to EACH line.
  - [x] **#149.2** Find and analyze the add_note() function `#bug` (2025-11-16)
    > Search for 'add_note()' or '^add_note\(' function in todo.ai. Check how it processes note text, especially when note contains newlines. Look for where indentation prefix is calculated and where blockquote marker (>) is added. Likely splits note on newlines but only formats first line correctly.
  - [x] **#149.1** Document the multi-line note formatting bug with examples `#bug` (2025-11-16)
    > Current behavior vs expected:
    >
    > CURRENT (broken):
    >   > First line of note
    > Line 2 without marker
    > Line 3 without marker
    >
    > EXPECTED (correct):
    >   > First line of note
    >   > Line 2 with marker
    >   > Line 3 with marker
    >
    > All note lines must have proper indentation (matching task depth) AND blockquote marker (>).
- [x] **#152** Test bug reporting feature before v2.5.0 release `#testing` (2025-11-16)
  - [x] **#152.7** Verify GitHub issue template structure `#testing` (2025-11-16)
  - [x] **#152.6** Test label categorization for different error types `#testing` (2025-11-16)
  - [x] **#152.5** Verify markdown formatting (callout blocks, tables, collapsible) `#testing` (2025-11-16)
  - [x] **#152.4** Test human workflow (without env vars, should prompt) `#testing` (2025-11-16)
    > Human workflow tested and verified:
    > - WITHOUT AI env vars, shows full preview
    > - Prompts: 'Report this bug? (y/N)'  
    > - User must explicitly confirm with 'y'
    > - Cancelled if user says 'N' or presses Enter
    > - Maintains full user control as designed
    > 
    > Test: Ran './todo.ai report-bug "test" "test" "test"' without env vars
    > Result: Prompted for confirmation as expected ✓
  - [x] **#152.3** Test AI agent detection and auto-submission (with CURSOR_AI set) `#testing` (2025-11-16)
  - [x] **#152.2** Verify context collection (git, TODO.md, env vars, commands) `#testing` (2025-11-16)
  - [x] **#152.1** Test bug report generation with mock error `#testing` (2025-11-16)
- [x] **#153** Add note management: update and delete note commands `#feature` (2025-11-16)
  > Currently can only ADD notes with './todo.ai note <id> "text"'. Need to add:
  > - delete-note: Remove all notes from a task
  > - update-note: Replace existing notes with new text
  > 
  > This allows fixing mistakes, removing outdated info, and updating context without manual TODO.md editing.
  - [x] **#153.8** Update GETTING_STARTED.md with note management examples `#feature` (2025-11-16)
  - [x] **#153.7** Add commands to help text and usage documentation `#feature` (2025-11-16)
  - [x] **#153.6** Test note management at all nesting levels (0, 1, 2) `#feature` (2025-11-16)
    > Test scenarios:
    > 
    > 1. delete-note on task with single-line note
    > 2. delete-note on task with multi-line note
    > 3. delete-note on task with no notes (should error)
    > 4. update-note: single-line to single-line
    > 5. update-note: single-line to multi-line
    > 6. update-note: multi-line to single-line
    > 7. update-note: multi-line to multi-line
    > 8. Test at level 0 (main task), level 1 (subtask), level 2 (sub-subtask)
    > 9. Verify indentation correct after update
    > 10. Verify show command displays updated notes correctly
  - [x] **#153.5** Handle multi-line notes correctly in both commands `#feature` (2025-11-16)
  - [x] **#153.4** Implement update-note command to replace existing notes `#feature` (2025-11-16)
    > Implementation approach for update-note:
    > 
    > 1. Call delete-note logic to remove existing notes
    > 2. Call add_note() logic to add new notes
    > 3. Essentially: delete + add in one operation
    > 4. Ensures proper formatting via existing add_note()
    > 
    > Could be wrapper function:
    > update_note() {
    >   delete_note_internal $task_id  # No prompt version
    >   add_note $task_id $new_text
    > }
    > 
    > Reuse existing add_note() multi-line formatting logic from fix #149.
  - [x] **#153.3** Implement delete-note command to remove all notes from a task `#feature` (2025-11-16)
    > Implementation approach for delete-note:
    > 
    > 1. Find task line number (reuse logic from show_task)
    > 2. Find all consecutive blockquote lines after task
    > 3. Use sed or temp file to delete those lines
    > 4. Update footer timestamp
    > 5. Log the action
    > 
    > Reference collect_task_notes() function if it exists - may already have note detection logic. Similar pattern to delete_task() but only removes note lines, not the task itself.
  - [x] **#153.2** Analyze current note storage format in TODO.md `#feature` (2025-11-16)
    > Notes in TODO.md format:
    > - Appear as blockquotes immediately after task line
    > - Indentation matches task level + 2 spaces
    > - Each line starts with '  >' (indent + > + space)
    > - Can span multiple lines
    > - Ends when next non-blockquote line encountered
    > 
    > Example level-1 subtask:
    >   - [ ] **#42.1** Task description
    >     > Note line 1
    >     > Note line 2
    >     > Note line 3
    > 
    > Need to identify all note lines for delete/update operations.
  - [x] **#153.1** Design command syntax for update-note and delete-note `#feature` (2025-11-16)
    > Proposed command syntax:
    > 
    > ./todo.ai delete-note <task-id>
    >   - Removes ALL notes from specified task
    >   - Confirmation prompt: 'Delete all notes from task #X? (y/N)'
    >   - Returns error if task has no notes
    > 
    > ./todo.ai update-note <task-id> "new note text"
    >   - Replaces ALL existing notes with new text
    >   - Supports multi-line notes (like add note)
    >   - Shows preview: 'Replace N lines with M lines?'
    >   - Returns error if task has no notes to update
    > 
    > Alternative: Could add --force to skip confirmations for both commands.
- [x] **#155** Fix get_config_value sed fallback to work in bash (uses zsh-specific $match array) `#bug` (2025-11-16)
  > Fixed 3 critical $match[ ] usages in get_config_value() and get_highest_task_number(). Found 60 total occurrences throughout codebase. Need systematic conversion: all regex match references must check BASH_VERSION and use BASH_REMATCH[ ] for bash or $match[ ] for zsh.
- [x] **#157** Fix issue#38: Single-user mode assigns duplicate task IDs `#bug` (2025-11-16)
  > Critical data integrity bug in v2.4.0 and v2.5.0. Duplicate ID #21 assigned in single-user mode. Error context suggests relation to recent bash compatibility fixes (match array conversion). Issue reported at https://github.com/fxstein/todo.ai/issues/38
  - [x] **#157.9** Fix increment_serial() to check TODO.md for highest ID `#bug` (2025-11-16)
    > Fixed and tested. In no-coordination mode with serial=65, correctly assigned #159 (using TODO.md highest of 158).
    > Function increment_serial() (lines 1197-1213) blindly increments serial file without checking TODO.md. In no-coordination mode, assigned #65 when TODO.md highest was #158. Fix: Use MAX(serial_file, get_highest_task_number()) + 1. This is likely the actual root cause of issue#38.
  - [x] **#157.8** Close issue#38 with release reference `#bug` (2025-11-16)
  - [x] **#157.7** Prepare and release hotfix v2.5.1 `#bug` (2025-11-16)
    > Released as v2.7.0 with complete fix for issue#38.
    > Use release script with --patch flag. Update RELEASE_SUMMARY.md with hotfix details. Ensure both todo.ai and todo.bash are tested before release.
  - [x] **#157.6** Verify fix with both zsh and bash versions `#bug` (2025-11-16)
    > Created universal converter script (release/convert_zsh_to_bash.sh). Updated release.sh to use it. Tested: bash version correctly detects highest ID (158) and ignores blockquote examples.
  - [x] **#157.5** Add test cases for ID collision detection `#bug` (2025-11-16)
    > Created test_id_tracking.sh with 2 test cases. Both pass: (1) identifies highest ID from TODO.md, (2) ignores blockquote examples.
  - [x] **#157.4** Fix task ID tracking logic to prevent duplicates `#bug` (2025-11-16)
  - [x] **#157.3** Review impact of bash conversion markers on regex captures `#bug` (2025-11-16)
    > Bash conversion markers (# BASH_CONVERT) are NOT the cause. They're just comments and don't affect zsh execution.
    > Check if # BASH_CONVERT: BASH_REMATCH[1] comments are interfering with regex execution in zsh. Verify that conversion happens ONLY in bash version, not affecting zsh logic.
  - [x] **#157.2** Test ID assignment with completed tasks in TODO.md `#bug` (2025-11-16)
    > Test confirmed: New task assigned #158 (correct, not duplicate). Coordinator warning normal (behind by ~22 due to local development).
  - [x] **#157.1** Investigate get_highest_task_number() function for ID extraction bugs `#bug` (2025-11-16)
    > Root cause: get_highest_task_number() was scanning ALL lines including blockquote examples (e.g., line 77 with example #42.1). Function lines 3650-3659.
    > Focus on lines ~2500-2600 in todo.ai. Check regex pattern for extracting task IDs, especially handling of BASH_CONVERT markers and  usage. Verify it correctly reads all task IDs including completed ones.
- [x] **#132** Optimize todo.ai codebase: reduce size and complexity `#optimization` (2025-11-12)
  > Current codebase is 5952 lines. Goal: reduce size and complexity by removing obsolete code, cleaning up old migrations, and improving maintainability. See docs/analysis/CODE_SIZE_ANALYSIS.md for detailed breakdown and recommendations.
  - [x] **#132.3** Explore bash version of todo.ai: evaluate impact on file size and platform compatibility `#research` (2025-11-12)
    > Smart installer created: install.sh detects OS/shell and installs optimal version. See docs/design/SMART_INSTALLER_DESIGN.md for full design. One-liner: curl -fsSL .../install.sh | sh maintains simplicity while adding intelligence.
    > Compare bash vs zsh syntax differences, evaluate portability benefits (works on more platforms), analyze if simpler syntax reduces file size. Current tool is zsh-specific with features like [[ ]], read patterns, arrays.
    - [x] **#132.3.4** Create bash vs zsh analysis document - document pros/cons, recommendation, and migration considerations `#research` (2025-11-12)
    - [x] **#132.3.3** Compare bash vs zsh versions - file size, performance, syntax complexity, and platform compatibility `#research` (2025-11-12)
    - [x] **#132.3.2** Test bash version functionality - verify all commands work correctly and produce identical output `#research` (2025-11-12)
    - [x] **#132.3.1** Create bash version of todo.ai (todo.bash) - convert zsh-specific syntax to bash-compatible equivalents `#research` (2025-11-12)
  - [x] **#132.2** Remove old migration logic: keep migration shell but eliminate version-specific migration code `#refactor` (2025-11-12)
    > Keep MIGRATIONS array and run_migrations() infrastructure, but remove all version-specific migration functions (v1_3_5, v2_0_0_cursor_rules, v2_1_0_git_coordination). Add comments pointing to git history for old migrations if needed for legacy installs. See docs/analysis/CODE_SIZE_ANALYSIS.md lines 66-67 for details.
  - [x] **#132.1** Create code size analysis document documenting current state and optimization opportunities `#docs` (2025-11-12)
    > Analysis document created at docs/analysis/CODE_SIZE_ANALYSIS.md - documents current 5952 lines with breakdown by functionality and identifies optimization opportunities
- [x] **#146** Test task#144 implementation before release `#test` (2025-11-12)
  > Validate all task#144 features before creating release: bash conversion, smart installer, release assets. All tests passed successfully. Release v2.4.0 is LIVE with smart installer, bash version, and automated conversion workflow.
  - [x] **#146.7** Clean up pre-release and verify ready for production release `#test` (2025-11-12)
    > v2.4.0 created and tested successfully. Converted from pre-release to production for installer testing. All tests passed: bash conversion works, smart installer works, both versions identical. Release is LIVE and ready for production use.
  - [x] **#146.6** Verify zsh and bash versions produce identical results `#test` (2025-11-12)
    > Both versions validated identical: version 2.4.0, add/subtask/note/complete all work. File sizes 253045 (zsh) vs 253019 (bash) - only 26 byte difference. 16 lines changed in conversion. Earlier tests confirmed 100% functionality parity.
  - [x] **#146.5** Test smart installer with pre-release assets `#test` (2025-11-12)
  - [x] **#146.4** Create pre-release with all assets for testing `#test` (2025-11-12)
  - [x] **#146.3** Test smart installer fallback to main branch `#test` (2025-11-12)
    > Installer correctly detects v.3.1 but assets don't exist (404). This is expected - v2.3.1 was before task#144. Need pre-release with new assets to test full flow. Fallback logic working correctly.
  - [x] **#146.2** Test bash version functionality matches zsh version `#test` (2025-11-12)
  - [x] **#146.1** Test bash conversion with release.sh --prepare `#test` (2025-11-12)
- [x] **#144** Implement release-aware smart installer with bash/zsh dual-version support `#feature` (2025-11-12)
  > Smart installer that detects OS/shell and installs optimal version (zsh/bash). Installs from releases (not main branch) to avoid incomplete/broken commits. Clear dev workflow: develop in zsh, auto-convert to bash during release. Released in v2.4.0.
  - [x] **#144.9** Update release script to include both todo.ai and todo.bash as assets `#release` (2025-11-12)
  - [x] **#144.8** Add cursor rule to prevent accidental todo.bash editing `#docs` (2025-11-12)
  - [x] **#144.7** Update GETTING_STARTED.md and other documentation references `#docs` (2025-11-12)
  - [x] **#144.6** Update README.md with smart installer as primary method `#docs` (2025-11-12)
  - [x] **#144.5** Create concise smart installer documentation `#docs` (2025-11-12)
  - [x] **#144.4** Test smart installer on multiple platforms and scenarios `#test` (2025-11-12)
  - [x] **#144.3** Create release-aware smart installer script (install.sh) `#installer` (2025-11-12)
  - [x] **#144.2** Add automated bash conversion to release script `#release` (2025-11-12)
  - [x] **#144.1** Create development guidelines document for zsh-first workflow `#docs` (2025-11-12)
- [x] **#145** Reorganize docs folder with logical subdirectory structure `#docs` (2025-11-11)
  > Proposed structure: guides/ (user docs), design/ (technical specs), development/ (contributor docs), analysis/ (research), archive/ (historical). Currently 29 files in flat structure need categorization and organization. Must update all cross-references, docs/README.md, and main README.md links.
  - [x] **#145.11** Verify all links work and no broken references remain `#docs` (2025-11-11)
    > Test: (1) Click through all links in README.md, (2) Check docs/README.md links, (3) Verify cross-references between docs, (4) Check .cursor/rules references, (5) Test any links in todo.ai script itself. Use grep to find any remaining old paths that weren't updated.
  - [x] **#145.10** Update main README.md documentation links `#docs` (2025-11-11)
    > Update Documentation section in main README.md (around line 177): Update paths to GETTING_STARTED, NUMBERING_MODES_GUIDE, USAGE_PATTERNS, COORDINATION_SETUP. Add link to docs/README.md for full documentation index.
  - [x] **#145.9** Update docs/README.md with new structure overview `#docs` (2025-11-11)
    > Rewrite docs/README.md as index: (1) Overview of documentation structure, (2) Quick links to key guides, (3) Directory descriptions (guides/, design/, development/, analysis/, archive/), (4) How to contribute/where to add new docs. Keep concise, scannable.
  - [x] **#145.8** Update all cross-references in documentation files `#docs` (2025-11-11)
    > Find all doc links: grep -r 'docs/.*\.md' . --include='*.md' --include='*.mdc'. Update relative paths to new structure (e.g., docs/INSTALLATION.md -> docs/guides/INSTALLATION.md). Check todo.ai script, .cursor/rules/, README.md, all docs/*.md files.
  - [x] **#145.7** Move historical/migration docs to docs/archive/ `#docs` (2025-11-11)
    > Move to archive/: COMMIT_FORMAT_MIGRATION.md, CURSOR_RULES_MIGRATION.md, RELEASE_NUMBERING_MAPPING.md, README_PREVIEW_WITH_SMART_INSTALLER.md (4 files - historical/completed migrations). Use git mv.
  - [x] **#145.6** Move analysis/research docs to docs/analysis/ `#docs` (2025-11-11)
    > Move to analysis/: BASH_VS_ZSH_ANALYSIS.md, CODE_SIZE_ANALYSIS.md, GITHUB_API_COORDINATION_ANALYSIS.md, IMPLEMENTATION_ALTERNATIVES_ANALYSIS.md, MULTI_USER_CONFLICT_ANALYSIS.md, MULTI_USER_TOOL_RESEARCH.md, TASK_NUMBERING_SCHEMA_ANALYSIS.md (7 files). Use git mv.
  - [x] **#145.5** Move development/contributor docs to docs/development/ `#docs` (2025-11-11)
    > Move to development/: DEVELOPMENT_GUIDELINES.md, MIGRATION_GUIDE.md, NUMBERING_MODES_TEST_PLAN.md, TODO_TOOL_IMPROVEMENTS.md (4 files). Use git mv.
  - [x] **#145.4** Move design documents to docs/design/ `#docs` (2025-11-11)
    > Move to design/: BUG_REPORTING_DESIGN.md, GIT_HOOKS_DESIGN.md, HYBRID_TASK_NUMBERING_DESIGN.md, MIGRATION_SYSTEM_DESIGN.md, MULTI_USER_DESIGN.md, SMART_INSTALLER_DESIGN.md, TODO_TAGGING_SYSTEM_DESIGN.md, UNINSTALL_DESIGN.md (8 files). Use git mv.
  - [x] **#145.3** Move user guide files to docs/guides/ `#docs` (2025-11-11)
    > Move to guides/: GETTING_STARTED.md, INSTALLATION.md, USAGE_PATTERNS.md, NUMBERING_MODES_GUIDE.md, COORDINATION_SETUP.md (5 files). Use git mv to preserve history.
  - [x] **#145.2** Create subdirectory structure in docs folder `#docs` (2025-11-11)
    > Create directories: mkdir -p docs/{guides,design,development,analysis,archive}. Verify structure with tree or ls. Do not move files yet - that's next step.
  - [x] **#145.1** Define and document docs folder structure with categories `#docs` (2025-11-11)
    > Create docs/STRUCTURE.md documenting: guides/ (GETTING_STARTED, INSTALLATION, USAGE_PATTERNS, NUMBERING_MODES_GUIDE, COORDINATION_SETUP), design/ (8 design docs), development/ (DEVELOPMENT_GUIDELINES, MIGRATION_GUIDE, test plans), analysis/ (7 analysis/research docs), archive/ (migration/historical docs). Keep README.md at root with overview.
- [x] **#143** Prevent stale release summaries from being used in releases `#bug` (2025-11-11)
  > Tested with old file (2024-11-11) vs v2.3.0 (2025-11-11): correctly detected and aborted. Fresh file passes validation.
  > Bug caused v2.3.0 to be released with v2.2.1's summary. Script used stale release/RELEASE_SUMMARY.md without validation. Fix: Check if summary file mtime > last release tag date.
  - [x] **#143.5** Test: Verify detection works with old and new summary files `#bug` (2025-11-11)
  - [x] **#143.4** Option: Prompt to continue or abort if stale summary detected `#bug` (2025-11-11)
  - [x] **#143.3** Add warning if summary appears stale (older than last release) `#bug` (2025-11-11)
  - [x] **#143.2** Add validation: Compare summary file mtime with last release tag date `#bug` (2025-11-11)
  - [x] **#143.1** Investigate: How to detect if summary file is stale `#bug` (2025-11-11)
- [x] **#142** Fix release script bug: version verification fails when version already updated in working directory `#bug` (2025-11-11)
  > Execute mode assumes version needs updating, but if version already changed in working dir (from failed attempt), commit has no changes and version_commit_hash points to old commit. Need to handle case where version already correct.
  - [x] **#142.4** Test: Verify execute works after failed/aborted release attempt `#test` (2025-11-11)
  - [x] **#142.3** Fix: Get correct commit hash when 'no commit needed' returned `#code` (2025-11-11)
  - [x] **#142.2** Fix: Handle case where version already correct in working directory `#code` (2025-11-11)
  - [x] **#142.1** Investigate execute_release: why version verification fails `#bug` (2025-11-11)
- [x] **#141** Redesign release workflow: separate prepare (default) and execute steps, eliminate prompts `#feature` (2025-11-11)
  > New workflow: release.sh defaults to --prepare (analyze, preview, show execution command). Then run release.sh --execute to perform release. No prompts in either mode.
  - [x] **#141.9** Update release documentation and Cursor rules with new workflow `#docs` (2025-11-11)
  - [x] **#141.8** Test execute mode: verify release completes without any prompts `#test` (2025-11-11)
  - [x] **#141.7** Test prepare mode: verify preview displays correctly with execution command `#test` (2025-11-11)
  - [x] **#141.6** Add highlighted execution command at end of prepare step output `#code` (2025-11-11)
    > Display: 'To execute this release, run: ./release/release.sh --execute' in green/highlighted text at end of prepare output.
  - [x] **#141.5** Remove all interactive prompts from both modes `#code` (2025-11-11)
  - [x] **#141.4** Implement --execute mode: perform release without prompts (version, tag, push, GitHub) `#code` (2025-11-11)
    > Read prepared release data from temp/cache. Update version, commit, tag, push to GitHub, create release. Exit with error if prepare not run first.
  - [x] **#141.3** Implement --prepare mode (default): analyze commits, generate notes, show preview only `#code` (2025-11-11)
    > Default behavior when called without --execute. Generate preview, save to temp file, display release notes. End with highlighted command to execute.
  - [x] **#141.2** Design new workflow: prepare (default) vs execute modes `#design` (2025-11-11)
  - [x] **#141.1** Analyze current release.sh: identify all prompts and manual confirmation points `#research` (2025-11-11)
- [x] **#139** Enhance show command to display notes for subtasks, not just parent task `#feature` (2025-11-11)
  > Investigate show_task() function. Currently only displays notes for parent task. Need to display notes for all subtasks shown in output.
  - [x] **#139.7** Test: verify nested subtask notes displayed correctly `#test` (2025-11-11)
  - [x] **#139.6** Test: verify subtask notes displayed for all subtasks `#test` (2025-11-11)
    > This note should appear in show output after implementing the fix - verifies subtask notes are displayed.
    - [ ] **#139.6.1** Nested sub-subtask with note for testing `#test` (2025-11-11)
      > This nested sub-subtask note should also appear in show output after fix - verifies all nesting levels work.
  - [x] **#139.5** Test: verify parent task note displayed `#test` (2025-11-11)
  - [x] **#139.4** Implement fix: modify show_task to display notes after each task/subtask line `#code` (2025-11-11)
    > Modify show_task() to call collect_task_notes() for each displayed task/subtask. Display notes immediately after each task line.
  - [x] **#139.3** Design solution: show notes for parent task and all displayed subtasks `#design` (2025-11-11)
  - [x] **#139.2** Verify current behavior: confirm only parent notes shown, subtask notes missing `#bug` (2025-11-11)
  - [x] **#139.1** Investigate show_task function: find where notes are displayed `#research` (2025-11-11)
    > Find show_task() function in todo.ai script. Look for note display logic around lines 4000-4100.
- [x] **#140** Fix bug: Note command doesn't work for nested sub-subtasks (4-space indentation) `#bug` (2025-11-11)
  > add_note() line 4303 only searches for 0-space and 2-space patterns, missing 4-space sub-subtask pattern. Need to add: |^    - \[.\] \*\*#\*\*
- [x] **#136** Fix bug: Adding subtask splits task notes - subtask inserts between task and note `#bug` (2025-11-09)
  > Investigate add_subtask() function. Fix to insert subtasks after parent task notes, not between task and notes.
- [x] **#131** Create Cursor rule encouraging agents to use notes for task implementation details `#feature` (2025-11-09)
  > Rule should encourage agents to add notes for: implementation approach, technical decisions, context about why certain choices were made, file locations to modify, dependencies between tasks. Keep rule short (~15-20 lines) following cursor-rules-guidelines.mdc principles.
  - [x] **#131.5** Test rule installation and verify agents follow note-adding guidelines `#test` (2025-11-09)
  - [x] **#131.4** Add rule to init_cursor_rules() function in todo.ai script `#code` (2025-11-09)
  - [x] **#131.3** Create .cursor/rules/todo.ai-task-notes.mdc with concise guidelines and examples `#code` (2025-11-09)
  - [x] **#131.2** Draft Cursor rule: define when agents should add notes to tasks (implementation details, context, decisions) `#docs` (2025-11-09)
  - [x] **#131.1** Research current note usage patterns: when and how notes are used in TODO.md `#research` (2025-11-09)
- [x] **#130** Fix issue#32: Archive command doesn't move task notes with the task `#bug` (2025-11-09)
  - [x] **#130.10** Verify no orphaned notes remain in active section after archiving `#bug` (2025-11-09)
  - [x] **#130.9** Test with nested subtasks (2 levels) with notes at each level `#bug` (2025-11-09)
  - [x] **#130.8** Test with parent task and subtasks with notes (verify all notes move) `#bug` (2025-11-09)
  - [x] **#130.7** Test with single task with note (verify note moves with task) `#bug` (2025-11-09)
  - [x] **#130.6** Implement note insertion: include notes in archived block with proper structure `#bug` (2025-11-09)
  - [x] **#130.5** Implement note removal: remove blockquotes from active section when archiving `#bug` (2025-11-09)
  - [x] **#130.4** Implement note collection: gather blockquotes after main task and each subtask `#bug` (2025-11-09)
  - [x] **#130.3** Design solution: create function to collect notes for a task and all its subtasks `#bug` (2025-11-09)
  - [x] **#130.2** Analyze delete_task function: study how it properly removes notes (lines 2926-2935) `#bug` (2025-11-09)
  - [x] **#130.1** Investigate archive_task function: how notes are currently handled (or not handled) `#bug` (2025-11-09)
- [x] **#135** Test nested subtasks with notes `#test` (2025-11-09)
  - [x] **#135.1** Level 1 subtask `#test` (2025-11-09)
    - [x] **#135.1.1** Level 2 subtask `#test` (2025-11-09)
    > Level 1 note
  > Level 0 parent note
- [x] **#134** Test parent task with subtasks and notes `#test` (2025-11-09)
  - [x] **#134.2** Subtask two with note `#test` (2025-11-09)
    > Subtask two note - should move with subtask
  - [x] **#134.1** Subtask one with note `#test` (2025-11-09)
    > Subtask one note - should move with subtask
  > Parent task note - should move with parent
- [x] **#133** Test task with note for archive bug fix `#test` (2025-11-09)
  > This is a test note that should move with the task when archived
- [x] **#126** Fix issue#27: Setup coordinator automatically switches to enhanced mode without user consent (fixed - setup-coordination now preserves current mode) `#bug` (2025-11-02)
  - [ ] **#126.4** Add tests to verify coordination setup doesn't change numbering mode `#bug` `#test` (2025-11-02)
  - [x] **#126.3** Fix setup-coordination to preserve current mode when configuring coordination (completed - fixed hardcoded enhanced mode) `#bug` (2025-11-02)
  - [x] **#126.2** Verify coordination should work with single-user mode without forcing enhanced (verified - validation supports single-user + coordination) `#bug` (2025-11-02)
  - [x] **#126.1** Investigate setup-coordination command mode switching logic (completed - found hardcoded mode: enhanced on line 3353) `#bug` (2025-11-02)
- [x] **#52** Design multi-user/multi-branch/PR support system for todo.ai with conflict-free task numbering `#feature` `#MAJOR` (2025-11-02)
  - [x] **#52.24** Document setup instructions for each coordination service: prerequisites, configuration steps, and verification `#docs` (2025-11-02)
  - [x] **#52.23** Add setup wizard/command that guides users through mode and coordination selection with validation `#feature` (2025-11-02)
  - [x] **#52.22** Create comprehensive documentation for all mode and coordination combinations (single-user, multi-user, branch, enhanced with github-issues, counterapi, none) `#docs` (2025-11-02)
  - [x] **#52.21** Implement automated setup command for coordination services (github-issues, counterapi) with interactive prompts `#code` (2025-11-02)
  - [x] **#52.20** Create function to detect and list available coordination options based on system capabilities (gh CLI, curl, jq, python3, etc.) `#code` (2025-11-02)
  - [x] **#52.19** Verify current operating mode display and mode switching functionality `#test` (2025-11-02)
  - [x] **#52.18** Test fallback scenarios: verify graceful degradation when coordination services are unavailable `#test` (2025-11-02)
  - [x] **#52.17** Test conflict resolution: verify automatic detection and renumbering of duplicate task IDs `#test` (2025-11-02)
  - [x] **#52.16** Test mode switching: verify migration, backup creation, and rollback functionality `#test` (2025-11-02)
  - [x] **#52.15** Test all numbering modes: verify correct task assignment, reference resolution, and conflict handling `#test` (2025-11-02)
  - [x] **#52.14** Create user documentation: guide for adopting and switching between numbering modes `#docs` (2025-11-02)
  - [x] **#52.13** Implement task reference resolution: auto-add user prefix when user references tasks by number only `#code` (2025-11-02)
  - [x] **#52.12** Implement conflict resolution system: automatic detection and renumbering of duplicate task IDs `#code` (2025-11-02)
  - [x] **#52.11** ✅ Implemented Mode 4 (Enhanced Multi-User) - GitHub Issues/CounterAPI coordination `#code` (2025-11-02)
  - [x] **#52.10** ✅ Implemented Mode 3 (Branch Mode) - branch prefix-based numbering `#code` (2025-11-02)
  - [x] **#52.9** ✅ Implemented Mode 2 (Multi-User) - prefix-based numbering `#code` (2025-11-02)
  - [x] **#52.8** ✅ Implemented Mode 1 (Single-User) - backward compatible `#code` (2025-11-02)
  - [x] **#52.7** ✅ Implemented configuration system (YAML reading, validation, mode detection) `#code` `#test` (2025-11-02)
  - [x] **#52.6** Implement automatic migration path between numbering modes: renumber tasks when switching modes `#code` (2025-11-02)
  - [x] **#52.5** Implement mode switching command: allow users to switch between numbering modes (single-user, multi-user, branch, enhanced) `#code` (2025-11-02)
  - [x] **#52.4** ✅ Implemented backup and rollback system for mode switching `#code` `#safety` (2025-11-02)
  - [x] **#52.3** Design document: propose solution architecture for conflict-free task numbering in multi-user environment `#docs` (2025-11-02)
  - [x] **#52.2** Research existing solutions: how other task management tools handle multi-user numbering conflicts `#research` (2025-11-02)
  - [x] **#52.1** Analyze need: identify scenarios where multi-user/multi-branch task conflicts occur `#research` (2025-11-02)
- [x] **#53** Fix bug reporting: reports to wrong repository (customer repo instead of todo.ai repo) `#bug` (2025-11-02)
  - [x] **#53.1** Test bug reporting from a different repository to verify it reports to todo.ai repo (2025-11-02)
- [x] **#55** Fix update command when installed to system directory in PATH (GitHub issue #17) `#bug` (2025-11-02)
  - [x] **#55.4** Close GitHub issue #17 when fix has been confirmed `close-issue` (2025-11-02)
  - [x] **#55.3** Test update command from system-wide installation location `#test` (2025-11-02)
  - [x] **#55.2** Fix get_script_path() to handle system-wide installations in /usr/local/bin or /usr/bin `#code` (2025-11-02)
  - [x] **#55.1** Investigate get_script_path() function: how it detects script location when installed system-wide `#research` (2025-11-02)
- [x] **#56** Fix release script: exclude .todo.ai/.todo.ai.serial from uncommitted changes check `#bug` (2025-11-02)
- [x] **#46** Fix release numbering bug: cursor rules migration incorrectly classified as PATCH instead of MINOR `#bug` (2025-11-02)
  - [x] **#46.6** Create mapping document: tags to release types with priority matrix showing numbering decisions `#docs` (2025-11-02)
  - [x] **#46.5** Test fix: verify cursor rules migration would be classified as MINOR with fix applied `#test` (2025-11-02)
  - [x] **#46.4** Handle ambiguous cases: migrations that affect users vs pure infrastructure changes `#code` (2025-11-02)
  - [x] **#46.3** Implement fix: check for functional changes in todo.ai before file-based classification `#code` (2025-11-02)
  - [x] **#46.2** Design fix: prioritize commit message prefixes (feat:) over file analysis for user-facing features `#docs` (2025-11-02)
  - [x] **#46.1** Investigate release numbering logic: why feat: commits with .cursor/rules/ changes are classified as PATCH `#research` (2025-11-02)
- [x] **#50** Investigate task numbering schema to avoid GitHub issue/PR number conflicts in commit messages `#research` (2025-11-02)
  - [x] **#50.4** Check existing commits for wrong format (#nn instead of task#nn) and create migration plan to fix or document them `#code` (2025-11-02)
  - [x] **#50.3** Propose solution: design numbering schema or commit message format to avoid conflicts `#docs` (2025-11-02)
  - [x] **#50.2** Research alternative numbering schemas: prefixes, formats, or conventions to distinguish task numbers from GitHub issues/PRs `#research` (2025-11-02)
  - [x] **#50.1** Create analysis document: investigate how GitHub treats task numbers in commit messages and potential conflicts with issue/PR numbers `#docs` (2025-11-02)
- [x] **#15** Setup git hooks with pre-commit validation for Markdown, YAML, JSON, and TODO.md linting `#setup` `#git` (2025-11-02)
- [x] **#19** Move Deleted Tasks section below Recently Completed section `#setup` (2025-11-02)
- [x] **#37** Build release migration and cleanup system for one-time migrations and cleanups `#feature` (2025-11-02)
  - [x] **#37.12** Update release process documentation to include migration workflow (2025-11-02)
  - [x] **#37.11** Document migration creation process for developers (2025-11-02)
  - [x] **#37.10** Test migration system with real TODO.md files (wrong section order) (2025-11-02)
  - [x] **#37.9** Create integration tests for migration execution during update (2025-11-02)
  - [x] **#37.8** Create unit tests for migration system (version comparison, idempotency) (2025-11-02)
  - [x] **#37.7** Add migration execution to script startup (after version check) (2025-11-02)
  - [x] **#37.6** Implement first migration: section order fix (v1.3.5) (2025-11-02)
  - [x] **#37.5** Create migration lock mechanism to prevent concurrent execution (2025-11-02)
  - [x] **#37.4** Implement migration execution system with run_migrations function (2025-11-02)
  - [x] **#37.3** Implement version comparison function for semantic versioning (2025-11-02)
  - [x] **#37.2** Create migration registry structure in todo.ai script (2025-11-02)
  - [x] **#37.1** Create design document for migration/cleanup system architecture (2025-11-02)
- [x] **#44** Migrate cursor rules from .cursorrules to .cursor/rules/ directory structure `#migration` (2025-11-02)
  - [x] **#44.10** Cleanup .cursorrules during migration: remove todo.ai references and create timestamped backup before edits `#code` (2025-11-02)
  - [x] **#44.9** Manage installation path of tool relative to cursor rules `#code` (2025-11-02)
  - [x] **#44.8** Update release process docs to reference .cursor/rules/ instead of .cursorrules `#docs` (2025-11-02)
  - [x] **#44.7** Update documentation to reflect .cursor/rules/ structure `#docs` (2025-11-02)
  - [x] **#44.6** Test migration with existing .cursorrules files `#test` (2025-11-02)
  - [x] **#44.5** Create migration to convert existing .cursorrules to .cursor/rules/ on update `#migration` (2025-11-02)
  - [x] **#44.4** Update init_cursor_rules to create .cursor/rules/ structure instead of .cursorrules file `#code` (2025-11-02)
  - [x] **#44.3** Implement migration logic to convert .cursorrules sections to .mdc files `#code` (2025-11-02)
  - [x] **#44.2** Create design document for .cursorrules to .cursor/rules/ migration `#docs` (2025-11-02)
  - [x] **#44.1** Verify .cursor/rules/ is the latest official Cursor implementation from docs.cursor.com `#research` (2025-11-02)
- [x] **#43** Create uninstall feature (2025-11-02)
  - [x] **#43.4** Create dedicated cursor rule for uninstall process: require agents to use ./todo.ai uninstall command and NOT delete files directly to control uninstall scope `#code` (2025-11-02)
  - [x] **#43.3** Enhance README.md to show simple uninstall command (2025-11-02)
  - [x] **#43.2** Implement and test uninstall feature (2025-11-02)
  - [x] **#43.1** Write design document for uninstall feature (2025-11-02)
- [x] **#48** Fix update logic error: new version update logic never executes (2025-11-02)
  - [x] **#48.4** Test update workflow: verify migrations execute in new version after update `#test` (2025-11-02)
  - [x] **#48.3** Implement update fix: execute new version's migrations and update logic before replacement `#code` (2025-11-02)
  - [x] **#48.2** Design solution: download → execute new version → replace old version `#docs` (2025-11-02)
  - [x] **#48.1** Research update execution pattern: how to execute new version's code after download `#research` (2025-11-02)
- [x] **#38** Fix orphaned subtasks bug: delete subtasks when deleting parent task `#bug` (2025-11-01)
  - [x] **#38.6** Verify orphaned subtask detection still works correctly (2025-11-01)
  - [x] **#38.5** Test deletion of subtask only (should not delete parent or siblings) (2025-11-01)
  - [x] **#38.4** Test deletion of parent task with nested subtasks (2-level) (2025-11-01)
  - [x] **#38.3** Test deletion of parent task with subtasks (verify subtasks deleted) (2025-11-01)
  - [x] **#38.2** Implement automatic subtask deletion when deleting parent task (2025-11-01)
  - [x] **#38.1** Analyze current delete_task function behavior (2025-11-01)
- [x] **#14** Formatting fixes complete `#setup` (2025-11-01)
- [x] **#7** Remove gitignore entry for .todo.ai directory - .todo.ai/ must be tracked in git `#setup` `#git` (2025-11-01)
- [x] **#5** Initialize repository structure and configuration `#setup` `#repo` (2025-11-01)
- [x] **#36** Create release process for todo.ai on GitHub (2025-11-01)
  - [x] **#36.5** Review and finetune release numbering logic (2025-11-01)
  - [x] **#36.4** Create permanent release log file with detailed timestamps (2025-11-01)
  - [x] **#36.3** Create release management process (2025-11-01)
  - [x] **#36.2** Review release process document (2025-11-01)
  - [x] **#36.1** Create release process document (2025-11-01)
- [x] **#32** Implement nested subtasks support (2-level limit) `#feature` (2025-10-30)
- [x] **#28** Rename files in .todo.ai/ to .todo.ai.log and .todo.ai_serial `#setup` (2025-10-30)
- [x] **#17** Create Cursor rules for repository `#setup` `#docs` (2025-10-30)
- [x] **#26** Rename .todo/ directory to .todo.ai/ `#setup` (2025-10-30)
- [x] **#25** Rename repository from todo to todo.ai `#setup` (2025-10-30)
- [x] **#23** Rename todo.ai to todo.ai `#setup` (2025-10-30)
- [x] **#22** Create update instructions and functions for todo.ai `#setup` (2025-10-30)
- [x] **#20** Create radically simplified README.md `#docs` (2025-10-30)
- [x] **#6** Update TODO.md template for this repository `#setup` `#docs` (2025-10-30)
- [x] **#18** Fix TODO.md header upon initialization - use repo name dynamically `#fix` `#setup` (2025-10-30)
- [x] **#13** All formatting fixes complete `#setup` (2025-10-30)
- [x] **#12** Final formatting test `#test` (2025-10-30)
- [x] **#11** Test new append method `#test` (2025-10-30)
- [x] **#10** Verify formatting works correctly `#test` (2025-10-30)
- [x] **#8** Fix all sed -i calls to use sed_inplace for macOS compatibility `#setup` `#fix` (2025-10-30)

## Deleted Tasks
- [D] **#159** Test task with fixed serial logic (deleted 2025-11-15, expires 2025-12-15)
- [D] **#65** Test task for no-coordination mode (deleted 2025-11-15, expires 2025-12-15)
- [D] **#158** Test task for ID tracking bug fix (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.1** Reproduce bug: create task with note, add subtask, verify note is split `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.2** Investigate add_subtask function: find where subtask insertion occurs `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.3** Analyze note detection: how to identify and skip over notes when inserting subtasks `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.4** Design solution: insert subtasks after task AND any following notes `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.5** Implement fix: modify add_subtask to skip over blockquotes before insertion `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.6** Test: task with note + add first subtask (note should stay with parent) `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.7** Test: task with multiple notes + add subtask (all notes stay with parent) `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.8** Test: add second subtask when first subtask already exists with notes `#bug` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#136.9** Verify note positioning remains correct after multiple subtask additions `#bug` (deleted 2025-11-15, expires 2025-12-15)
- [D] **#136** Global fix test `#test` (deleted 2025-11-15, expires 2025-12-15)
- [D] **#156** Clean bash test `#test` (deleted 2025-11-15, expires 2025-12-15)
    - [D] **#154.1.1** Level 2 sub-subtask `#test` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#154.1** Level 1 subtask `#test` (deleted 2025-11-15, expires 2025-12-15)
- [D] **#154** Test note management commands `#testing` (deleted 2025-11-15, expires 2025-12-15)
    - [D] **#151.1.1** Level 2 sub-subtask `#test` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#151.1** Level 1 subtask `#test` (deleted 2025-11-15, expires 2025-12-15)
- [D] **#151** Test fix level 0 `#test` (deleted 2025-11-15, expires 2025-12-15)
    - [D] **#150.1.1** Test level 2 sub-subtask `#test` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#150.1** Test level 1 subtask `#test` (deleted 2025-11-15, expires 2025-12-15)
- [D] **#150** Test main task (level 0) `#test` (deleted 2025-11-15, expires 2025-12-15)
    - [D] **#148.1.2** Test delete on level 2 `#test` (deleted 2025-11-15, expires 2025-12-15)
    - [D] **#148.1.1** Level 2 sub-subtask (MODIFIED to verify fix works) `#test` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#148.1** Level 1 subtask `#test` (deleted 2025-11-15, expires 2025-12-15)
- [D] **#148** Test parent task `#test` (deleted 2025-11-15, expires 2025-12-15)
  - [D] **#125.5** Test bug reporting flow with automated agent execution `#bug` `#test` (deleted 2025-11-12, expires 2025-12-12)
  - [D] **#125.4** Add context detection to auto-fill relevant information without prompts `#bug` (deleted 2025-11-12, expires 2025-12-12)
  - [D] **#125.3** Improve bug report formatting with better markdown structure `#bug` (deleted 2025-11-12, expires 2025-12-12)
  - [D] **#125.2** Update bug report template for better readability and structure `#bug` (deleted 2025-11-12, expires 2025-12-12)
  - [D] **#125.1** Eliminate user prompts - make bug reporting fully automated for AI agents `#bug` (deleted 2025-11-12, expires 2025-12-12)
    - [D] **#138.1.1** Nested sub-subtask `#test` (deleted 2025-11-09, expires 2025-12-09)
  - [D] **#138.1** First subtask after fix `#test` (deleted 2025-11-09, expires 2025-12-09)
  - [D] **#138.2** Second subtask after multiple notes `#test` (deleted 2025-11-09, expires 2025-12-09)
- [D] **#138** Test fix: task with note `#test` (deleted 2025-11-09, expires 2025-12-09)
  - [D] **#137.1** First subtask `#test` (deleted 2025-11-09, expires 2025-12-09)
- [D] **#137** Test bug reproduction `#test` (deleted 2025-11-09, expires 2025-12-09)
- [D] **#124** Convince the coffee machine to understand sarcasm `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [  D] **#123.1** Investigate delete command placement logic for Deleted Tasks section (completed - found footer boundary check missing) `#bug`
  - [  D] **#123.2** Verify expected section order: Tasks -> Recently Completed -> Deleted Tasks -> Footer (verified - order is now correct) `#bug`
  - [  D] **#123.3** Fix delete command to place Deleted Tasks section before footer (completed - updated ensure_deleted_section function) `#bug`
  - [D] **#123.4** Add tests to verify correct section ordering `#bug` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#123** Fix issue#25: Deleted tasks section placement - footer appears before Deleted Tasks section instead of after `#bug` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-106** clean the car (deleted 2025-11-02, expires 2025-12-02)
- [D] **#64** Test after fix (deleted 2025-11-02, expires 2025-12-02)
- [D] **#63** Test coordination after mode switch (deleted 2025-11-02, expires 2025-12-02)
- [D] **#62** Test coordination after fix (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.1** Create .todo.ai/backups/ directory for storing versioned backups `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.2** Modify update_tool() to save backups with timestamp to .todo.ai/backups/ `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.3** Create list_backups() function to show available backup versions `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.4** Create rollback() function to restore from backup `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.5** Implement default rollback (restore latest backup) `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.6** Implement version-specific rollback (restore by timestamp or version) `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.7** Add 'rollback' command to main script command handler `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.8** Add 'backups' or 'list-backups' command to view available backups `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.9** Update help text and show_usage() to include new commands `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.10** Remove old .bak file creation logic `#cleanup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#30.11** Test backup and rollback functionality `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#30** Implement versioned backups and rollback capability `#feature` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-29** Test task 2 (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#28.1** Rename .todo.log to .todo.ai.log using git mv `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#28.2** Rename .todo_serial to .todo.ai_serial using git mv `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#28.3** Update LOG_FILE path reference in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#28.4** Update SERIAL_FILE path reference in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-28** Test coordination numbering (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-27** Test task after coordination setup (deleted 2025-11-02, expires 2025-12-02)
- [D] **#61** Test single-user mode `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.1** Rename directory using git mv: .todo/ -> .todo.ai/ `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.2** Update SERIAL_FILE path in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.3** Update LOG_FILE path in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.4** Update all references to .todo/ in script code `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.5** Update environment variable names (TODO_SERIAL, TODO_LOG) `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.6** Update README.md if it mentions .todo/ `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.7** Update any documentation files `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.8** Test script execution after rename `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.9** Verify git tracking of .todo.ai/ `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#26.10** Update .cursorrules to reference .todo.ai/ instead of .todo/ `#setup` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-26** to buy folwers (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.1** Rename repository on GitHub (manual step) `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.2** Update local git remote URL after GitHub rename `#repo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.3** Update REPO_URL in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.4** Update SCRIPT_URL in todo.ai script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.5** Update README.md repository references `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#25.6** Update header comment in todo.ai `#code` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-25** Mode check `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-24** Test mode display `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.1** Update script filename: todo.zsh -> todo.ai `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.2** Update all references in README.md (installation, examples, commands) `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.3** Update TODO.md template path references `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.4** Update self-references in update_tool() function `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.5** Update Cursor rules to reference todo.ai instead of todo.zsh `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.6** Update help text and show_usage() examples `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.7** Update init_cursor_rules() to reference todo.ai `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.8** Update all inline comments and documentation in script `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.9** Test installation and execution after rename `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#23.10** Test update command works with new filename `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-23** Another test `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-16** Test enhanced mode task creation `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#17.1** Enforce todo.ai usage for all task tracking `#rules` `#todo` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#17.3** Ensure TODO.md and .todo.ai/ are always committed together `#rules` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-17** Test fallback scenario 1: coordination.type=none `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#18.1** Remove path from todo.ai upon init `#fix` `#setup` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-18** Test fallback scenario 2: GitHub Issues unavailable (no issue_number) `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-19** Test fallback scenario 3: CounterAPI unavailable (no namespace) `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-20** Test fallback scenario 4: GitHub Issues API unavailable (gh CLI/auth issues) `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-21** Test fallback scenario 5: CounterAPI unavailable (invalid namespace) `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#22.1** Option 1: Simple re-download instruction in README `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#22.2** Option 2: Add version info + update command `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#22.3** Option 3: Auto-check version on startup (informational only) `#setup` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-22** Test tag formatting with backticks `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#main-3** Test branch mode task `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-9** Duplicate ID for conflict test `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-8** Test multi-user mode task `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#7.1** Add setup instructions documenting that .todo.ai/ must be tracked in git `#docs` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-7** Test multi-user mode task something else A `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-6** Test duplicate task #60 for conflict resolution `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#fxstein-5.1** Test subtask in multi-user mode `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-5** Test multi-user mode task something else B `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.4** TODO.md linting: implement validate_todo() using existing ./todo.ai --lint command, validates task IDs, subtask relationships, formatting, tags, and section structure `#lint` (deleted 2025-11-02, expires 2025-12-02) (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.1** Markdown linting: implement validate_markdown() using markdownlint-cli2 (recommended) or mdl (fallback), validate .md/.mdc files, create .markdownlint.yaml config `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.2** YAML linting: implement validate_yaml() using yamllint (recommended) or yq (fallback), validate .yml/.yaml files, create .yamllint config with relaxed rules for .mdc front matter `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.3** JSON linting: implement validate_json() using jq (recommended) or jsonlint/Python (fallback), validate .json files for syntax errors `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.5** Create pre-commit hook script at scripts/pre-commit-hook.sh with file type detection, error aggregation, and exit handling `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.6** Create setup script at scripts/setup-git-hooks.sh to install pre-commit hook and check for required linting tools `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.7** TODO.md linting: implement validate_todo() using existing ./todo.ai --lint command, validates task IDs, subtask relationships, formatting, tags, and section structure `#lint` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.8** Investigate installation options for linters (markdownlint-cli2, yamllint, jq): document direct installation methods and agent-assisted installation for developers after forking the repo, reference GIT_HOOKS_DESIGN.md `#docs` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#15.9** Create developer/ directory and setup script for automated linter installation, update design doc to reference the setup script `#code` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-15** Test duplicate #1 `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-14** Manual duplicate test task 2 `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-13** Manual duplicate test task 1 `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-12** Test duplicate #2 again `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-11** Test duplicate #2 `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-10** Test duplicate #1 again `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#60** Test single-user mode task somthing else D `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#104** Test single-user mode task `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#103** Test single-user mode task somthing else C `#deleteme` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#57.1** Test subtask `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#59** Test duplicate numbering bug `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#58** Test single-user mode task 2 `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#57** Test single-user mode task 1 `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#main-2** Test branch mode task 1 `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#main-1** Test branch mode task 2 `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-4** Test multi-user mode task 1 `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-3** Test multi-user task B `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-2** Test multi-user task A `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#fxstein-1** Test multi-user mode task 2 `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#51.1** Investigate get_script_path() function: how it detects script location when installed system-wide `#research` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#51.2** Fix get_script_path() to handle system-wide installations in /usr/local/bin or /usr/bin `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#51.3** Test update command from system-wide installation location `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#101** Add contributor section to release summary: list all contributors for each release `#feature` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#21** Ensure .todo.ai/ is tracked in git - not in gitignore or explicitly added `#setup` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#34.1** Level 1 subtask `#test` (deleted 2025-11-02, expires 2025-12-02)
    - [D] **#34.1.1** Level 2 sub-subtask `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#34** Final nested subtask test `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#33.1** Add subtask to main task `#test` (deleted 2025-11-02, expires 2025-12-02)
    - [D] **#33.1.1** Test sub-subtask creation `#test` (deleted 2025-11-02, expires 2025-12-02)
- [D] **#33** Test nested subtasks implementation `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#40.1** Subtask A (deleted 2025-11-01, expires 2025-12-01)
  - [D] **#40.2** Subtask B (deleted 2025-11-01, expires 2025-12-01)
- [D] **#40** Test parent task 2 (deleted 2025-11-01, expires 2025-12-01)
    - [D] **#41.1.1** Level 2 nested subtask (deleted 2025-11-01, expires 2025-12-01)
  - [D] **#41.1** Level 1 subtask (deleted 2025-11-01, expires 2025-12-01)
- [D] **#41** Test parent for nested subtasks (deleted 2025-11-01, expires 2025-12-01)
  - [D] **#39.2** Test subtask 2 (deleted 2025-11-01, expires 2025-12-01)
    - [D] **#39.1.1** Test nested subtask (deleted 2025-11-01, expires 2025-12-01)
  - [D] **#39.1** Test subtask 1 (deleted 2025-11-01, expires 2025-12-01)
- [D] **#39** Test parent task for deletion bug fix (deleted 2025-11-01, expires 2025-12-01)
- [D] **#9** Test new formatting fix `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#31** Test task after serial rename `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#29** Test task after file rename `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#27** Test task after .todo.ai rename `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#24** Test task after rename `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#4** Test task `#test` (deleted 2025-10-30, expires 2025-11-29)

---

**Last Updated:** Sun Nov 16 21:21:27 CET 2025
**Repository:** https://github.com/fxstein/todo.ai
**Maintenance:** Use `todo.ai` script only
