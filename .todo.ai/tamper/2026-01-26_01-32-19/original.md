# todo.ai ToDo List

> ⚠️ **MANAGED FILE**: Do not edit manually. Use `todo-ai` (CLI/MCP) or `todo.ai` to manage tasks.

## Tasks

- [x] **#213** Resolve whitespace conflict between todo.ai and pre-commit hooks `#bug` `#linter` `#maintenance` (2026-01-26)
  - [x] **#213.4** Verify fix by running pre-commit hooks on generated TODO.md `#verification` (2026-01-26)
  - [x] **#213.3** Configure pre-commit hooks to exclude .todo.ai/state/ directory `#config` (2026-01-26)
  - [ ] **#213.2** Implement whitespace stripping in todo.ai FileOps/Templates `#code`
  - [ ] **#213.1** Analyze todo.ai file writing logic to identify source of trailing whitespace `#analysis`

- [ ] **#205** Develop mechanism to prevent premature task archiving by agents `#design` `#safety`
  - [ ] **#205.5** Create design document for 'Safe Archival' workflow `#design` `#documentation`
  - [ ] **#205.4** Investigate MCP protocol capabilities for enforcing 'human-in-the-loop' confirmation for destructive/archival actions `#investigation` `#mcp`
  - [ ] **#205.3** Design a 'review required' state or flag for completed tasks before they can be archived `#design`
  - [ ] **#205.2** Research potential safeguards (e.g., time-based delays, explicit confirmation steps, 'cooldown' periods) `#research`
  - [ ] **#205.1** Analyze current agent behavior and triggers for premature archiving `#analysis`

- [ ] **#203** Redesign README.md for v3.0 (Python/MCP migration)  `#v3.0` `#documentation`
  - [ ] **#203.5** Review and refine additional documentation requirements `#documentation` `#review`
  - [ ] **#203.4** Document Next-Gen System Installation (uv/pipx/pip) and matching MCP config `#documentation` `#mcp` `#python`
  - [ ] **#203.3** Document Next-Gen Zero-Install MCP setup (uvx) `#documentation` `#mcp` `#uvx`
  - [ ] **#203.2** Document Legacy installation (Shell script) `#documentation` `#legacy`
  - [ ] **#203.1** Design new README structure (Overview, Legacy vs Next-Gen sections) `#design` `#documentation`

- [ ] **#191** Harden MCP server setup for portability and ease of installation `#design` `#infrastructure` `#mcp`
  > Current issue: .cursor/mcp.json contains absolute paths (/Users/oratzes/...) which breaks portability. Need a way to reference the project root dynamically or rely on CWD. Cursor's stdio transport might default to home dir, causing the issue we saw earlier. Need to find a way to make `todo-ai-mcp` aware of the project context without hardcoding absolute paths in the config file.
  - [ ] **#191.6** Create documentation for default installation and alternatives `#documentation` `#mcp`
  - [ ] **#191.5** Implement and test the portable setup solution `#implementation` `#mcp`
  - [ ] **#191.4** Design a clean installation process that sets up portable MCP config `#design` `#mcp`
  - [ ] **#191.3** Compare with MCP best practices for project-local configuration `#investigation` `#mcp`
  - [ ] **#191.2** Investigate options for dynamic workspace root detection in MCP server `#investigation` `#mcp`
  - [ ] **#191.1** Assess current situation: absolute paths in .cursor/mcp.json break portability `#mcp`

- [ ] **#190** Review MCP tool parameter naming consistency across all tools to ensure intuitive usage `#design` `#mcp`
  > Current inconsistency example: CLI uses `note`, MCP uses `note_text`. This causes friction for agents guessing parameters. Should we align them or document them better?

- [ ] **#187** Update cursor rules to prefer MCP server over CLI when available `#cursor-rules` `#feature`
  > Three versions exist: 1) todo.ai (shell script v2.x+ including v3.0), 2) todo-ai (Python CLI v3.0+), 3) todo-ai-mcp (MCP server v3.0+). Rules should prefer MCP > CLI > shell script.
  - [ ] **#187.10** Update rules to handle shell script (./todo.ai) as fallback for v2.x+ users (shell script continues in v3.0) `#cursor-rules`
  - [ ] **#187.9** Document version detection: MCP server (todo-ai-mcp) > Python CLI (todo-ai) > Shell script (./todo.ai) - all v3.0+ except shell script also supports v2.x `#documentation`
  - [ ] **#187.8** Test updated rules: verify AI agents prefer MCP when available, fallback to CLI when not `#test`
  - [ ] **#187.7** Update init_cursor_rules() function to include MCP preference in generated rules `#code`
  - [x] **#187.6** Add detection logic: prefer MCP (todo-ai-mcp) > Python CLI (todo-ai) > shell script (./todo.ai) as fallback   (2026-01-25) `#cursor-rules` `#documentation` (2026-01-26)
  - [x] **#187.5** Update .cursorrules file to mention MCP preference in Task Management section  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.4** Update todo.ai-task-notes.mdc to use MCP note tool instead of CLI command  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.3** Update bug-review-workflow.mdc to use MCP tools (add_task, add_subtask) instead of CLI commands  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.2** Update todo.ai-task-management.mdc: prefer MCP tools (todo-ai-mcp) > Python CLI (todo-ai) > shell script (./todo.ai)  (2026-01-25) `#cursor-rules` (2026-01-26)
  - [x] **#187.1** Review all cursor rules files to identify CLI command references  (2026-01-25) `#cursor-rules` (2026-01-26)

- [ ] **#172** Implement Beta/Pre-Release Strategy (2-Tier Approach) `#infrastructure` `#release`
  > Implements simplified 2-tier beta strategy (Beta→Stable). See docs/design/BETA_PRERELEASE_STRATEGY.md v2.0. Core infrastructure complete in Phases 1-3.
  - [ ] **#172.5** Phase 5: Stable Release `#release`
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

- [ ] **#163** Refactor todo.ai into Python-based MCP server with CLI interface (issue#39) `#feature`
  > Implementation audit completed. See docs/analysis/TASK_163_IMPLEMENTATION_AUDIT.md. Key findings: Only 4 of 30+ CLI commands implemented (~13%), only 3 of 30+ MCP tools implemented (~10%). Core infrastructure complete, but CLI/MCP interfaces severely incomplete. Overall ~40% complete, not ready for release.
  > Issue #39: Refactor into Python MCP server with dual interfaces (MCP + CLI). Core logic implemented once, exposed through both. Installable via pipx. Must maintain existing shell script functionality during development. Extensive testing required with dedicated test dataset.
  - [ ] **#163.52** Phase 16: Release Phase - Beta/pre-release and final release with migration support `#release`
  - [x] **#163.51** Phase 15: Cleanup - Remove unused methods, update documentation, add unit tests  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.50** Phase 14: Simplify Commands (Breaking) - Remove manual file editing and state restoration from commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.49** Phase 13: Remove Old State Variables (Breaking) - Remove mutable state variables and override logic  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.48** Phase 12: Use Snapshot for Generation (Non-Breaking) - Modify _generate_markdown() to use snapshot and implement mtime validation  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.47** Phase 11: Create Structure Snapshot (Non-Breaking) - Create FileStructureSnapshot dataclass and capture structure from pristine file  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.46** Phase 10: Enhanced Parsing (Pre-requisite) - Update FileOps._parse_markdown() to capture non-task lines in Tasks section  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.44** Phase 9: Testing and Validation - Re-test all commands and verify feature parity with shell script  (2026-01-25) `#test` (2026-01-26)
  - [x] **#163.43** Phase 8: MCP Server Completion - Add all missing MCP tools for implemented CLI commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.42** Phase 7: Utility Commands - Implement report-bug, uninstall, version commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.41** Phase 6: Configuration and Setup - Implement config, detect-coordination, setup-coordination, setup, switch-mode, list-mode-backups, rollback-mode commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.40** Phase 5: System Operations - Implement log, update, backups, rollback commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.39** Phase 4: File Operations - Implement lint, reformat, resolve-conflicts, edit commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.38** Phase 3: Task Display and Relationships - Implement show and relate commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.37** Phase 2: Note Management - Implement note, delete-note, update-note commands  (2026-01-25) `#code` (2026-01-26)
  - [x] **#163.36** Phase 1: Core Task Management Operations - Implement modify, delete, archive, restore, undo commands  (2026-01-25) `#code` (2026-01-26)
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

