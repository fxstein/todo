#!/bin/zsh
#
# Entry point for running the ShellSpec test suite.
#
# Responsibilities:
#   - Ensure ShellSpec is available (use vendor copy when not installed globally)
#   - Export environment variables consumed by the specs (project root, shell path)
#   - Pass through arguments to shellspec (pattern overrides, focus options, etc.)

set -euo pipefail

readonly SCRIPT_DIR="$(cd "${0:A:h}" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly VENDOR_DIR="${PROJECT_ROOT}/tests/vendor"
readonly BOOTSTRAP="${PROJECT_ROOT}/tests/bin/bootstrap_shellspec.zsh"

# Use zsh for specs to match the todo.ai implementation language.
export SHELLSPEC_SHELL="${SHELLSPEC_SHELL:-/bin/zsh}"

# Make project root available to helpers and specs.
export TODO_AI_PROJECT_ROOT="${PROJECT_ROOT}"

# Locate shellspec command. Prefer globally installed version, fall back to vendor.
if command -v shellspec >/dev/null 2>&1; then
  SHELLSPEC_CMD="$(command -v shellspec)"
else
  "${BOOTSTRAP}" >/dev/null
  SHELLSPEC_CMD="${VENDOR_DIR}/shellspec-0.28.1/bin/shellspec"
  if [[ ! -x "${SHELLSPEC_CMD}" ]]; then
    echo "ShellSpec executable not found after bootstrap" >&2
    exit 1
  fi
  export PATH="${VENDOR_DIR}/shellspec-0.28.1/bin:${PATH}"
fi

cd "${PROJECT_ROOT}"

exec "${SHELLSPEC_CMD}" \
  --shell "${SHELLSPEC_SHELL}" \
  --helperdir "${PROJECT_ROOT}/tests/spec" \
  --pattern "${SHELLSPEC_PATTERN:-*_spec.sh}" \
  "$@" \
  "${PROJECT_ROOT}/tests/spec"
