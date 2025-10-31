#!/bin/zsh
#
# Download and unpack ShellSpec into tests/vendor when it is not already available.
# This script favours repeatable installations by pinning the ShellSpec version.
#
# It creates the following structure:
#   tests/vendor/shellspec-${version}/
#     bin/shellspec
#     lib/
#
# The top-level tests/run.zsh wrapper will add the extracted bin directory to PATH
# when ShellSpec is not installed globally.

set -euo pipefail

readonly SCRIPT_DIR="$(cd "${0:A:h}" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
readonly VENDOR_DIR="${PROJECT_ROOT}/tests/vendor"

# Pin to a known-good ShellSpec release to keep behaviour deterministic.
readonly SHELLSPEC_VERSION="0.28.1"
readonly ARCHIVE_URL="https://github.com/shellspec/shellspec/archive/refs/tags/${SHELLSPEC_VERSION}.tar.gz"
readonly DEST_DIR="${VENDOR_DIR}/shellspec-${SHELLSPEC_VERSION}"

# Allow callers to skip the download when running in fully offline environments
# that already have the archive mirrored locally.
if [[ -n "${SHELLSPEC_OFFLINE:-}" ]]; then
  if [[ ! -d "${DEST_DIR}" ]]; then
    echo "ShellSpec ${SHELLSPEC_VERSION} is not available in tests/vendor and SHELLSPEC_OFFLINE is set." >&2
    echo "Either unset SHELLSPEC_OFFLINE or place the extracted archive at ${DEST_DIR}" >&2
    exit 1
  fi
fi

if [[ -x "${DEST_DIR}/bin/shellspec" ]]; then
  exit 0
fi

mkdir -p "${VENDOR_DIR}"

if [[ -z "${SHELLSPEC_OFFLINE:-}" ]]; then
  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is required to download ShellSpec" >&2
    exit 1
  fi

  tmp_archive="$(mktemp)"
  trap 'rm -f "${tmp_archive}"' EXIT

  echo "Downloading ShellSpec ${SHELLSPEC_VERSION}..." >&2
  curl -fsSL "${ARCHIVE_URL}" -o "${tmp_archive}"

  echo "Extracting ShellSpec..." >&2
  tar -xzf "${tmp_archive}" -C "${VENDOR_DIR}"
else
  if [[ ! -d "${DEST_DIR}" ]]; then
    echo "ShellSpec archive not found and SHELLSPEC_OFFLINE prevents downloading." >&2
    exit 1
  fi
fi

# Some tar implementations extract to shellspec-${version}/; ensure DEST_DIR matches.
if [[ ! -x "${DEST_DIR}/bin/shellspec" ]]; then
  if [[ -d "${DEST_DIR}" ]]; then
    chmod +x "${DEST_DIR}/bin/shellspec"
  else
    echo "Failed to locate shellspec-${SHELLSPEC_VERSION} after extraction." >&2
    exit 1
  fi
fi

echo "ShellSpec ${SHELLSPEC_VERSION} installed in ${DEST_DIR}" >&2
