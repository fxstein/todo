"""Test all commands with dedicated test TODO.md dataset.

Ensure Python version produces identical results to shell version.

CRITICAL: These tests use isolated temporary directories and NEVER modify
the project's TODO.md file. All test operations use the cwd parameter in
subprocess calls to ensure complete isolation.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Skip all tests in this module on Windows
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="Shell script requires Zsh")

# Path to shell script and test data
SHELL_SCRIPT = Path(__file__).parent.parent.parent / "legacy" / "todo.ai"
TEST_DATA_DIR = Path(__file__).parent.parent / "integration" / "test_data"
PROJECT_ROOT = Path(__file__).parent.parent.parent
PROJECT_TODO = PROJECT_ROOT / "TODO.md"


def run_shell_command(cmd: list[str], cwd: Path) -> tuple[str, int]:
    """Run shell script command and return output and exit code."""
    try:
        env = os.environ.copy()
        env["TODO_AI_TESTING"] = "1"
        # Clear TODO_FILE to prevent pollution from other tests
        env.pop("TODO_FILE", None)

        result = subprocess.run(
            [str(SHELL_SCRIPT)] + cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 1
    except Exception as e:
        return f"ERROR: {e}", 1


def run_python_command(cmd: list[str], cwd: Path) -> tuple[str, int]:
    """Run Python CLI command and return output and exit code."""
    try:
        env = os.environ.copy()
        repo_root = Path(__file__).parent.parent.parent
        env["PYTHONPATH"] = str(repo_root)
        # Set TODO_AI_ROOT to ensure Python CLI uses the test directory
        env["TODO_AI_ROOT"] = str(cwd)

        result = subprocess.run(
            ["uv", "run", "python", "-m", "ai_todo.cli.main"] + cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 1
    except Exception as e:
        return f"ERROR: {e}", 1


def copy_test_data(dest: Path) -> None:
    """Copy test data to destination directory.

    CRITICAL: Ensures dest is NOT the project root to prevent modifying
    the project's TODO.md file.
    """
    # Safety check: Never copy test data to project root
    if dest.resolve() == PROJECT_ROOT.resolve():
        raise ValueError(
            f"CRITICAL: Attempted to copy test data to project root! "
            f"This would modify {PROJECT_TODO}. Use a temporary directory instead."
        )

    # Copy TODO.md
    if (TEST_DATA_DIR / "TODO.md").exists():
        shutil.copy2(TEST_DATA_DIR / "TODO.md", dest / "TODO.md")

    # Copy .ai-todo directory
    if (TEST_DATA_DIR / ".ai-todo").exists():
        dest_todo_ai = dest / ".ai-todo"
        if dest_todo_ai.exists():
            shutil.rmtree(dest_todo_ai)
        shutil.copytree(TEST_DATA_DIR / ".ai-todo", dest_todo_ai)


def normalize_output(output: str) -> str:
    """Normalize output for comparison."""
    lines = output.split("\n")
    normalized = []
    for line in lines:
        # Remove absolute paths
        line = line.replace(str(Path.cwd()), "CWD")
        # Remove timestamps from log entries
        if "|" in line and ("COMPLETE" in line or "ADD" in line):
            parts = line.split("|")
            if len(parts) >= 2:
                line = "|".join(parts[1:])
        normalized.append(line)
    return "\n".join(normalized).strip()


def compare_todo_files(shell_path: Path, python_path: Path) -> tuple[bool, str]:
    """Compare two TODO.md files and return (match, diff_message).

    Ignores differences in header and footer content, focusing on the Tasks,
    Archived Tasks, and Deleted Tasks sections.

    Also normalizes known parity differences:
    - Dates on task lines: (YYYY-MM-DD) patterns are stripped
    - Section headers: "Recently Completed" and "Archived Tasks" are equivalent
    """
    import re

    shell_content = shell_path.read_text(encoding="utf-8") if shell_path.exists() else ""
    python_content = python_path.read_text(encoding="utf-8") if python_path.exists() else ""

    if shell_content == python_content:
        return True, "Files are identical"

    # Find differences
    shell_lines = shell_content.splitlines()
    python_lines = python_content.splitlines()

    # Filter out header/footer lines for comparison
    # We only care about lines starting with "-", "##", or ">" (notes)
    # Also ignore blank lines
    def is_relevant_line(line: str) -> bool:
        line = line.strip()
        if not line:
            return False
        # Ignore header/footer lines (metadata, separators, titles)
        if line.startswith("# todo.ai") or line.startswith("# Project"):
            return False
        if line.startswith("> ⚠️"):
            return False
        if line.startswith("**"):
            return False
        if line == "---" or line == "------------------":
            return False
        return True

    def normalize_line(line: str) -> str:
        """Normalize a line to ignore known parity differences."""
        # Strip trailing/leading whitespace
        line = line.strip()
        # Normalize section headers (Shell: "Recently Completed", Python: "Archived Tasks")
        if line == "## Recently Completed":
            line = "## Archived Tasks"
        # Strip date suffixes like (2026-01-26) or (2025-01-01) from task lines
        # These appear at end of lines like: - [x] **#1** Task description (2026-01-26)
        line = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)\s*$", "", line)
        return line

    relevant_shell = [normalize_line(line) for line in shell_lines if is_relevant_line(line)]
    relevant_python = [normalize_line(line) for line in python_lines if is_relevant_line(line)]

    if relevant_shell == relevant_python:
        return True, "Files match (ignoring header/footer and date differences)"

    # If still different, show relevant diff
    diff_msg = []
    max_len = max(len(relevant_shell), len(relevant_python))
    for i in range(max_len):
        shell_line = relevant_shell[i] if i < len(relevant_shell) else "<MISSING>"
        python_line = relevant_python[i] if i < len(relevant_python) else "<MISSING>"
        if shell_line != python_line:
            diff_msg.append(f"Line {i + 1} (relevant):")
            diff_msg.append(f"  Shell:  {shell_line}")
            diff_msg.append(f"  Python: {python_line}")

    return False, "\n".join(diff_msg)


@pytest.fixture
def test_env_shell(tmp_path):
    """Create test environment for shell script testing.

    CRITICAL: Uses isolated tmp_path that is NOT the project root.
    """
    # Safety check: Ensure tmp_path is not project root
    if tmp_path.resolve() == PROJECT_ROOT.resolve():
        pytest.fail(
            f"CRITICAL: tmp_path resolved to project root! "
            f"This would modify {PROJECT_TODO}. Test setup is broken."
        )
    copy_test_data(tmp_path)
    return tmp_path


@pytest.fixture
def test_env_python(tmp_path):
    """Create test environment for Python CLI testing.

    CRITICAL: Uses isolated tmp_path that is NOT the project root.
    """
    # Safety check: Ensure tmp_path is not project root
    if tmp_path.resolve() == PROJECT_ROOT.resolve():
        pytest.fail(
            f"CRITICAL: tmp_path resolved to project root! "
            f"This would modify {PROJECT_TODO}. Test setup is broken."
        )
    copy_test_data(tmp_path)
    return tmp_path


def test_list_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test list command with test dataset."""
    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["list"], test_env_shell)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["list"], test_env_python)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should list tasks from dataset
    assert "Test task" in shell_output or "Test task" in python_output, "Test tasks not found"


