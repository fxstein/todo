Pinned Project Directory Investigation
======================================

Context
-------
The todo.ai CLI currently initializes its working files based on the directory
where the script is invoked. This can cause accidental initialization in
unintended directories when the user runs the command from a submodule or
different working directory than the intended project root.

Findings
--------
1) The script captures the current working directory at startup as
   `ORIGINAL_WORKING_DIR=$(pwd)`.

2) Core paths are derived from `ORIGINAL_WORKING_DIR`:
   - `TODO_FILE` -> `${ORIGINAL_WORKING_DIR}/TODO.md`
   - `LOG_FILE` -> `${ORIGINAL_WORKING_DIR}/.todo.ai/.todo.ai.log`
   - `SERIAL_FILE` -> `${ORIGINAL_WORKING_DIR}/.todo.ai/.todo.ai.serial`
   - `CONFIG_FILE` -> `${ORIGINAL_WORKING_DIR}/.todo.ai/config.yaml`

3) Initialization runs before CLI argument handling:
   - `init_log_file`
   - `init_todo_file`
   - `run_migrations`
   - `init_cursor_rules`

   This means calling `todo.ai` from any directory will create `.todo.ai/`
   and `TODO.md` in that directory before any command-specific logic runs.

4) `init_cursor_rules` also uses `pwd`, so rule creation is tied to the
   invocation directory as well.

5) The only existing override mechanism is environment variables
   (`TODO_FILE`, `TODO_SERIAL`, `TODO_LOG`, `TODO_CONFIG`), which are not
   exposed as a user-facing pinning feature.

Implication
-----------
To support a pinned project directory, the script needs a reliable mechanism
to resolve the intended root before initialization and then set the derived
paths accordingly. This likely requires a new config value and a pre-init
directory resolution step.
