"""Test that forbidden flags are not present in codebase."""

import subprocess
from pathlib import Path


def test_no_forbidden_flags():
    """Verify that --no-verify is not present in any process scripts or workflows.

    This test uses string concatenation to avoid self-detection.
    The forbidden flag bypasses all pre-commit hooks and safety checks,
    and is ETERNALLY FORBIDDEN without explicit human approval.
    """
    # Build the forbidden flag using string concatenation to avoid self-detection
    forbidden = "--no-" + "verify"

    # Get project root
    project_root = Path(__file__).parent.parent.parent

    # Directories to check
    check_dirs = [
        project_root / "release",
        project_root / ".github",
        project_root / "scripts",
    ]

    # Collect all shell and yaml files
    files_to_check = []
    for directory in check_dirs:
        if directory.exists():
            files_to_check.extend(directory.rglob("*.sh"))
            files_to_check.extend(directory.rglob("*.yml"))
            files_to_check.extend(directory.rglob("*.yaml"))

    # Search for the forbidden flag
    found_in = []
    for file_path in files_to_check:
        try:
            content = file_path.read_text(encoding="utf-8")
            if forbidden in content:
                found_in.append(str(file_path.relative_to(project_root)))
        except Exception:
            # Skip files that can't be read
            pass

    # Assert no occurrences found
    assert not found_in, (
        f"CRITICAL: Found forbidden flag '{forbidden}' in the following files:\n"
        + "\n".join(f"  - {f}" for f in found_in)
        + f"\n\nThe flag '{forbidden}' is ETERNALLY FORBIDDEN.\n"
        + "It bypasses all pre-commit hooks and safety checks.\n"
        + "No automated process may use it without explicit human approval."
    )


def test_check_forbidden_flags_script_exists():
    """Verify that the check-forbidden-flags.sh script exists and is executable."""
    import platform

    project_root = Path(__file__).parent.parent.parent
    script_path = project_root / "scripts" / "check-forbidden-flags.sh"

    assert script_path.exists(), "check-forbidden-flags.sh script is missing"

    # Only check executable bit on Unix-like systems
    if platform.system() != "Windows":
        assert script_path.stat().st_mode & 0o111, "check-forbidden-flags.sh is not executable"


def test_check_forbidden_flags_script_works():
    """Verify that the check-forbidden-flags.sh script runs successfully."""
    import platform

    import pytest

    # Skip on Windows - bash scripts don't work natively
    if platform.system() == "Windows":
        pytest.skip("Bash scripts not supported on Windows")

    project_root = Path(__file__).parent.parent.parent
    script_path = project_root / "scripts" / "check-forbidden-flags.sh"

    # Run the script
    result = subprocess.run([str(script_path)], cwd=project_root, capture_output=True, text=True)

    # Should pass (exit 0) with no forbidden flags
    assert result.returncode == 0, (
        f"check-forbidden-flags.sh failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
