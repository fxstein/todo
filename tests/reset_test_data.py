from pathlib import Path


def reset_test_data():
    """Resets the test data directory to a clean state."""
    base_dir = Path(__file__).parent / "integration" / "test_data"

    # Create directory if it doesn't exist
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create .todo.ai directory
    config_dir = base_dir / ".todo.ai"
    config_dir.mkdir(exist_ok=True)

    # Create default TODO.md
    todo_content = """# Tasks

- [ ] **#1** Test task 1
- [ ] **#2** Test task 2 `#tag1`
- [x] **#3** Completed task
  > Note on completed task

## Recently Completed
- [x] **#4** Archived task 1 (2025-01-01)

## Deleted Tasks
- [ ] **#5** Deleted task 1 (2025-01-01)
"""
    (base_dir / "TODO.md").write_text(todo_content)

    # Create config files
    (config_dir / "config.yaml").write_text("mode: single-user\ncoordination:\n  type: none\n")
    (config_dir / ".todo.ai.serial").write_text("6")
    (config_dir / ".todo.ai.log").write_text("")

    print(f"Test data reset in {base_dir}")


if __name__ == "__main__":
    reset_test_data()