- [ ] **#129** Implement --prune function to remove old archived tasks based on git history `#feature`
  - [ ] **#129.3** Add prune command with --days and --from-task options `#feature`
  - [ ] **#129.2** Implement git history analysis to identify archive dates for tasks `#feature`
  - [ ] **#129.1** Design prune function with 30-day default and task ID targeting options `#feature`

- [ ] **#128** Create git commit hook for todo list linting and validation `#feature`

- [ ] **#127** Enhance --lint command with additional detection features `#feature`

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
  - [x] **#42.6** Test duplicate detection and 'me too' reply flow (2026-01-25) (2026-01-26)
  - [x] **#42.5** Test bug reporting with GitHub CLI integration (2026-01-25) (2026-01-26)
  - [x] **#42.4** Create bug report template with logs and data attachment (2026-01-25) (2026-01-26)
  - [x] **#42.3** Implement duplicate issue detection and 'me too' reply functionality (2026-01-25) (2026-01-26)
  - [x] **#42.2** Implement bug detection and reporting logic (2026-01-25) (2026-01-26)
  - [x] **#42.1** Create design document for bug reporting feature (2026-01-25) (2026-01-26)

- [ ] **#35** Build comprehensive test framework for todo.ai `#tests` `#todoai`
  - [x] **#35.3** Create tests directory and draft detailed test plan document   (2026-01-25) `#docs` `#tests` (2026-01-26)
  - [x] **#35.2** Define test framework architecture and tooling   (2026-01-25) `#planning` `#tests` (2026-01-26)
  - [x] **#35.1** Research todo.ai testing requirements and existing docs   (2026-01-25) `#docs` `#tests` (2026-01-26)

---

## Archived Tasks
  - [x] **#212.5** Verify new rules are concise and effective `#verify` (2026-01-26)
  - [x] **#212.4** Remove obsolete rules (e.g. zsh-first-development.mdc) `#cleanup` (2026-01-26)
  - [x] **#212.3** Update rules to mandate MCP tool usage `#mcp` (2026-01-26)
  - [x] **#212.2** Consolidate overlapping rules and simplify `#refactor` (2026-01-26)
  - [x] **#212.1** Audit existing rules for legacy shell/CLI references `#audit` (2026-01-26)
    > Create initial audit document for review
- [x] **#212** Clean up .cursor rules for MCP-first workflow `#maintenance` `#rules` (2026-01-26)
  > Requirement: Remove all references to shell tool (./todo.ai) and CLI (todo-ai) in the rules. Focus exclusively on MCP tools.
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
- [x] **#210** Implement TODO.md tamper detection and warnings `#feature` `#integrity` `#security` (2026-01-26)
  > Goal: Detect and warn when TODO.md has been manually edited outside of todo-ai commands.
  > Current issue: MANAGED FILE warning exists but no enforcement or detection mechanism.
  > Scope: Design and implement integrity checks, provide clear warnings to agents/users, suggest recovery actions.
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
- [x] **#211** Fix subtask ordering bug: IDs sorted alphabetically instead of numerically (125.10 before 125.2) `#bug` `#critical` `#sorting` (2026-01-25)
  > Bug: Subtasks sorted alphabetically instead of numerically. Example: #125 subtasks appear as 125.1, 125.10, 125.11, 125.12, 125.13, 125.2, 125.3, etc. Should be: 125.13, 125.12, 125.11, 125.10, 125.9, 125.8, etc. (newest first). Root cause: Task IDs treated as strings, not numbers. Need to split by dots, convert to ints, sort numerically.
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
- [x] **#209** Tell at least 3 funny jokes `#test` (2026-01-25)
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
- [x] **#207** Fix shell/Python parity issues discovered in validation tests `#bug` (2026-01-25)
  > Discovered while fixing task#206. After clearing TODO_FILE env var, validation tests revealed Python CLI isn't modifying TODO.md in test directories. Pattern: Tests create separate shell_env/python_env dirs, shell version works correctly, Python version appears to run but doesn't modify files. Likely issue: Python CLI not respecting cwd parameter or using different TODO.md path. Tests failing: test_complete_with_dataset, test_modify_with_dataset, test_delete_with_dataset, test_archive_with_dataset, test_undo_with_dataset, test_note_with_dataset, test_workflow_sequence_with_dataset, test_show_command_parity, test_basic_commands_exit_codes[show].
  > CONFIRMED: Python CLI ignores --root parameter. When --root /tmp/test is passed, CLI still modifies project TODO.md instead of /tmp/test/TODO.md. Shell script respects ROOT_DIR. Fix: Modify Python CLI main.py to resolve todo_file relative to root when root is provided. Line 48: ctx.obj['todo_file'] should become Path(root) / todo_file if root else todo_file.
  - [x] **#206.7** Document the fix and add test to prevent regression `#bug` (2026-01-25)
  - [x] **#206.6** Verify all 5 parity tests pass (dataset_parity + feature_parity) `#bug` (2026-01-25)
  - [x] **#206.5** Implement fix in shell script (todo.ai) `#bug` (2026-01-25)
  - [x] **#206.4** Design fix to suppress Cursor rules initialization during tests `#bug` (2026-01-25)
  - [x] **#206.3** Identify root cause (check if recent regression in shell script) `#bug` (2026-01-25)
  - [x] **#206.2** Investigate why Cursor rules initialization triggers during test runs `#bug` (2026-01-25)
  - [x] **#206.1** Reproduce shell script test failures locally `#bug` (2026-01-25)
- [x] **#206** Fix shell script test failures (Cursor rules initialization during tests) `#bug` (2026-01-25)
  > 5 parity tests failing: test_list_with_dataset, test_archive_with_dataset, test_note_with_dataset, test_show_command_parity, test_basic_commands_exit_codes[command3-args3]. Root cause: Shell script outputs '⚠️ IMPORTANT: Cursor rules initialized' during test runs, causing exit code 1 instead of 0. Python version correctly returns exit code 0.
  > Fix implemented: Added TODO_AI_TESTING environment variable check in todo.ai lines 1474-1476 (init_cursor_rules) and line 7134 (mode display). Test harnesses updated in test_dataset_parity.py lines 31-32 and test_feature_parity.py lines 40-41. When TODO_AI_TESTING=1, shell script suppresses all initialization output for clean test parity with Python version.
  - [x] **#204.6** Fix `restore_command` to preserve completion status of tasks (do not reset to PENDING) `#bug` `#fix` (2026-01-25)
  - [x] **#204.5** Fix `restore_command` to restore subtasks in correct reverse-chronological order `#bug` `#fix` (2026-01-25)
  - [x] **#204.4** Ensure `restore_command` is idempotent and restores missing subtasks even if parent is already active `#code` `#fix` (2026-01-25)
  - [x] **#204.3** Verify fix with regression test `#test` (2026-01-25)
  - [x] **#204.2** Fix `restore_command` to recursively restore subtasks `#code` `#fix` (2026-01-25)
  - [x] **#204.1** Create reproduction test case for restore subtask failure `#test` (2026-01-25)
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
  - [x] **#202.5** Update documentation to reflect Python 3.14 requirement and new dependency versions `#documentation` (2026-01-25)
  - [x] **#202.4** Run full test suite with Python 3.14 and updated dependencies `#test` (2026-01-25)
  - [x] **#202.3** Review and update all dependencies to latest stable versions in `pyproject.toml` `#dependencies` (2026-01-25)
  - [x] **#202.2** Update CI/CD workflows to use Python 3.14 as default (linting, building, etc.) `#cicd` (2026-01-25)
  - [x] **#202.1** Update `pyproject.toml` to require Python >= 3.14 and update classifiers `#configuration` (2026-01-25)