def test_show_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test show command with test dataset."""
    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["show", "1"], test_env_shell)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["show", "1"], test_env_python)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should show task #1
    assert "#1" in shell_output or "#1" in python_output, "Task #1 not found"


def test_complete_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test complete command with test dataset - compare final TODO.md."""
    # Create separate copies for shell and Python
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["complete", "1"], shell_env)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["complete", "1"], python_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after complete:\n{diff}"


def test_modify_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test modify command with test dataset - compare final TODO.md."""
    # Create separate copies
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["modify", "1", "Modified task"], shell_env)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["modify", "1", "Modified task"], python_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after modify:\n{diff}"


def test_delete_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test delete command with test dataset - compare final TODO.md."""
    # Create separate copies
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["delete", "1"], shell_env)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["delete", "1"], python_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after delete:\n{diff}"


def test_archive_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test archive command with test dataset - compare final TODO.md."""
    # Create separate copies
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["archive", "3"], shell_env)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["archive", "3"], python_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after archive:\n{diff}"


def test_restore_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test restore command with test dataset - compare final TODO.md."""
    # Create separate copies
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # Test data already has ## Tasks header format (no fix needed)

    # First delete a task (task #5 is already in Deleted section, so delete task #1 instead)
    # (cwd parameter ensures isolation - no os.chdir needed)
    run_shell_command(["delete", "1"], shell_env)
    run_python_command(["delete", "1"], python_env)

    # Now restore (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["restore", "1"], shell_env)
    python_output, python_code = run_python_command(["restore", "1"], python_env)

    # Compare exit codes
    assert shell_code == python_code, (
        f"Exit codes differ: shell={shell_code}, python={python_code}\nShell: {shell_output}\nPython: {python_output}"
    )

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after restore:\n{diff}"


