import pytest

from todo_ai.core.exceptions import TamperError
from todo_ai.core.file_ops import FileOps


@pytest.fixture
def temp_todo_dir(tmp_path):
    """Create a temporary directory with initialized TODO.md."""
    todo_dir = tmp_path / "todo_project"
    todo_dir.mkdir()

    # Initialize TODO.md
    todo_file = todo_dir / "TODO.md"
    todo_file.write_text("# Tasks\n\n- [ ] **#1** Task 1\n", encoding="utf-8")

    # Initialize .todo.ai
    config_dir = todo_dir / ".todo.ai"
    config_dir.mkdir()

    # Initialize config.yaml
    config_file = config_dir / "config.yaml"
    config_file.write_text("security:\n  tamper_proof: false\n", encoding="utf-8")

    return todo_dir


def test_checksum_calculation(temp_todo_dir):
    """Test that checksum calculation is consistent and normalized."""
    todo_file = temp_todo_dir / "TODO.md"
    file_ops = FileOps(str(todo_file))

    content_unix = "Line 1\nLine 2\n"
    content_win = "Line 1\r\nLine 2\r\n"

    hash_unix = file_ops.calculate_checksum(content_unix)
    hash_win = file_ops.calculate_checksum(content_win)

    assert hash_unix == hash_win
    assert len(hash_unix) == 64  # SHA-256 length


def test_initialization_creates_checksum(temp_todo_dir):
    """Test that initializing FileOps creates a checksum file."""
    todo_file = temp_todo_dir / "TODO.md"
    checksum_file = temp_todo_dir / ".todo.ai" / "checksum"

    assert not checksum_file.exists()

    FileOps(str(todo_file))

    assert checksum_file.exists()
    assert len(checksum_file.read_text().strip()) == 64


def test_tamper_detection_passive_mode(temp_todo_dir):
    """Test that passive mode logs warning but allows access."""
    todo_file = temp_todo_dir / "TODO.md"
    _ = FileOps(str(todo_file))

    # Modify file externally
    todo_file.write_text("# Tasks\n\n- [ ] **#1** Task 1 Modified\n", encoding="utf-8")

    # Re-initialize (should detect tamper but auto-accept in passive mode)
    # Note: verify_integrity is called in __init__
    file_ops_new = FileOps(str(todo_file))

    # Checksum should be updated to match new content
    checksum_file = temp_todo_dir / ".todo.ai" / "checksum"
    new_checksum = file_ops_new.calculate_checksum(todo_file.read_text(encoding="utf-8"))
    assert checksum_file.read_text().strip() == new_checksum

    # Log should contain TAMPER_DETECTED
    log_file = temp_todo_dir / ".todo.ai" / ".todo.ai.log"
    assert "TAMPER_DETECTED" in log_file.read_text(encoding="utf-8")


def test_tamper_detection_active_mode(temp_todo_dir):
    """Test that active mode raises TamperError."""
    todo_file = temp_todo_dir / "TODO.md"
    config_file = temp_todo_dir / ".todo.ai" / "config.yaml"

    # Enable active mode
    config_file.write_text("security:\n  tamper_proof: true\n", encoding="utf-8")

    # Initialize to set checksum
    FileOps(str(todo_file))

    # Modify file externally
    todo_file.write_text("# Tasks\n\n- [ ] **#1** Task 1 Modified\n", encoding="utf-8")

    # Re-initialize should raise TamperError
    with pytest.raises(TamperError):
        FileOps(str(todo_file))


def test_accept_tamper(temp_todo_dir):
    """Test accepting tamper updates checksum and archives event."""
    todo_file = temp_todo_dir / "TODO.md"
    config_file = temp_todo_dir / ".todo.ai" / "config.yaml"

    # Enable active mode
    config_file.write_text("security:\n  tamper_proof: true\n", encoding="utf-8")

    # Initialize
    _ = FileOps(str(todo_file))

    # Modify file externally
    _ = todo_file.read_text(encoding="utf-8")
    new_content = "# Tasks\n\n- [ ] **#1** Task 1 Modified\n"
    todo_file.write_text(new_content, encoding="utf-8")

    # Verify it raises error
    with pytest.raises(TamperError):
        FileOps(str(todo_file))

    # Accept tamper (using skip_verify to get instance)
    file_ops_tampered = FileOps(str(todo_file), skip_verify=True)
    file_ops_tampered.accept_tamper("Test reason")

    # Now it should work
    FileOps(str(todo_file))

    # Check archive
    tamper_dir = temp_todo_dir / ".todo.ai" / "tamper"
    assert tamper_dir.exists()
    # Should have one timestamped directory
    event_dirs = list(tamper_dir.glob("*"))
    assert len(event_dirs) == 1

    # Check archived files
    # Note: shadow copy might not exist if we only did one write before tampering
    # In this test flow:
    # 1. FileOps init -> updates integrity (writes checksum and shadow)
    # 2. External modify -> shadow is OLD content
    # 3. Accept tamper -> archives shadow (original) and current (forced)

    assert (event_dirs[0] / "original.md").exists()
    assert (event_dirs[0] / "forced.md").exists()
    assert (event_dirs[0] / "forced.md").read_text(encoding="utf-8") == new_content


def test_shadow_copy_update(temp_todo_dir):
    """Test that shadow copy is updated on write."""
    todo_file = temp_todo_dir / "TODO.md"
    file_ops = FileOps(str(todo_file))

    # Write tasks (simulated via update_integrity for simplicity, or full write)
    # Let's use update_integrity directly as it's what we want to test
    content = "New content"
    file_ops.update_integrity(content)

    shadow_file = temp_todo_dir / ".todo.ai" / "shadow" / "TODO.md"
    assert shadow_file.exists()
    assert shadow_file.read_text(encoding="utf-8") == content