- [x] **#202** Upgrade project to Python 3.14 and update dependencies `#infrastructure` `#python` (2026-01-25)
  > Reopening to restore legacy Python support (3.10-3.13).
  > - Requirement: Keep 3.10+ support.
  > - Requirement: Use 3.14 for dev/linting/comprehensive CI.
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
- [x] **#200** Review and cleanup TODO.md file format and enhance formatting standards `#cleanup` `#formatting` `#linting` (2026-01-25)
  > Design doc: docs/design/TODO_MD_VISUAL_STANDARDS_2026_V3.md (approved)
  > Tests: tests/unit/test_visual_standards.py (23 tests, all passing)
  - [x] **#199.2** Add regression test case: archiving orphaned subtasks should group them under the already-archived parent `#test` (2026-01-25)
  - [x] **#199.1** Implement logic to move archived subtasks immediately after their parent in the task list `#code` (2026-01-25)
- [x] **#199** Enhance `archive_command` to enforce parent-child grouping in archive section `#archive` `#enhancement` (2026-01-25)
  > Scenario to test:
  > 1. Parent #1 is already archived (at bottom of file).
  > 2. Subtask #1.1 is active (at top of file).
  > 3. Run `archive 1.1`.
  > 4. Result: #1.1 should move to bottom of file, immediately after #1.
  > Current behavior would leave #1.1 at top (but in Archive section), appearing before #1.
  - [x] **#198.4** Update documentation to reflect new linting capabilities `#documentation` (2026-01-25)
  - [x] **#198.3** Add unit tests for subtask ordering detection and fixing `#test` (2026-01-25)
  - [x] **#198.2** Implement `reorder_command` as a separate fixer for subtask ordering (distinct from `reformat_command`) `#code` (2026-01-25)
  - [x] **#198.1** Update `lint_command` to detect subtasks that violate reverse-chronological order (newest on top) `#code` (2026-01-25)
