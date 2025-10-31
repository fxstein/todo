#!/bin/zsh
# Utilities for ShellSpec examples to execute todo.ai in isolated sandboxes.

set -euo pipefail

if [[ -z "${TODO_AI_PROJECT_ROOT:-}" ]]; then
  echo "TODO_AI_PROJECT_ROOT must be set (exported by tests/run.zsh)." >&2
  exit 1
fi

# Create a disposable sandbox directory with a predictable layout.
create_sandbox() {
  local sandbox
  sandbox="$(mktemp -d "${TMPDIR:-/tmp}/todoai-spec-XXXXXX")"
  mkdir -p "${sandbox}/bin"
  mkdir -p "${sandbox}/.todo.ai"
  echo "${sandbox}"
}

# Remove sandbox directory if it still exists.
destroy_sandbox() {
  local sandbox="$1"
  if [[ -d "${sandbox}" ]]; then
    rm -rf "${sandbox}"
  fi
}

# Copy named fixture into the sandbox.
# Usage: load_fixture "${sandbox}" "empty_repo"
load_fixture() {
  local sandbox="$1"
  local fixture_name="$2"
  local fixture_dir="${TODO_AI_PROJECT_ROOT}/tests/fixtures/${fixture_name}"

  if [[ ! -d "${fixture_dir}" ]]; then
    echo "Fixture not found: ${fixture_name}" >&2
    return 1
  fi

  (cd "${fixture_dir}" && tar -cf - .) | (cd "${sandbox}" && tar -xf -)
}

# Export environment variables so todo.ai operates inside the sandbox.
configure_sandbox_env() {
  local sandbox="$1"
  export TODO_FILE="${sandbox}/TODO.md"
  export TODO_SERIAL="${sandbox}/.todo.ai/.todo.ai.serial"
  export TODO_LOG="${sandbox}/.todo.ai/.todo.ai.log"
  export TODO_BACKUPS_DIR="${sandbox}/.todo.ai/archives"
  export PATH="${sandbox}/bin:${PATH}"
}

# Provide deterministic time output by shadowing the `date` command within the sandbox.
# Example: sandbox_stub_date "$SANDBOX" "2025-01-01 00:00:00"
sandbox_stub_date() {
  local sandbox="$1"
  local timestamp="$2"
  local stub="${sandbox}/bin/date"

  cat > "${stub}" <<EOF
#!/bin/sh
timestamp="${timestamp}"
if [ "\$#" -gt 0 ]; then
  printf '%s\n' "\${timestamp}"
else
  printf '%s\n' "\${timestamp}"
fi
EOF
  chmod +x "${stub}"
}
