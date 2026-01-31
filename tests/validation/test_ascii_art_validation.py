"""Validation tests for ASCII art formatting."""

import subprocess


def test_ascii_guard_installed():
    """Verify ascii-guard is installed and executable."""
    result = subprocess.run(
        ["uv", "run", "ascii-guard", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "ascii-guard not installed or not executable"
    assert "ascii-guard" in result.stdout.lower(), "Unexpected version output"


def test_ascii_guard_passes_on_all_docs():
    """Verify all documentation passes ascii-guard linting."""
    result = subprocess.run(
        ["uv", "run", "ascii-guard", "lint", "docs/"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"ascii-guard found errors in documentation:\n{result.stdout}\n{result.stderr}"
    )