- [x] **#198** Enhance linting to detect and fix out-of-order subtasks `#feature` `#linting` (2026-01-25)
  > Goal: Enforce the "newest on top" rule for subtasks, matching the behavior we recently fixed in task creation (#188).
  > Current fixers:
  > - `reformat_command`: Fixes indentation and checkboxes.
  > - `resolve_conflicts_command`: Fixes duplicate IDs.
  > We should likely add the reordering logic to `reformat_command` (optional or default?) or a new fixer. Given it changes content order, it should probably be part of `--reformat`.
  > Decision: Create a separate `reorder_command` (CLI: `reorder`) instead of overloading `reformat`.
  > Reasoning: Reordering changes content structure significantly, whereas reformat is cosmetic (indentation/checkboxes). Users should opt-in to reordering explicitly.
  - [x] **#197.2** Second subtask (should be at top) `#test` (2026-01-25)
  - [x] **#197.1** First subtask (should be at bottom) `#test` (2026-01-25)
- [x] **#197** Verify MCP server reload with ordering test `#mcp` `#test` (2026-01-25)
  - [x] **#196.5** Update documentation to reflect new quality gates `#documentation` (2026-01-25)
  - [x] **#196.4** Add regression test suite to CI (running `tests/integration/`) to catch logic bugs like #195 `#cicd` `#test` (2026-01-25)
  - [x] **#196.3** Investigate adding auto-fix (`--reformat`) to pre-commit (optional/manual trigger?) `#investigation` (2026-01-25)
    > Investigation results for #196.3:
    > - `todo-ai reformat` fixes indentation and checkboxes.
    > - It is suitable for a pre-commit hook.
    > - Recommendation: Add as `todo-ai-reformat` hook before linting.
  - [x] **#196.2** Add `todo-ai --lint` step to GitHub Actions CI workflow `#cicd` (2026-01-25)
  - [x] **#196.1** Add `todo-ai --lint` to pre-commit hooks to block commits with invalid TODO.md `#infrastructure` (2026-01-25)
- [x] **#196** Enhance Pre-commit and CI/CD with todo-ai linting and validation `#cicd` `#infrastructure` `#quality` (2026-01-25)
  > Goal: Ensure `TODO.md` integrity is enforced automatically.
  > - Pre-commit: Fast checks (linting, formatting).
  > - CI: Deep checks (regression tests, logic validation).
  > This prevents bugs like the "orphaned subtasks" from slipping through.
  - [x] **#195.3** Verify fix with regression test `#test` (2026-01-25)
  - [x] **#195.2** Fix archive_command to recursively archive subtasks `#code` `#fix` (2026-01-25)
  - [x] **#195.1** Create reproduction test case for archive subtask failure `#test` (2026-01-25)
- [x] **#195** Fix bug: Archiving a task does not archive its subtasks `#bug` `#critical` (2026-01-25)
  > Decision: Archiving a task should ALWAYS archive its subtasks. We will not add an extra --with-subtasks option; instead, we will change the default behavior of archive_command to include subtasks automatically. This aligns with user expectations that archiving a parent implies archiving its children.
  > Status: Fix implemented (default with_subtasks=True), but verification test failed due to unexpected ordering of archived tasks.
  > Issue: Archived subtask (1.1) appears BEFORE parent (1) in 'Recently Completed', while we expected parent first.
  > Action: Pausing work on #195 to fix the underlying ordering inconsistency in #188 first. We will return to verify #195 once ordering is deterministic and correct.
- [x] **#194** Hello World Test Task `#test` (2026-01-25)
  - [x] **#192.7** Release beta version with unified executable for testing `#release` (2026-01-25)
  - [x] **#192.6** Update documentation to reflect unified executable and `serve` command `#documentation` (2026-01-25)
  - [x] **#192.5** Add test cases for `serve` command and argument parsing `#test` (2026-01-25)
  - [x] **#192.4** Implement `--root` argument support for MCP server (via `serve` command) `#code` `#implementation` (2026-01-25)
  - [x] **#192.3** Implement `serve` command in CLI to launch MCP server `#code` `#implementation` (2026-01-25)
  - [x] **#192.2** Create design document for unified executable architecture `#design` `#documentation` (2026-01-25)
  - [x] **#192.1** Investigate default parameters for well-defined MCP server (e.g. logging, transport options) `#investigation` `#mcp` (2026-01-25)
- [x] **#192** Combine CLI and MCP server into single `todo-ai` executable with `serve` command and `--root` support `#design` `#mcp` `#refactor` (2026-01-25)
  - [x] **#188.2** Create reproduction test case for subtask ordering (newest should be on top) `#test` (2026-01-25)
  - [x] **#188.1** Fix task ordering inconsistency: Ensure subtasks follow the same reverse-chronological order (newest on top) as main tasks `#code` `#fix` (2026-01-25)
- [x] **#188** Investigate task ordering in Python version (todo-ai) - does not follow reverse order (newest on top) like shell script `#bug` `#python` (2026-01-25)
  > Shell script version (todo.ai) displays newest tasks first (reverse chronological). Python version (todo-ai) may not follow this same ordering. Need to investigate and ensure parity.
  - [x] **#161.5** Verify fix works with both local and system-wide installations `#bug` (2026-01-25)
    > VERIFIED: Tested fix from different working directory (/tmp). Script correctly uses ORIGINAL_WORKING_DIR (/tmp) instead of script directory. Fixed glob error by using find instead of glob expansion. Fix works for both local and system-wide installations - migrations always run in user's working directory where .todo.ai exists.
  - [x] **#161.4** Fix migration path detection for system-wide installations `#bug` (2026-01-25)
    > FIXED: Added ORIGINAL_WORKING_DIR variable captured at script startup. Updated run_migrations() to use ORIGINAL_WORKING_DIR instead of $(pwd) for migrations_dir. This ensures migrations always run in the user's working directory (where .todo.ai exists), not the script's directory (e.g., /usr/local/bin). Fixes issue where update command changes directory to script_dir before executing new version, causing run_migrations() to look in wrong location.
  - [x] **#161.3** Test migration execution when installed to /usr/local/bin or /usr/bin `#bug` (2026-01-25)
  - [x] **#161.2** Review get_script_path() and migration system for system directory handling `#bug` (2026-01-25)
  - [x] **#161.1** Investigate migration path error: reproduce with system directory installation `#bug` (2026-01-25)
    > BUG IDENTIFIED: In update_tool() at line 5805, script changes directory to script_dir (e.g., /usr/local/bin) before executing new version. When run_migrations() is called, it uses $(pwd) which is now /usr/local/bin, so it looks for .todo.ai/migrations in wrong location. The .todo.ai directory should always be in the user's working directory, not next to the script. Fix: Capture original working directory at script startup and use it in run_migrations().
- [x] **#161** Fix issue#26: Migration path error when todo.ai installed to system directory `#bug` (2026-01-25)
  > Issue #26: When todo.ai installed to /usr/local/bin and config at /homeassistant/.todo.ai, update to v2.0.1 shows error: 'run_migrations:21: no matches found: /usr/local/bin/.todo.ai/migrations/v*_*.migrated'. Migration logic looks for .todo.ai next to script instead of working directory. Issue: https://github.com/fxstein/todo.ai/issues/26
  - [x] **#126.4** Add tests to verify coordination setup doesn't change numbering mode `#bug` `#test` (2026-01-25)
  - [x] **#126.3** Fix setup-coordination to preserve current mode when configuring coordination (completed - fixed hardcoded enhanced mode) `#bug` (2026-01-25)
  - [x] **#126.2** Verify coordination should work with single-user mode without forcing enhanced (verified - validation supports single-user + coordination) `#bug` (2026-01-25)
  - [x] **#126.1** Investigate setup-coordination command mode switching logic (completed - found hardcoded mode: enhanced on line 3353) `#bug` (2026-01-25)
- [x] **#126** Fix issue#27: Setup coordinator automatically switches to enhanced mode without user consent (fixed - setup-coordination now preserves current mode) `#bug` (2026-01-25)
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
- [x] **#125** Overhaul bug reporting feature: eliminate prompts and improve formatting `#bug` `#feature` (2026-01-25)
  > Current implementation has basic markdown but needs improvement: (1) Create GitHub issue template (.github/ISSUE_TEMPLATE/bug_report.yml), (2) Use GitHub callout blocks (> [!NOTE], > [!WARNING]), (3) Better structure with proper sections, (4) Remove prompts for agent workflow, (5) Auto-collect all context without user input
- [x] **#189** Verify MCP server task creation with another test task `#mcp` `#test` (2026-01-24)
  > Why do programmers prefer dark mode? Because light attracts bugs. 🐛
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
- [x] **#186** Fix CI/CD release jobs skipping on tag pushes (validate-release and release) `#bug` (2026-01-24)
  > See docs/analysis/CI_CD_SILENT_FAILURE_ANALYSIS.md lines 73-227 for detailed analysis. Key files: .github/workflows/ci-cd.yml lines 384-488 (validate-release) and 489-549 (release).
- [x] **#185** Remove confirmation prompt when updating task notes `#feature` (2026-01-24)
- [x] **#184** Remove confirmation prompt when deleting task notes `#feature` (2026-01-24)
  - [x] **#183.5** Document CI/CD optimization and release impact `#docs` (2026-01-24)
    > Doc: release/RELEASE_PROCESS.md includes CI/CD triggers + optimization section.
  - [x] **#183.4** Add tests/verification for CI/CD changes `#infra` `#skipped` (2026-01-24)
  - [x] **#183.3** Implement optimized CI/CD workflow changes `#infra` (2026-01-24)
  - [x] **#183.2** Design CI/CD optimization plan (path filters, tiers) `#infra` (2026-01-24)
  - [x] **#183.1** Analyze current CI/CD triggers and test matrix `#infra` (2026-01-24)
- [x] **#183** Optimize CI/CD pipeline to avoid full suite on minor changes `#infra` (2026-01-24)
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
- [x] **#182** Design pinned project directory for todo.ai CLI (non-MCP) `#feature` (2026-01-23)
  > Overall summary: Design pinned project directory for todo.ai CLI (non-MCP).
  - [x] **#181.4** Add regression tests for release.sh prepare/execute workflow `#release` (2026-01-23)
  - [x] **#181.3** Harden execute flow (preflight, cleanup, retries) `#release` (2026-01-23)
  - [x] **#181.2** Fix release notes lifecycle so prepare/execute are clean `#release` (2026-01-23)
  - [x] **#181.1** Investigate current release blockers (preflight failures, notes handling) `#release` (2026-01-23)
- [x] **#181** Stabilize release process (no failures) `#release` (2026-01-23)
  > Investigation: execute preflight fails due to uncommitted files. In release.sh preflight check (around 'Check 3'), git status excludes only release/RELEASE_LOG.log and .todo.ai/.todo.ai.{serial,log}. It still flags release/RELEASE_NOTES.md and TODO.md, which are expected after prepare or task updates. Suggest extend exclusion list to include release/RELEASE_NOTES.md, release/.prepare_state, TODO.md and .todo.ai/.todo.ai.log so execute can proceed and then commit them in version commit (execute already stages TODO.md/.todo.ai and RELEASE_NOTES.md).
  > Focus on release.sh prepare/execute idempotency: keep RELEASE_NOTES.md for review without triggering auto-commit; ensure execute handles notes/log changes deterministically. Files: release/release.sh, release/RELEASE_NOTES.md, release/RELEASE_LOG.log.
  - [x] **#180.3** Implement change and update docs/tests `#bug` (2026-01-23)
  - [x] **#180.2** Decide whether to add --set-version or document alternative `#bug` (2026-01-23)
  - [x] **#180.1** Confirm supported release.sh options and expected override workflow `#bug` (2026-01-23)
    > release.sh does not support --help; running ./release/release.sh --help returns 'Unknown option' but prints usage. Usage currently lists --prepare/--execute/--abort, --beta, --summary, --set-version, --dry-run.
- [x] **#180** Investigate missing --set-version in release.sh `#bug` (2026-01-23)
  > Implemented --set-version override in release/release.sh (format X.Y.Z or X.Y.ZbN) with version comparison and beta-cycle base validation; documented override usage and constraints in release/RELEASE_PROCESS.md.
  > Attempted to run './release/release.sh --set-version 3.0.0b3' after prepare; script errored with 'Unknown option: --set-version'. Current usage only lists --prepare/--execute/--abort/--beta/--summary. Need a supported way to override version for beta releases.
  - [x] **#179.3** Implement fix and add regression test `#bug` (2026-01-23)
  - [x] **#179.2** Decide expected behavior for AI_RELEASE_SUMMARY.md vs RELEASE_SUMMARY.md `#bug` (2026-01-23)
  - [x] **#179.1** Reproduce stale summary detection in release.sh `#bug` (2026-01-23)
- [x] **#179** Investigate release prepare failure on stale RELEASE_SUMMARY.md `#bug` (2026-01-23)
  > Prepare failed with stale summary warning: release.sh auto-detected release/RELEASE_SUMMARY.md (timestamp 2025-12-18) and aborted in non-interactive mode despite new release/AI_RELEASE_SUMMARY.md. Error surfaced on 'release.sh --prepare' after summary commit d5208d4.
  - [x] **#178.3** Add tests for multiple parents/subtasks `#bug` (2026-01-17)
  - [x] **#178.2** Fix subtask insertion to correct parent `#bug` (2026-01-17)
  - [x] **#178.1** Investigate subtask placement logic `#bug` (2026-01-17)
- [x] **#178** Fix issue#40: Subtasks assigned to wrong parent `#bug` (2026-01-17)
  > Investigate/fix in `todo_ai/cli/commands/__init__.py` add_subtask_command; tests in `tests/integration/test_cli.py` (add_subtasks_multiple_parents).
  - [x] **#177.3** Move GitHub release to workflow (after PyPI success) `#infrastructure` (2026-01-17)
  - [x] **#177.2** Remove GitHub release creation from release.sh `#infrastructure` (2026-01-17)
  - [x] **#177.1** Update PyPI Trusted Publisher config to ci-cd.yml/release `#infrastructure` (2026-01-17)
- [x] **#177** Fix release process - PyPI must succeed before GitHub release `#critical` `#infrastructure` (2026-01-17)
- [x] **#176** Fix CI/CD dependency flaw - merge workflows with job dependencies `#critical` `#infrastructure` (2026-01-17)
  - [x] **#175.3** Add CI/CD check to detect forbidden flags `#infrastructure` (2026-01-17)
  - [x] **#175.2** Add pytest test to detect forbidden flags `#infrastructure` (2026-01-17)
  - [x] **#175.1** Add pre-commit hook to detect forbidden flags `#infrastructure` (2026-01-17)
- [x] **#175** Implement safeguards to prevent --no-verify from returning to codebase `#critical` `#infrastructure` (2026-01-17)
  - [x] **#174.7** Test first beta release with trusted publisher `#testing` (2026-01-17)
  - [x] **#174.6** Update GitHub Actions workflow to use OIDC authentication `#infrastructure` (2026-01-17)
  - [x] **#174.5** Register GitHub as trusted publisher on PyPI `#setup` (2026-01-17)
  - [x] **#174.1** Create PyPI project 'todo-ai' (or verify name available) `#setup` (2026-01-17)
- [x] **#174** Set up PyPI project for todo-ai package `#release` (2026-01-17)
  > Changed PyPI package name from 'todo-ai' to 'ai-todo' (PyPI rejected original name as too similar to existing project). Updated pyproject.toml, README.md, and all documentation.
  > Using PyPI Trusted Publisher (OpenID Connect) - no API token needed. Requires: 1) Create PyPI project, 2) Add GitHub as trusted publisher, 3) Update GitHub Actions workflow to use OIDC.
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
- [x] **#173** Fix release script bugs found during v3.0.0b1 attempt `#bug` (2026-01-17)
- [x] **#171** Improve CI/CD job grouping and naming `#cicd` `#enhancement` (2025-12-16)
  > Added 'needs: quality' dependency to all test jobs - tests won't run until code quality checks pass. Saves CI resources by failing fast on linting/typing/formatting issues.
  > Refactored to 3 separate jobs: 'Comprehensive Tests' (Py 3.14 × 3 OS, main only), 'Quick Tests' (Py 3.10-3.13 × 3 OS, main only), 'PR Tests' (Py 3.12 × ubuntu, PRs only). Creates clean grouping in GitHub Actions UI.
  > Added conditional job naming: '🔬 Comprehensive Tests' for Python 3.14 (full suite), '⚡ Quick Tests' for Python 3.10-3.13 (unit only). Makes GitHub Actions UI more readable and groups related tests.
