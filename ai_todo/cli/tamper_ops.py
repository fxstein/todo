import difflib
import sys

from ai_todo.core.file_ops import FileOps


def tamper_diff_command(todo_path: str = "TODO.md") -> None:
    """Show diff between current TODO.md and shadow copy."""
    # Initialize with skip_verify=True to avoid raising TamperError immediately
    file_ops = FileOps(todo_path, skip_verify=True)

    if not file_ops.todo_path.exists():
        print("Error: TODO.md not found")
        return

    if not file_ops.shadow_path.exists():
        print("Error: No shadow copy found. Cannot show diff.")
        return

    try:
        current_lines = file_ops.todo_path.read_text(encoding="utf-8").splitlines()
        shadow_lines = file_ops.shadow_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    diff = difflib.unified_diff(
        shadow_lines,
        current_lines,
        fromfile="Shadow Copy (Last Valid)",
        tofile="Current File (Tampered)",
        lineterm="",
    )

    print("Tamper Diff:")
    print("============")
    diff_lines = list(diff)
    if not diff_lines:
        print("No differences found (files match).")
        return

    for line in diff_lines:
        if line.startswith("+") and not line.startswith("+++"):
            print(f"\033[92m{line}\033[0m")  # Green
        elif line.startswith("-") and not line.startswith("---"):
            print(f"\033[91m{line}\033[0m")  # Red
        elif line.startswith("@"):
            print(f"\033[96m{line}\033[0m")  # Cyan
        else:
            print(line)


def tamper_accept_command(reason: str, todo_path: str = "TODO.md") -> None:
    """Accept external changes."""
    # Initialize with skip_verify=True to bypass the check
    file_ops = FileOps(todo_path, skip_verify=True)

    try:
        file_ops.accept_tamper(reason)
        print("✅ External changes accepted and archived.")
        print(f"   Reason: {reason}")
    except Exception as e:
        print(f"Error accepting changes: {e}")
        sys.exit(1)