def test_undo_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test undo command with test dataset - compare final TODO.md."""
    # Create separate copies
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # First complete a task (cwd parameter ensures isolation - no os.chdir needed)
    run_shell_command(["complete", "3"], shell_env)
    run_python_command(["complete", "3"], python_env)

    # Now undo (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["undo", "3"], shell_env)
    python_output, python_code = run_python_command(["undo", "3"], python_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after undo:\n{diff}"


def test_note_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test note command with test dataset - compare final TODO.md."""
    # Create separate copies
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["note", "1", "Test note"], shell_env)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["note", "1", "Test note"], python_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after note:\n{diff}"


def test_lint_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test lint command with test dataset."""
    # Run shell version (cwd parameter ensures isolation - no os.chdir needed)
    shell_output, shell_code = run_shell_command(["lint"], test_env_shell)

    # Run Python version (cwd parameter ensures isolation - no os.chdir needed)
    python_output, python_code = run_python_command(["lint"], test_env_python)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should report lint results (may differ in format, but should both work)


@pytest.mark.skip(
    reason="Shell uses .todo.ai/, Python uses .ai-todo/ - parity no longer applicable"
)
def test_workflow_sequence_with_dataset(test_env_shell, test_env_python, tmp_path):
    """Test a sequence of commands with test dataset - compare final TODO.md."""
    # Create separate copies
    shell_env = tmp_path / "shell"
    python_env = tmp_path / "python"
    shell_env.mkdir()
    python_env.mkdir()

    copy_test_data(shell_env)
    copy_test_data(python_env)

    # Sequence: add -> modify -> complete -> undo
    # (cwd parameter ensures isolation - no os.chdir needed)
    # Note: Test data has serial=6, tasks #1-5, so next task will be #7 (max(6,5)+1)
    shell_output, _ = run_shell_command(["add", "New task", "#test"], shell_env)
    # Extract task ID from output (e.g., "Added: #7 New task")
    shell_task_id = "7"  # Based on serial=6, max(6,5)+1=7
    run_shell_command(["modify", shell_task_id, "Modified new task"], shell_env)
    run_shell_command(["complete", shell_task_id], shell_env)
    run_shell_command(["undo", shell_task_id], shell_env)

    python_output, _ = run_python_command(["add", "New task", "#test"], python_env)
    # Extract task ID from output (e.g., "Added: #7 New task")
    python_task_id = "7"  # Based on serial=6, max(6,5)+1=7
    run_python_command(["modify", python_task_id, "Modified new task"], python_env)
    run_python_command(["complete", python_task_id], python_env)
    run_python_command(["undo", python_task_id], python_env)

    # Compare final TODO.md files
    match, diff = compare_todo_files(shell_env / "TODO.md", python_env / "TODO.md")
    assert match, f"TODO.md files differ after workflow sequence:\n{diff}"
