#!/bin/zsh

Describe 'todo.ai add'
  Include "$TODO_AI_PROJECT_ROOT/tests/spec/spec_helper.sh"

  setup_sandbox() {
    SANDBOX=$(create_sandbox)
    configure_sandbox_env "${SANDBOX}"
    sandbox_stub_date "${SANDBOX}" "2025-01-01 00:00:00"
  }

  cleanup_sandbox() {
    destroy_sandbox "${SANDBOX}"
  }

  BeforeEach 'setup_sandbox'
  AfterEach 'cleanup_sandbox'

  It 'creates TODO.md and serial for first task'
    When run todo_ai add "Write shellspec tests" "#testing"
    The status should be success
    The output should include "Added: #1"
    The path "$TODO_FILE" should be exist
    The path "$TODO_SERIAL" should be exist
    The contents of file "$TODO_FILE" should include "**#1** Write shellspec tests"
    The contents of file "$TODO_FILE" should include "`#testing`"
    The contents of file "$TODO_SERIAL" should equal "1"
  End

  It 'appends subsequent tasks and increments serial'
    todo_ai add "Write initial task" >/dev/null
    When run todo_ai add "Review output" "#ops"
    The status should be success
    The output should include "Added: #2"
    The contents of file "$TODO_SERIAL" should equal "2"
    The contents of file "$TODO_FILE" should include "**#2** Review output"
    The contents of file "$TODO_FILE" should include "**#1** Write initial task"
  End
End
