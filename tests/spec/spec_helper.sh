#!/bin/zsh

set -euo pipefail

if [[ -z "${TODO_AI_PROJECT_ROOT:-}" ]]; then
  readonly SPEC_DIR="$(cd "${0:A:h}" && pwd)"
  export TODO_AI_PROJECT_ROOT="$(cd "${SPEC_DIR}/../.." && pwd)"
fi

source "${TODO_AI_PROJECT_ROOT}/tests/helpers/sandbox.zsh"

# Convenience wrapper around the todo.ai executable.
todo_ai() {
  "${TODO_AI_PROJECT_ROOT}/todo.ai" "$@"
}

# Helper to capture the entire TODO.md file content (if present) for assertions.
todo_file_contents() {
  if [[ -f "${TODO_FILE:-}" ]]; then
    cat "${TODO_FILE}"
  fi
}