- [x] **#170** Further optimize CI/CD: Granular test strategy `#cicd` `#optimization` (2025-12-16)
  > Main branch: Full tests only on Python 3.14 (3 OS × 1 version = 3 jobs), unit tests on 3.10-3.13 (3 OS × 4 versions = 12 jobs). PRs: Full tests on ubuntu + 3.12 (1 job). Total main: 15 jobs but most are fast unit-only.
  - [x] **#169.3** Phase 3: Cleanup and documentation `#cicd` (2025-12-16)
  - [x] **#169.2** Phase 2: Optimize pre-commit configuration `#cicd` (2025-12-16)
  - [x] **#169.1** Phase 1: Refactor CI/CD workflow `#cicd` (2025-12-16)
- [x] **#169** Implement CI/CD optimizations from assessment `#cicd` `#optimization` (2025-12-16)
  - [x] **#167.9** Phase 3.3: Add documentation automation `#cicd` (2025-12-14)
  - [x] **#167.8** Phase 3.2: Expand test matrix to multiple OS (macOS, Windows) `#cicd` (2025-12-14)
  - [x] **#167.7** Phase 3.1: Add code coverage reporting (codecov) `#cicd` (2025-12-14)
  - [x] **#167.6** Phase 2.3: Integrate automated release process with release.sh `#cicd` (2025-12-14)
    > Integration complete: release.sh creates GitHub release with shell assets and release notes. GitHub Actions workflow (triggered by tag push) builds Python package, publishes to PyPI, and attaches dist files to existing release. Clean separation of concerns achieved.
    > Release workflow (.github/workflows/release.yml) created but needs integration with existing release/release.sh process. Consider: (1) Have release.sh trigger workflow, (2) Replace release.sh with workflow, or (3) Keep both with different purposes.
  - [x] **#167.5** Phase 2.2: Configure code quality tools `#cicd` (2025-12-14)
    > Configured [tool.ruff] section with target-version py310, select rules (E, W, F, I, B, C4, UP), and per-file ignores for tests. Configured [tool.mypy] section with python_version 3.10 and strict type checking options.
  - [x] **#167.4** Phase 2.1: Add development dependencies `#cicd` (2025-12-14)
    > Added [project.optional-dependencies] dev section to pyproject.toml with: pytest, pytest-cov, ruff, mypy, pre-commit, build, twine, types-requests, types-pyyaml.
  - [x] **#167.3** Phase 1.3: Create GitHub Actions CI/CD `#cicd` (2025-12-14)
    > Created .github/workflows/ci.yml with test matrix for Python 3.10-3.12, linting, type checking, and pre-commit checks. Created .github/workflows/release.yml for automated PyPI publishing on version tags.
  - [x] **#167.2** Phase 1.2: Migrate to pre-commit framework `#cicd` (2025-12-14)
    > Created .pre-commit-config.yaml with ruff, mypy, and standard pre-commit hooks. Updated scripts/setup-git-hooks.sh to use 'uv run pre-commit install' instead of custom shell script hooks.
  - [x] **#167.1** Phase 1.1: Add uv dependency management `#cicd` (2025-12-14)
    > Created uv.lock file via 'uv lock'. Updated pyproject.toml with dev dependencies section. Created setup.sh script with PATH handling for $HOME/.local/bin (default uv installation path). Created docs/development/SETUP.md with setup instructions.
