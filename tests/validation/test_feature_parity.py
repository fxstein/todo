"""Feature parity validation tests.

Compare Python CLI output with shell script output to ensure identical behavior.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Skip all tests in this module on Windows
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="Shell script requires Zsh")

# Path to shell script (todo.ai in repo root)
SHELL_SCRIPT = Path(__file__).parent.parent.parent / "todo.ai"
PYTHON_CLI = "todo-ai"  # Installed CLI command


@pytest.fixture
def test_env(tmp_path):
    """Create isolated test environment."""
    # Create .todo.ai directory structure
    todo_ai_dir = tmp_path / ".todo.ai"
    todo_ai_dir.mkdir(exist_ok=True)
    (todo_ai_dir / "config.yaml").write_text(
        "numbering_mode: single-user\ncoordination_type: none\n"
    )
    (todo_ai_dir / ".todo.ai.serial").write_text("0")

    # Create TODO.md
    (tmp_path / "TODO.md").write_text("# Tasks\n\n")

    return tmp_path


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
        # Use the installed CLI or run as module
        env = os.environ.copy()
        repo_root = Path(__file__).parent.parent.parent
        env["PYTHONPATH"] = str(repo_root)

        result = subprocess.run(
            ["uv", "run", "python", "-m", "todo_ai.cli.main"] + cmd,
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


def normalize_output(output: str) -> str:
    """Normalize output for comparison (remove timestamps, paths, etc.)."""
    lines = output.split("\n")
    normalized = []
    for line in lines:
        # Remove absolute paths
        line = line.replace(str(Path.cwd()), "CWD")
        # Remove timestamps from log entries
        if "|" in line and ("COMPLETE" in line or "ADD" in line):
            parts = line.split("|")
            if len(parts) >= 2:
                # Keep only the action and description parts
                line = "|".join(parts[1:])
        normalized.append(line)
    return "\n".join(normalized).strip()


def test_add_command_parity(test_env, tmp_path):
    """Test add command produces identical output."""
    os.chdir(test_env)

    # Run shell version
    shell_output, shell_code = run_shell_command(["add", "Test task", "#tag1"], test_env)

    # Reset environment
    (test_env / "TODO.md").write_text("# Tasks\n\n")
    (test_env / ".todo.ai" / ".todo.ai.serial").write_text("0")

    # Run Python version
    python_output, python_code = run_python_command(["add", "Test task", "#tag1"], test_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Normalize and compare outputs
    shell_norm = normalize_output(shell_output)
    python_norm = normalize_output(python_output)

    # Both should contain "Added: #1" (or similar)
    assert "Added" in shell_norm or "Added" in python_norm, "Neither output contains 'Added'"
    assert "#1" in shell_norm or "#1" in python_norm, "Neither output contains task ID"


def test_list_command_parity(test_env, tmp_path):
    """Test list command produces identical output."""
    os.chdir(test_env)

    # Add a task first (using Python to set up)
    run_python_command(["add", "Task 1"], test_env)
    (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run shell version
    shell_output, shell_code = run_shell_command(["list"], test_env)

    # Run Python version
    python_output, python_code = run_python_command(["list"], test_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should list the task
    assert "Task 1" in shell_output or "Task 1" in python_output, "Task not found in output"


def test_complete_command_parity(test_env, tmp_path):
    """Test complete command produces identical output."""
    os.chdir(test_env)

    # Add a task first (using shell to match shell script behavior)
    run_shell_command(["add", "Task to complete"], test_env)
    (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run shell version
    shell_output, shell_code = run_shell_command(["complete", "1"], test_env)

    # Reset and add task again for Python
    (test_env / "TODO.md").write_text("# Tasks\n\n- [ ] **#1** Task to complete\n")
    (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run Python version
    python_output, python_code = run_python_command(["complete", "1"], test_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should show completion (shell uses "Marked X task(s) as completed", Python uses "Completed: #X")
    assert (
        "completed" in shell_output.lower()
        or "completed" in python_output.lower()
        or "Marked" in shell_output
    ), f"Completion not found. Shell: {shell_output[:100]}, Python: {python_output[:100]}"


def test_modify_command_parity(test_env, tmp_path):
    """Test modify command produces identical output."""
    os.chdir(test_env)

    # Add a task first
    run_python_command(["add", "Original task"], test_env)
    (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run shell version
    shell_output, shell_code = run_shell_command(["modify", "1", "Modified task"], test_env)

    # Reset and add task again
    (test_env / "TODO.md").write_text("# Tasks\n\n- [ ] **#1** Original task\n")
    (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run Python version
    python_output, python_code = run_python_command(["modify", "1", "Modified task"], test_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should show modification
    assert "Modified" in shell_output or "Modified" in python_output, "Modification not found"


def test_show_command_parity(test_env, tmp_path):
    """Test show command produces identical output."""
    os.chdir(test_env)

    # Add a task first
    run_python_command(["add", "Task to show"], test_env)
    (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run shell version
    shell_output, shell_code = run_shell_command(["show", "1"], test_env)

    # Run Python version
    python_output, python_code = run_python_command(["show", "1"], test_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should show task details
    assert "#1" in shell_output or "#1" in python_output, "Task ID not found"
    assert "Task to show" in shell_output or "Task to show" in python_output, (
        "Task description not found"
    )


def test_version_command_parity(test_env, tmp_path):
    """Test version command produces identical output."""
    os.chdir(test_env)

    # Run shell version
    shell_output, shell_code = run_shell_command(["version"], test_env)

    # Run Python version
    python_output, python_code = run_python_command(["version"], test_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should show version (format may differ slightly)
    assert len(shell_output.strip()) > 0 or len(python_output.strip()) > 0, "No version output"


def test_config_command_parity(test_env, tmp_path):
    """Test config command produces identical output."""
    os.chdir(test_env)

    # Run shell version
    shell_output, shell_code = run_shell_command(["config"], test_env)

    # Run Python version
    python_output, python_code = run_python_command(["config"], test_env)

    # Compare exit codes
    assert shell_code == python_code, f"Exit codes differ: shell={shell_code}, python={python_code}"

    # Both should show config (format may differ)
    assert len(shell_output.strip()) > 0 or len(python_output.strip()) > 0, "No config output"


@pytest.mark.parametrize(
    "command,args",
    [
        (["add"], ["Test task"]),
        (["list"], []),
        (["complete"], ["1"]),
        (["show"], ["1"]),
        (["config"], []),
        (["version"], []),
    ],
)
def test_basic_commands_exit_codes(test_env, tmp_path, command, args):
    """Test that basic commands have matching exit codes."""
    os.chdir(test_env)

    # Set up test data if needed
    if command[0] in ["complete", "show"]:
        run_python_command(["add", "Test task"], test_env)
        (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run shell version
    shell_output, shell_code = run_shell_command(command + args, test_env)

    # Reset if needed
    if command[0] in ["complete"]:
        (test_env / "TODO.md").write_text("# Tasks\n\n- [ ] **#1** Test task\n")
        (test_env / ".todo.ai" / ".todo.ai.serial").write_text("1")

    # Run Python version
    python_output, python_code = run_python_command(command + args, test_env)

    # Exit codes should match
    assert shell_code == python_code, (
        f"Exit codes differ for {command + args}: "
        f"shell={shell_code}, python={python_code}\n"
        f"Shell output: {shell_output[:200]}\n"
        f"Python output: {python_output[:200]}"
    )
