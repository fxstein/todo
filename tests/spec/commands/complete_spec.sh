#!/bin/zsh

Describe 'todo.ai complete'
  Include "$TODO_AI_PROJECT_ROOT/tests/spec/spec_helper.sh"

  setup_sandbox() {
    SANDBOX=$(create_sandbox)
    configure_sandbox_env "${SANDBOX}"
    sandbox_stub_date "${SANDBOX}" "2025-02-02 12:00:00"
  }

  cleanup_sandbox() {
    destroy_sandbox "${SANDBOX}"
  }

  BeforeEach 'setup_sandbox'
  AfterEach 'cleanup_sandbox'

  It 'marks a single task as completed'
    todo_ai add "Finish docs" >/dev/null
    When run todo_ai complete 1
    The status should be success
    The output should include "Marked 1 task(s) as completed"
    The contents of file "$TODO_FILE" should include "- [x] **#1** Finish docs"
    The contents of file "$TODO_FILE" should not include "- [ ] **#1** Finish docs"
  End

  It 'completes parent and subtasks with --with-subtasks'
    todo_ai add "Parent" >/dev/null
    todo_ai add-subtask 1 "Child" >/dev/null
    When run todo_ai complete 1 --with-subtasks
    The status should be success
    The output should include "Marked 2 task(s) as completed"
    The contents of file "$TODO_FILE" should include "- [x] **#1** Parent"
    The contents of file "$TODO_FILE" should include "- [x] **#1.1** Child"
  End
End