- [x] **#167** Implement CI/CD process parity with ascii-guard (Phase 1-3) `#cicd` (2025-12-14)
  > Reference: docs/analysis/CI_CD_PROCESS_PARITY_ASSESSMENT.md. Implementation roadmap for achieving process parity with ascii-guard's modern Python development workflow (uv, pre-commit, GitHub Actions CI/CD).
  - [x] **#160.5** Add tests to prevent regression `#bug` (2025-12-12)
  - [x] **#160.4** Fix task ID resolution in modify command if bug confirmed `#bug` (2025-12-12)
    > FIXED ALL FUNCTIONS: Updated modify_todo(), add_note(), complete_todo(), archive_task(), show_task(), add_relationship(), update_note(), and delete_note() to handle both bold and non-bold task ID formats. All functions now search for (\*\*#task_id\*\*|#task_id) pattern. Tested: modify and note commands work correctly with non-bold tasks.
    > FIXED: Updated modify_todo() sed patterns to match both bold (\*\*#task_id\*\*) and non-bold (#task_id) formats using extended regex. Also updated add_note() grep pattern to search for both formats. Updated sed_inplace() to support -E flag for extended regex. This ensures modify command can replace tasks regardless of formatting, and note command can find them afterward.
  - [x] **#160.3** Test modify command with various task IDs and nesting levels `#bug` (2025-12-12)
  - [x] **#160.2** Review modify_task() function for task ID resolution issues `#bug` (2025-12-12)
  - [x] **#160.1** Investigate modify command: reproduce the bug and identify root cause `#bug` (2025-12-12)
    > BUG IDENTIFIED: modify_todo() finds tasks with pattern matching both bold and non-bold (line 2596), but sed replacement only matches bold format (lines 2669-2682). If task exists without bold (#2.6), modify finds it but sed replacement fails silently, leaving task unchanged. Then add_note() only searches bold format (line 4417), so it can't find the task. Fix: Make sed patterns match both bold and non-bold like grep does.
- [x] **#160** Fix issue#35: Task not found after successful modify command `#bug` (2025-12-12)
  > All functions fixed to handle both bold and non-bold task ID formats. Tested: modify and note commands work. Complete command may need additional testing with tags.
  > Issue #35: User ran './todo.ai modify 2.6' which succeeded, then immediately ran './todo.ai note 2.6' but got 'Task #2.6 not found'. The modify command reported success but task became unfindable. Version 2.4.0, macOS. Issue: https://github.com/fxstein/todo.ai/issues/35
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
- [x] **#157** Fix issue#38: Single-user mode assigns duplicate task IDs `#bug` (2025-11-16)
  > Critical data integrity bug in v2.4.0 and v2.5.0. Duplicate ID #21 assigned in single-user mode. Error context suggests relation to recent bash compatibility fixes (match array conversion). Issue reported at https://github.com/fxstein/todo.ai/issues/38
- [x] **#155** Fix get_config_value sed fallback to work in bash (uses zsh-specific $match array) `#bug` (2025-11-16)
  > Fixed 3 critical $match[ ] usages in get_config_value() and get_highest_task_number(). Found 60 total occurrences throughout codebase. Need systematic conversion: all regex match references must check BASH_VERSION and use BASH_REMATCH[ ] for bash or $match[ ] for zsh.
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
    > delete_note_internal $task_id  # No prompt version
    > add_note $task_id $new_text
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
    > - [ ] **#42.1** Task description
    > > Note line 1
    > > Note line 2
    > > Note line 3
    > 
    > Need to identify all note lines for delete/update operations.
  - [x] **#153.1** Design command syntax for update-note and delete-note `#feature` (2025-11-16)
    > Proposed command syntax:
    > 
    > ./todo.ai delete-note <task-id>
    > - Removes ALL notes from specified task
    > - Confirmation prompt: 'Delete all notes from task #X? (y/N)'
    > - Returns error if task has no notes
    > 
    > ./todo.ai update-note <task-id> "new note text"
    > - Replaces ALL existing notes with new text
    > - Supports multi-line notes (like add note)
    > - Shows preview: 'Replace N lines with M lines?'
    > - Returns error if task has no notes to update
    > 
    > Alternative: Could add --force to skip confirmations for both commands.
- [x] **#153** Add note management: update and delete note commands `#feature` (2025-11-16)
  > Currently can only ADD notes with './todo.ai note <id> "text"'. Need to add:
  > - delete-note: Remove all notes from a task
  > - update-note: Replace existing notes with new text
  > 
  > This allows fixing mistakes, removing outdated info, and updating context without manual TODO.md editing.
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
- [x] **#152** Test bug reporting feature before v2.5.0 release `#testing` (2025-11-16)
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
    > > First line of note
    > Line 2 without marker
    > Line 3 without marker
    > 
    > EXPECTED (correct):
    > > First line of note
    > > Line 2 with marker
    > > Line 3 with marker
    > 
    > All note lines must have proper indentation (matching task depth) AND blockquote marker (>).
- [x] **#149** Fix multi-line note indentation bug in add_note() function `#bug` (2025-11-16)
  > When adding multi-line notes, only the first line gets the blockquote marker (>) and proper indentation. Subsequent lines are inserted as raw text without indentation or markers, breaking TODO.md structure. Affects tasks 147.3 (lines 36-45), 147.4 (lines 27-32), 147.5 (lines 21-23), 147.6 (lines 14-18). Example: First line is '  > Text' but second line is just 'More text' instead of '  > More text'.
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
- [x] **#147** Fix issue#36: Task show command fails for deeply nested subtasks `#bug` (2025-11-16)
  > Issue #36 reports that 'show 1.2.1' fails with 'Task not found' even though task exists. Commands work for 1-level (#1) and 2-level (#1.2) but fail at 3-level (#1.2.1). This affects show, modify, note commands. Need to find task ID parsing/resolution logic and fix for arbitrary nesting depth. All 7 subtasks under #1.2 (tasks #1.2.1 through #1.2.7) affected.
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
- [x] **#146** Test task#144 implementation before release `#test` (2025-11-12)
  > Validate all task#144 features before creating release: bash conversion, smart installer, release assets. All tests passed successfully. Release v2.4.0 is LIVE with smart installer, bash version, and automated conversion workflow.
  - [x] **#144.9** Update release script to include both todo.ai and todo.bash as assets `#release` (2025-11-12)
  - [x] **#144.8** Add cursor rule to prevent accidental todo.bash editing `#docs` (2025-11-12)
  - [x] **#144.7** Update GETTING_STARTED.md and other documentation references `#docs` (2025-11-12)
  - [x] **#144.6** Update README.md with smart installer as primary method `#docs` (2025-11-12)
  - [x] **#144.5** Create concise smart installer documentation `#docs` (2025-11-12)
  - [x] **#144.4** Test smart installer on multiple platforms and scenarios `#test` (2025-11-12)
  - [x] **#144.3** Create release-aware smart installer script (install.sh) `#installer` (2025-11-12)
  - [x] **#144.2** Add automated bash conversion to release script `#release` (2025-11-12)
  - [x] **#144.1** Create development guidelines document for zsh-first workflow `#docs` (2025-11-12)
- [x] **#144** Implement release-aware smart installer with bash/zsh dual-version support `#feature` (2025-11-12)
  > Smart installer that detects OS/shell and installs optimal version (zsh/bash). Installs from releases (not main branch) to avoid incomplete/broken commits. Clear dev workflow: develop in zsh, auto-convert to bash during release. Released in v2.4.0.
  - [x] **#132.3** Explore bash version of todo.ai: evaluate impact on file size and platform compatibility `#research` (2025-11-12)
    > Smart installer created: install.sh detects OS/shell and installs optimal version. See docs/design/SMART_INSTALLER_DESIGN.md for full design. One-liner: curl -fsSL .../install.sh | sh maintains simplicity while adding intelligence.
    > Compare bash vs zsh syntax differences, evaluate portability benefits (works on more platforms), analyze if simpler syntax reduces file size. Current tool is zsh-specific with features like [[ ]], read patterns, arrays.
  - [x] **#132.2** Remove old migration logic: keep migration shell but eliminate version-specific migration code `#refactor` (2025-11-12)
    > Keep MIGRATIONS array and run_migrations() infrastructure, but remove all version-specific migration functions (v1_3_5, v2_0_0_cursor_rules, v2_1_0_git_coordination). Add comments pointing to git history for old migrations if needed for legacy installs. See docs/analysis/CODE_SIZE_ANALYSIS.md lines 66-67 for details.
  - [x] **#132.1** Create code size analysis document documenting current state and optimization opportunities `#docs` (2025-11-12)
    > Analysis document created at docs/analysis/CODE_SIZE_ANALYSIS.md - documents current 5952 lines with breakdown by functionality and identifies optimization opportunities
- [x] **#132** Optimize todo.ai codebase: reduce size and complexity `#optimization` (2025-11-12)
  > Current codebase is 5952 lines. Goal: reduce size and complexity by removing obsolete code, cleaning up old migrations, and improving maintainability. See docs/analysis/CODE_SIZE_ANALYSIS.md for detailed breakdown and recommendations.
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
- [x] **#145** Reorganize docs folder with logical subdirectory structure `#docs` (2025-11-11)
  > Proposed structure: guides/ (user docs), design/ (technical specs), development/ (contributor docs), analysis/ (research), archive/ (historical). Currently 29 files in flat structure need categorization and organization. Must update all cross-references, docs/README.md, and main README.md links.
  - [x] **#143.5** Test: Verify detection works with old and new summary files `#bug` (2025-11-11)
  - [x] **#143.4** Option: Prompt to continue or abort if stale summary detected `#bug` (2025-11-11)
  - [x] **#143.3** Add warning if summary appears stale (older than last release) `#bug` (2025-11-11)
  - [x] **#143.2** Add validation: Compare summary file mtime with last release tag date `#bug` (2025-11-11)
  - [x] **#143.1** Investigate: How to detect if summary file is stale `#bug` (2025-11-11)
- [x] **#143** Prevent stale release summaries from being used in releases `#bug` (2025-11-11)
  > Tested with old file (2024-11-11) vs v2.3.0 (2025-11-11): correctly detected and aborted. Fresh file passes validation.
  > Bug caused v2.3.0 to be released with v2.2.1's summary. Script used stale release/RELEASE_SUMMARY.md without validation. Fix: Check if summary file mtime > last release tag date.
  - [x] **#142.4** Test: Verify execute works after failed/aborted release attempt `#test` (2025-11-11)
  - [x] **#142.3** Fix: Get correct commit hash when 'no commit needed' returned `#code` (2025-11-11)
  - [x] **#142.2** Fix: Handle case where version already correct in working directory `#code` (2025-11-11)
  - [x] **#142.1** Investigate execute_release: why version verification fails `#bug` (2025-11-11)
- [x] **#142** Fix release script bug: version verification fails when version already updated in working directory `#bug` (2025-11-11)
  > Execute mode assumes version needs updating, but if version already changed in working dir (from failed attempt), commit has no changes and version_commit_hash points to old commit. Need to handle case where version already correct.
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
- [x] **#141** Redesign release workflow: separate prepare (default) and execute steps, eliminate prompts `#feature` (2025-11-11)
  > New workflow: release.sh defaults to --prepare (analyze, preview, show execution command). Then run release.sh --execute to perform release. No prompts in either mode.
- [x] **#140** Fix bug: Note command doesn't work for nested sub-subtasks (4-space indentation) `#bug` (2025-11-11)
  > add_note() line 4303 only searches for 0-space and 2-space patterns, missing 4-space sub-subtask pattern. Need to add: |^    - \[.\] \*\*#\*\*
  - [x] **#139.7** Test: verify nested subtask notes displayed correctly `#test` (2025-11-11)
  - [x] **#139.6** Test: verify subtask notes displayed for all subtasks `#test` (2025-11-11)
    > This note should appear in show output after implementing the fix - verifies subtask notes are displayed.
  - [x] **#139.5** Test: verify parent task note displayed `#test` (2025-11-11)
  - [x] **#139.4** Implement fix: modify show_task to display notes after each task/subtask line `#code` (2025-11-11)
    > Modify show_task() to call collect_task_notes() for each displayed task/subtask. Display notes immediately after each task line.
  - [x] **#139.3** Design solution: show notes for parent task and all displayed subtasks `#design` (2025-11-11)
  - [x] **#139.2** Verify current behavior: confirm only parent notes shown, subtask notes missing `#bug` (2025-11-11)
  - [x] **#139.1** Investigate show_task function: find where notes are displayed `#research` (2025-11-11)
    > Find show_task() function in todo.ai script. Look for note display logic around lines 4000-4100.
- [x] **#139** Enhance show command to display notes for subtasks, not just parent task `#feature` (2025-11-11)
  > Investigate show_task() function. Currently only displays notes for parent task. Need to display notes for all subtasks shown in output.
- [x] **#136** Fix bug: Adding subtask splits task notes - subtask inserts between task and note `#bug` (2025-11-09)
  > Investigate add_subtask() function. Fix to insert subtasks after parent task notes, not between task and notes.
  - [x] **#135.1** Level 1 subtask `#test` (2025-11-09)
- [x] **#135** Test nested subtasks with notes `#test` (2025-11-09)
  - [x] **#134.2** Subtask two with note `#test` (2025-11-09)
    > Subtask two note - should move with subtask
  - [x] **#134.1** Subtask one with note `#test` (2025-11-09)
    > Subtask one note - should move with subtask
    > Parent task note - should move with parent
- [x] **#134** Test parent task with subtasks and notes `#test` (2025-11-09)
- [x] **#133** Test task with note for archive bug fix `#test` (2025-11-09)
  > This is a test note that should move with the task when archived
  - [x] **#131.5** Test rule installation and verify agents follow note-adding guidelines `#test` (2025-11-09)
  - [x] **#131.4** Add rule to init_cursor_rules() function in todo.ai script `#code` (2025-11-09)
  - [x] **#131.3** Create .cursor/rules/todo.ai-task-notes.mdc with concise guidelines and examples `#code` (2025-11-09)
  - [x] **#131.2** Draft Cursor rule: define when agents should add notes to tasks (implementation details, context, decisions) `#docs` (2025-11-09)
  - [x] **#131.1** Research current note usage patterns: when and how notes are used in TODO.md `#research` (2025-11-09)
- [x] **#131** Create Cursor rule encouraging agents to use notes for task implementation details `#feature` (2025-11-09)
  > Rule should encourage agents to add notes for: implementation approach, technical decisions, context about why certain choices were made, file locations to modify, dependencies between tasks. Keep rule short (~15-20 lines) following cursor-rules-guidelines.mdc principles.
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
- [x] **#130** Fix issue#32: Archive command doesn't move task notes with the task `#bug` (2025-11-09)
- [x] **#56** Fix release script: exclude .todo.ai/.todo.ai.serial from uncommitted changes check `#bug` (2025-11-02)
  - [x] **#55.4** Close GitHub issue #17 when fix has been confirmed `close-issue` (2025-11-02)
  - [x] **#55.3** Test update command from system-wide installation location `#test` (2025-11-02)
  - [x] **#55.2** Fix get_script_path() to handle system-wide installations in /usr/local/bin or /usr/bin `#code` (2025-11-02)
  - [x] **#55.1** Investigate get_script_path() function: how it detects script location when installed system-wide `#research` (2025-11-02)
- [x] **#55** Fix update command when installed to system directory in PATH (GitHub issue #17) `#bug` (2025-11-02)
  - [x] **#53.1** Test bug reporting from a different repository to verify it reports to todo.ai repo (2025-11-02)
- [x] **#53** Fix bug reporting: reports to wrong repository (customer repo instead of todo.ai repo) `#bug` (2025-11-02)
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
- [x] **#52** Design multi-user/multi-branch/PR support system for todo.ai with conflict-free task numbering `#MAJOR` `#feature` (2025-11-02)
  - [x] **#50.4** Check existing commits for wrong format (#nn instead of task#nn) and create migration plan to fix or document them `#code` (2025-11-02)
  - [x] **#50.3** Propose solution: design numbering schema or commit message format to avoid conflicts `#docs` (2025-11-02)
  - [x] **#50.2** Research alternative numbering schemas: prefixes, formats, or conventions to distinguish task numbers from GitHub issues/PRs `#research` (2025-11-02)
  - [x] **#50.1** Create analysis document: investigate how GitHub treats task numbers in commit messages and potential conflicts with issue/PR numbers `#docs` (2025-11-02)
- [x] **#50** Investigate task numbering schema to avoid GitHub issue/PR number conflicts in commit messages `#research` (2025-11-02)
  - [x] **#48.4** Test update workflow: verify migrations execute in new version after update `#test` (2025-11-02)
  - [x] **#48.3** Implement update fix: execute new version's migrations and update logic before replacement `#code` (2025-11-02)
  - [x] **#48.2** Design solution: download → execute new version → replace old version `#docs` (2025-11-02)
  - [x] **#48.1** Research update execution pattern: how to execute new version's code after download `#research` (2025-11-02)
- [x] **#48** Fix update logic error: new version update logic never executes (2025-11-02)
  - [x] **#46.6** Create mapping document: tags to release types with priority matrix showing numbering decisions `#docs` (2025-11-02)
  - [x] **#46.5** Test fix: verify cursor rules migration would be classified as MINOR with fix applied `#test` (2025-11-02)
  - [x] **#46.4** Handle ambiguous cases: migrations that affect users vs pure infrastructure changes `#code` (2025-11-02)
  - [x] **#46.3** Implement fix: check for functional changes in todo.ai before file-based classification `#code` (2025-11-02)
  - [x] **#46.2** Design fix: prioritize commit message prefixes (feat:) over file analysis for user-facing features `#docs` (2025-11-02)
  - [x] **#46.1** Investigate release numbering logic: why feat: commits with .cursor/rules/ changes are classified as PATCH `#research` (2025-11-02)
- [x] **#46** Fix release numbering bug: cursor rules migration incorrectly classified as PATCH instead of MINOR `#bug` (2025-11-02)
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
- [x] **#44** Migrate cursor rules from .cursorrules to .cursor/rules/ directory structure `#migration` (2025-11-02)
  - [x] **#43.4** Create dedicated cursor rule for uninstall process: require agents to use ./todo.ai uninstall command and NOT delete files directly to control uninstall scope `#code` (2025-11-02)
  - [x] **#43.3** Enhance README.md to show simple uninstall command (2025-11-02)
  - [x] **#43.2** Implement and test uninstall feature (2025-11-02)
  - [x] **#43.1** Write design document for uninstall feature (2025-11-02)
- [x] **#43** Create uninstall feature (2025-11-02)
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
- [x] **#37** Build release migration and cleanup system for one-time migrations and cleanups `#feature` (2025-11-02)
- [x] **#19** Move Deleted Tasks section below Recently Completed section `#setup` (2025-11-02)
- [x] **#15** Setup git hooks with pre-commit validation for Markdown, YAML, JSON, and TODO.md linting `#git` `#setup` (2025-11-02)
  - [x] **#38.6** Verify orphaned subtask detection still works correctly (2025-11-01)
  - [x] **#38.5** Test deletion of subtask only (should not delete parent or siblings) (2025-11-01)
  - [x] **#38.4** Test deletion of parent task with nested subtasks (2-level) (2025-11-01)
  - [x] **#38.3** Test deletion of parent task with subtasks (verify subtasks deleted) (2025-11-01)
  - [x] **#38.2** Implement automatic subtask deletion when deleting parent task (2025-11-01)
  - [x] **#38.1** Analyze current delete_task function behavior (2025-11-01)
- [x] **#38** Fix orphaned subtasks bug: delete subtasks when deleting parent task `#bug` (2025-11-01)
  - [x] **#36.5** Review and finetune release numbering logic (2025-11-01)
  - [x] **#36.4** Create permanent release log file with detailed timestamps (2025-11-01)
  - [x] **#36.3** Create release management process (2025-11-01)
  - [x] **#36.2** Review release process document (2025-11-01)
  - [x] **#36.1** Create release process document (2025-11-01)
- [x] **#36** Create release process for todo.ai on GitHub (2025-11-01)
- [x] **#14** Formatting fixes complete `#setup` (2025-11-01)
- [x] **#7** Remove gitignore entry for .todo.ai directory - .todo.ai/ must be tracked in git `#git` `#setup` (2025-11-01)
- [x] **#5** Initialize repository structure and configuration `#repo` `#setup` (2025-11-01)
- [x] **#32** Implement nested subtasks support (2-level limit) `#feature` (2025-10-30)
- [x] **#28** Rename files in .todo.ai/ to .todo.ai.log and .todo.ai_serial `#setup` (2025-10-30)
- [x] **#26** Rename .todo/ directory to .todo.ai/ `#setup` (2025-10-30)
- [x] **#25** Rename repository from todo to todo.ai `#setup` (2025-10-30)
- [x] **#23** Rename todo.ai to todo.ai `#setup` (2025-10-30)
- [x] **#22** Create update instructions and functions for todo.ai `#setup` (2025-10-30)
- [x] **#20** Create radically simplified README.md `#docs` (2025-10-30)
- [x] **#18** Fix TODO.md header upon initialization - use repo name dynamically `#fix` `#setup` (2025-10-30)
- [x] **#17** Create Cursor rules for repository `#docs` `#setup` (2025-10-30)
- [x] **#13** All formatting fixes complete `#setup` (2025-10-30)
- [x] **#12** Final formatting test `#test` (2025-10-30)
- [x] **#11** Test new append method `#test` (2025-10-30)
- [x] **#10** Verify formatting works correctly `#test` (2025-10-30)
- [x] **#8** Fix all sed -i calls to use sed_inplace for macOS compatibility `#fix` `#setup` (2025-10-30)
- [x] **#6** Update TODO.md template for this repository `#docs` `#setup` (2025-10-30)

---

## Deleted Tasks
- [D] **#214** Test task for whitespace verification `#test` (deleted 2026-01-26, expires 2026-02-25)
- [D] **#208** Test task from root (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.7** Update documentation with 'start' command usage `#documentation` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.6** Add unit and integration tests for 'start' command `#test` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.5** Implement 'start_task' tool in MCP server `#code` `#mcp` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.4** Implement 'start' command in CLI `#code` `#implementation` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.3** Create design document for 'start' command architecture `#design` `#documentation` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.2** Design the 'start' functionality: status changes, timers, assignments, etc. `#design` (deleted 2026-01-25, expires 2026-02-24)
  - [D] **#193.1** Research existing 'start' command patterns in other todo apps and define requirements `#research` (deleted 2026-01-25, expires 2026-02-24)
- [D] **#193** Implement 'start task' command to track task progress and status `#design` `#feature` (deleted 2026-01-25, expires 2026-02-24)
  > Key questions to answer:
  > 1. Does 'starting' a task imply a status change (e.g. to 'in-progress')?
  > 2. Should we support time tracking (start/stop)?
  > 3. How does this interact with todo.txt format (e.g. priority changes)?
  > 4. Should this trigger any external integrations?
  - [D] **#174.4** Test PyPI authentication with manual upload `#testing` (deleted 2025-12-16, expires 2026-01-15)
  - [D] **#174.3** Add PYPI_API_TOKEN to GitHub secrets `#setup` (deleted 2025-12-16, expires 2026-01-15)
  - [D] **#174.2** Generate PyPI API token with upload permissions `#setup` (deleted 2025-12-16, expires 2026-01-15)
- [D] **#168** Phase 10: Enhanced Parsing (Pre-requisite) - Update FileOps._parse_markdown() to capture non-task lines in Tasks section `#code` (deleted 2025-12-15, expires 2026-01-14)
  - [D] **#163.45** Phase 10: Release Phase - Beta/pre-release and final release with migration support `#release` (deleted 2025-12-15, expires 2026-01-14)
  - [D] **#163.35** Release phase: Final release of Python version with migration support `#release` (deleted 2025-12-14, expires 2026-01-13)
  - [D] **#163.34** Release phase: Create beta/pre-release for testing with real users `#release` (deleted 2025-12-14, expires 2026-01-13)
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
  - [D] **#51.3** Test update command from system-wide installation location `#test` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#51.2** Fix get_script_path() to handle system-wide installations in /usr/local/bin or /usr/bin `#code` (deleted 2025-11-02, expires 2025-12-02)
  - [D] **#51.1** Investigate get_script_path() function: how it detects script location when installed system-wide `#research` (deleted 2025-11-02, expires 2025-12-02)
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
**todo-ai (mcp)** v3.0.0 | Last Updated: 2026-01-26 01:30:42
