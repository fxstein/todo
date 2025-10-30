# todo ToDo List

> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**

## Tasks
- [ ] **#30** Implement versioned backups and rollback capability `#feature`
  - [ ] **#30.11** Test backup and rollback functionality `#test`
  - [ ] **#30.10** Remove old .bak file creation logic `#cleanup`
  - [ ] **#30.9** Update help text and show_usage() to include new commands `#docs`
  - [ ] **#30.8** Add 'backups' or 'list-backups' command to view available backups `#code`
  - [ ] **#30.7** Add 'rollback' command to main script command handler `#code`
  - [ ] **#30.6** Implement version-specific rollback (restore by timestamp or version) `#code`
  - [ ] **#30.5** Implement default rollback (restore latest backup) `#code`
  - [ ] **#30.4** Create rollback() function to restore from backup `#code`
  - [ ] **#30.3** Create list_backups() function to show available backup versions `#code`
  - [ ] **#30.2** Modify update_tool() to save backups with timestamp to .todo.ai/backups/ `#code`
  - [ ] **#30.1** Create .todo.ai/backups/ directory for storing versioned backups `#setup`
- [ ] **#21** Ensure .todo.ai/ is tracked in git - not in gitignore or explicitly added `#setup`
- [ ] **#19** Move Deleted Tasks section below Recently Completed section `#setup`
- [ ] **#15** Setup githooks `#setup` `#git`
  - [ ] **#15.4** TODO linting (using todo.ai --lint) `#lint`
  - [ ] **#15.3** JSON linting `#lint`
  - [ ] **#15.2** YAML linting `#lint`
  - [ ] **#15.1** Markdown linting `#lint`
- [ ] **#14** Formatting fixes complete `#setup`
- [ ] **#7** Remove gitignore entry for .todo.ai directory - .todo.ai/ must be tracked in git `#setup` `#git`
  - [ ] **#7.1** Add setup instructions documenting that .todo.ai/ must be tracked in git `#docs`
- [ ] **#5** Initialize repository structure and configuration `#setup` `#repo`
------------------

## Deleted Tasks
- [D] **#29** Test task after file rename `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#27** Test task after .todo.ai rename `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#24** Test task after rename `#test` (deleted 2025-10-30, expires 2025-11-29)
- [D] **#4** Test task `#test` (deleted 2025-10-30, expires 2025-11-29)

## Recently Completed
- [x] **#28** Rename files in .todo.ai/ to .todo.ai.log and .todo.ai_serial `#setup` (2025-10-30)
  - [x] **#28.4** Update SERIAL_FILE path reference in todo.ai script `#code` (2025-10-30)
  - [x] **#28.3** Update LOG_FILE path reference in todo.ai script `#code` (2025-10-30)
  - [x] **#28.2** Rename .todo_serial to .todo.ai_serial using git mv `#repo` (2025-10-30)
  - [x] **#28.1** Rename .todo.log to .todo.ai.log using git mv `#repo` (2025-10-30)
- [x] **#17** Create Cursor rules for repository `#setup` `#docs` (2025-10-30)
  - [x] **#17.3** Ensure TODO.md and .todo.ai/ are always committed together `#rules` (2025-10-30)
  - [x] **#17.1** Enforce todo.ai usage for all task tracking `#rules` `#todo` (2025-10-30)
- [x] **#26** Rename .todo/ directory to .todo.ai/ `#setup` (2025-10-30)
  - [x] **#26.10** Update .cursorrules to reference .todo.ai/ instead of .todo/ `#setup` (2025-10-30)
  - [x] **#26.9** Verify git tracking of .todo.ai/ `#test` (2025-10-30)
  - [x] **#26.8** Test script execution after rename `#test` (2025-10-30)
  - [x] **#26.7** Update any documentation files `#docs` (2025-10-30)
  - [x] **#26.6** Update README.md if it mentions .todo/ `#docs` (2025-10-30)
  - [x] **#26.5** Update environment variable names (TODO_SERIAL, TODO_LOG) `#code` (2025-10-30)
  - [x] **#26.4** Update all references to .todo/ in script code `#code` (2025-10-30)
  - [x] **#26.3** Update LOG_FILE path in todo.ai script `#code` (2025-10-30)
  - [x] **#26.2** Update SERIAL_FILE path in todo.ai script `#code` (2025-10-30)
  - [x] **#26.1** Rename directory using git mv: .todo/ -> .todo.ai/ `#repo` (2025-10-30)
- [x] **#25** Rename repository from todo to todo.ai `#setup` (2025-10-30)
  - [x] **#25.6** Update header comment in todo.ai `#code` (2025-10-30)
  - [x] **#25.5** Update README.md repository references `#docs` (2025-10-30)
  - [x] **#25.4** Update SCRIPT_URL in todo.ai script `#code` (2025-10-30)
  - [x] **#25.3** Update REPO_URL in todo.ai script `#code` (2025-10-30)
  - [x] **#25.2** Update local git remote URL after GitHub rename `#repo` (2025-10-30)
  - [x] **#25.1** Rename repository on GitHub (manual step) `#repo` (2025-10-30)
- [x] **#23** Rename todo.ai to todo.ai `#setup` (2025-10-30)
  - [x] **#23.10** Test update command works with new filename `#test` (2025-10-30)
  - [x] **#23.9** Test installation and execution after rename `#test` (2025-10-30)
  - [x] **#23.8** Update all inline comments and documentation in script `#code` (2025-10-30)
  - [x] **#23.7** Update init_cursor_rules() to reference todo.ai `#code` (2025-10-30)
  - [x] **#23.6** Update help text and show_usage() examples `#code` (2025-10-30)
  - [x] **#23.5** Update Cursor rules to reference todo.ai instead of todo.zsh `#setup` (2025-10-30)
  - [x] **#23.4** Update self-references in update_tool() function `#code` (2025-10-30)
  - [x] **#23.3** Update TODO.md template path references `#setup` (2025-10-30)
  - [x] **#23.2** Update all references in README.md (installation, examples, commands) `#docs` (2025-10-30)
  - [x] **#23.1** Update script filename: todo.zsh -> todo.ai `#setup` (2025-10-30)
- [x] **#22** Create update instructions and functions for todo.ai `#setup` (2025-10-30)
  - [x] **#22.3** Option 3: Auto-check version on startup (informational only) `#setup` (2025-10-30)
  - [x] **#22.2** Option 2: Add version info + update command `#setup` (2025-10-30)
  - [x] **#22.1** Option 1: Simple re-download instruction in README `#docs` (2025-10-30)
- [x] **#20** Create radically simplified README.md `#docs` (2025-10-30)
- [x] **#6** Update TODO.md template for this repository `#setup` `#docs` (2025-10-30)
- [x] **#18** Fix TODO.md header upon initialization - use repo name dynamically `#fix` `#setup` (2025-10-30)
  - [x] **#18.1** Remove path from todo.ai upon init `#fix` `#setup` (2025-10-30)
- [x] **#13** All formatting fixes complete `#setup` (2025-10-30)
- [x] **#12** Final formatting test `#test` (2025-10-30)
- [x] **#11** Test new append method `#test` (2025-10-30)
- [x] **#10** Verify formatting works correctly `#test` (2025-10-30)
- [x] **#8** Fix all sed -i calls to use sed_inplace for macOS compatibility `#setup` `#fix` (2025-10-30)
- [x] **#9** Test new formatting fix `#test` (2025-10-30)

---

**Last Updated:** Thu Oct 30 23:31:46 CET 2025
**Repository:** https://github.com/fxstein/todo.ai 
**Maintenance:** Use `todo.ai` script only

