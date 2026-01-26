import pytest

from todo_ai.core.file_ops import FileOps, FileStructureSnapshot
from todo_ai.core.task import Task, TaskStatus


@pytest.fixture
def temp_todo_file(tmp_path):
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text("# Tasks\n", encoding="utf-8")
    return todo_path


@pytest.fixture
def file_ops(temp_todo_file):
    return FileOps(str(temp_todo_file))


def test_init_creates_config_dir(tmp_path):
    todo_path = tmp_path / "TODO.md"
    _ = FileOps(str(todo_path))
    assert (tmp_path / ".todo.ai").exists()
    assert (tmp_path / ".todo.ai").is_dir()


def test_read_tasks_empty(file_ops):
    tasks = file_ops.read_tasks()
    assert len(tasks) == 0


def test_write_and_read_tasks(file_ops):
    t1 = Task(id="1", description="Task 1", status=TaskStatus.PENDING)
    t2 = Task(id="2", description="Task 2", status=TaskStatus.COMPLETED)
    t2.add_note("Note for task 2")

    file_ops.write_tasks([t1, t2])

    read_tasks = file_ops.read_tasks()
    assert len(read_tasks) == 2

    rt1 = next(t for t in read_tasks if t.id == "1")
    assert rt1.description == "Task 1"
    assert rt1.status == TaskStatus.PENDING

    rt2 = next(t for t in read_tasks if t.id == "2")
    assert rt2.description == "Task 2"
    assert rt2.status == TaskStatus.COMPLETED
    assert len(rt2.notes) == 1
    assert rt2.notes[0] == "Note for task 2"


def test_parse_complex_todo(tmp_path):
    content = """# todo.ai ToDo List

> Warning

## Tasks
- [ ] **#1** Task 1 `#tag1`
  > Note 1
- [x] **#2** Task 2
- [ ] **#3** Task 3
  - [ ] **#3.1** Subtask 3.1

## Recently Completed
- [x] **#4** Archived Task

## Deleted Tasks
- [ ] **#5** Deleted Task
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    assert len(tasks) == 6  # 1, 2, 3, 3.1, 4, 5

    t1 = next(t for t in tasks if t.id == "1")
    assert t1.description == "Task 1"  # Tags removed from description
    assert "tag1" in t1.tags  # Tags stored separately
    assert t1.notes == ["Note 1"]

    t3_1 = next(t for t in tasks if t.id == "3.1")
    assert t3_1.status == TaskStatus.PENDING

    t4 = next(t for t in tasks if t.id == "4")
    assert t4.status == TaskStatus.ARCHIVED

    t5 = next(t for t in tasks if t.id == "5")
    assert t5.status == TaskStatus.DELETED


def test_serial_ops(file_ops):
    # Initial state
    assert file_ops.get_serial() == 0

    # Set serial
    file_ops.set_serial(5)
    assert file_ops.get_serial() == 5
    assert (file_ops.config_dir / ".todo.ai.serial").read_text() == "5"

    # Set again
    file_ops.set_serial(10)
    assert file_ops.get_serial() == 10
    assert (file_ops.config_dir / ".todo.ai.serial").read_text() == "10"


def test_relationships(tmp_path):
    content = """# todo.ai ToDo List

## Tasks
- [ ] **#1** Task 1
- [ ] **#2** Task 2

## Task Metadata

Task relationships and dependencies (managed by todo.ai tool).
View with: `./todo.ai show <task-id>`

<!-- TASK RELATIONSHIPS
1:depends-on:2
1:blocks:3
2:related-to:1 4
-->
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    # Check relationships
    rels_1 = ops.get_relationships("1")
    assert "depends-on" in rels_1
    assert rels_1["depends-on"] == ["2"]
    assert "blocks" in rels_1
    assert rels_1["blocks"] == ["3"]

    rels_2 = ops.get_relationships("2")
    assert "related-to" in rels_2
    assert rels_2["related-to"] == ["1", "4"]

    # Add a relationship
    ops.add_relationship("1", "completed-by", ["5", "6"])
    ops.write_tasks(tasks)

    # Read back and verify
    ops2 = FileOps(str(todo_path))
    ops2.read_tasks()
    rels_1_updated = ops2.get_relationships("1")
    assert "completed-by" in rels_1_updated
    assert rels_1_updated["completed-by"] == ["5", "6"]
    # Old relationships should still be there
    assert "depends-on" in rels_1_updated
    assert "blocks" in rels_1_updated


def test_interleaved_content_capture(tmp_path):
    """Phase 10: Test that interleaved content (non-task lines) is captured."""
    content = """## Tasks
- [ ] **#1** Task 1
  > Note for task 1
# This is a comment between tasks
- [ ] **#2** Task 2
  > Note for task 2

# Another comment
- [ ] **#3** Task 3
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    # Verify tasks are parsed
    assert len(tasks) == 3

    # Verify interleaved content is captured
    # Task 1 should have comment after it
    assert "1" in ops.interleaved_content
    assert "# This is a comment between tasks" in ops.interleaved_content["1"]

    # Task 2 should have comment after it (blank lines are not captured)
    assert "2" in ops.interleaved_content
    interleaved_2 = ops.interleaved_content["2"]
    assert "# Another comment" in interleaved_2
    # Blank lines are NOT captured (handled by existing logic)

    # Task 3 should have no interleaved content (it's the last task)
    assert "3" not in ops.interleaved_content or len(ops.interleaved_content.get("3", [])) == 0


def test_interleaved_content_excludes_blank_lines(tmp_path):
    """Phase 10: Test that blank lines are NOT captured as interleaved content (handled by existing logic)."""
    content = """## Tasks
- [ ] **#1** Task 1

- [ ] **#2** Task 2
# Comment after task 2
- [ ] **#3** Task 3
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    assert len(tasks) == 3

    # Verify blank lines are NOT captured (they're handled by existing blank line logic)
    assert "1" not in ops.interleaved_content or "" not in ops.interleaved_content.get("1", [])

    # Verify non-blank interleaved content (comments) IS captured
    assert "2" in ops.interleaved_content
    assert "# Comment after task 2" in ops.interleaved_content["2"]


def test_structure_snapshot_creation(tmp_path):
    """Phase 11: Test that structure snapshot is created on first read."""
    content = """# Custom Header
> Some warning

## Tasks
- [ ] **#1** Task 1
# Comment
- [ ] **#2** Task 2

## Recently Completed
- [x] **#3** Task 3

------------------
**Last Updated:** 2025-01-01
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    ops.read_tasks()

    # Verify snapshot was created
    assert ops._structure_snapshot is not None
    snapshot = ops._structure_snapshot

    # Verify snapshot captures structure elements
    assert snapshot.tasks_header_format == "## Tasks"
    assert snapshot.blank_after_tasks_header is False  # Task follows directly
    assert snapshot.has_original_header is True
    assert "# Custom Header" in snapshot.header_lines
    assert "**Last Updated:** 2025-01-01" in snapshot.footer_lines
    assert "1" in snapshot.interleaved_content
    assert "# Comment" in snapshot.interleaved_content["1"]


def test_structure_snapshot_persistence(tmp_path):
    """Phase 11: Test that snapshot persists across multiple read_tasks() calls."""
    content = """## Tasks
- [ ] **#1** Task 1
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    ops.read_tasks()
    snapshot1 = ops._structure_snapshot
    mtime1 = ops._snapshot_mtime

    # Read again without modifying file
    ops.read_tasks()
    snapshot2 = ops._structure_snapshot
    mtime2 = ops._snapshot_mtime

    # Snapshot should be the same object (not recreated)
    snapshot2 = ops._structure_snapshot
    mtime2 = ops._snapshot_mtime
    assert snapshot1 is snapshot2
    assert mtime1 == mtime2


def test_structure_snapshot_recreation_on_file_modification(tmp_path):
    """Phase 11: Test that snapshot is recreated when file is modified externally."""
    content = """## Tasks
- [ ] **#1** Task 1
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    ops.read_tasks()
    snapshot1 = ops._structure_snapshot

    # Modify file externally (simulate user edit)
    import time

    time.sleep(0.1)  # Ensure mtime changes
    new_content = """## Tasks
- [ ] **#1** Task 1
- [ ] **#2** Task 2
"""
    todo_path.write_text(new_content, encoding="utf-8")

    # Read again - snapshot should be recreated
    tasks2 = ops.read_tasks()
    snapshot2 = ops._structure_snapshot

    # Snapshot should be different (recreated)
    assert snapshot1 is not snapshot2
    assert len(tasks2) == 2  # New task should be detected


def test_structure_snapshot_default_for_missing_file(tmp_path):
    """Phase 11: Test that default snapshot is created for non-existent files."""
    todo_path = tmp_path / "TODO.md"

    ops = FileOps(str(todo_path))
    ops.read_tasks()

    # Verify default snapshot was created
    assert ops._structure_snapshot is not None
    snapshot = ops._structure_snapshot

    # Verify default values
    assert snapshot.tasks_header_format == "## Tasks"
    assert snapshot.blank_after_tasks_header is True
    assert snapshot.blank_between_tasks is False
    assert snapshot.has_original_header is False
    assert len(snapshot.header_lines) == 0
    assert len(snapshot.footer_lines) == 0
    assert len(snapshot.interleaved_content) == 0


def test_generate_markdown_uses_snapshot(tmp_path):
    """Phase 12: Test that _generate_markdown uses snapshot when available."""
    content = """# Custom Header
> Warning

## Tasks
- [ ] **#1** Task 1
# Comment between tasks
- [ ] **#2** Task 2

------------------
**Footer**
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    # Verify snapshot was created
    assert ops._structure_snapshot is not None
    snapshot = ops._structure_snapshot

    # Generate markdown using snapshot
    generated = ops._generate_markdown(tasks, snapshot)

    # Verify custom header is preserved
    assert "# Custom Header" in generated
    assert "> Warning" in generated

    # Verify tasks section
    assert "## Tasks" in generated

    # Verify custom footer is preserved
    assert "**Footer**" in generated
    # Verify interleaved content is inserted
    assert "# Comment between tasks" in generated
    # Verify it appears between tasks
    lines = generated.splitlines()
    task1_idx = next(i for i, line in enumerate(lines) if "**#1**" in line)
    comment_idx = next(i for i, line in enumerate(lines) if "# Comment between tasks" in line)
    task2_idx = next(i for i, line in enumerate(lines) if "**#2**" in line)
    assert task1_idx < comment_idx < task2_idx


def test_generate_markdown_requires_snapshot(tmp_path):
    """Phase 13: Test that _generate_markdown requires snapshot (no fallback)."""
    content = """## Tasks
- [ ] **#1** Task 1
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    # Generate markdown without snapshot (None) - should raise ValueError
    with pytest.raises(ValueError, match="Structure snapshot must be available"):
        ops._generate_markdown(tasks, None)


def test_interleaved_content_insertion_in_generation(tmp_path):
    """Phase 12: Test that interleaved content is inserted during markdown generation."""
    content = """## Tasks
- [ ] **#1** Task 1
# User comment here
- [ ] **#2** Task 2
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    tasks = ops.read_tasks()

    # Verify snapshot has interleaved content
    assert ops._structure_snapshot is not None
    snapshot = ops._structure_snapshot
    assert "1" in snapshot.interleaved_content
    assert "# User comment here" in snapshot.interleaved_content["1"]

    # Generate markdown
    generated = ops._generate_markdown(tasks, snapshot)

    # Verify interleaved content appears in generated markdown
    lines = generated.splitlines()
    task1_line = next(i for i, line in enumerate(lines) if "**#1**" in line)
    comment_line = next(i for i, line in enumerate(lines) if "# User comment here" in line)
    task2_line = next(i for i, line in enumerate(lines) if "**#2**" in line)

    # Comment should be between task 1 and task 2
    assert task1_line < comment_line < task2_line


def test_interleaved_content_survives_read_write_cycle(tmp_path):
    """Phase 12: Test that interleaved content survives read/write cycle (task#163.46.7)."""
    content = """## Tasks
- [ ] **#1** Task 1
# User comment between tasks
- [ ] **#2** Task 2
# Another comment
- [ ] **#3** Task 3
"""
    todo_path = tmp_path / "TODO.md"
    todo_path.write_text(content, encoding="utf-8")

    ops = FileOps(str(todo_path))
    # Read tasks (captures snapshot with interleaved content)
    tasks = ops.read_tasks()

    # Verify interleaved content is in snapshot
    assert ops._structure_snapshot is not None
    snapshot = ops._structure_snapshot
    assert "1" in snapshot.interleaved_content
    assert "# User comment between tasks" in snapshot.interleaved_content["1"]
    assert "2" in snapshot.interleaved_content
    assert "# Another comment" in snapshot.interleaved_content["2"]

    # Write tasks back (should use snapshot to preserve interleaved content)
    ops.write_tasks(tasks)

    # Read again and verify interleaved content is still there
    ops2 = FileOps(str(todo_path))
    ops2.read_tasks()
    snapshot2 = ops2._structure_snapshot

    # Verify interleaved content survived
    assert "1" in snapshot2.interleaved_content
    assert "# User comment between tasks" in snapshot2.interleaved_content["1"]
    assert "2" in snapshot2.interleaved_content
    assert "# Another comment" in snapshot2.interleaved_content["2"]

    # Verify it's in the file content
    file_content = todo_path.read_text(encoding="utf-8")
    assert "# User comment between tasks" in file_content
    assert "# Another comment" in file_content


def test_file_structure_snapshot_immutability():
    """Phase 15: Test that FileStructureSnapshot is immutable (frozen dataclass)."""
    from dataclasses import FrozenInstanceError

    snapshot = FileStructureSnapshot(
        tasks_header_format="## Tasks",
        blank_after_tasks_header=True,
        blank_between_tasks=False,
        blank_after_tasks_section=False,
        header_lines=("Header line 1", "Header line 2"),
        footer_lines=("Footer line 1",),
        has_original_header=True,
        metadata_lines=("<!-- comment -->",),
        interleaved_content={"1": ("# Comment",)},
        original_task_order=(),
    )

    # Verify it's a frozen dataclass - cannot modify fields
    with pytest.raises(FrozenInstanceError):
        snapshot.tasks_header_format = "# Tasks"

    # Verify tuple fields are immutable (tuples don't have append, but test assignment)
    with pytest.raises(FrozenInstanceError):
        snapshot.header_lines = ("New line",)


def test_file_structure_snapshot_creation():
    """Phase 15: Test creating FileStructureSnapshot with various configurations."""
    # Minimal snapshot
    snapshot1 = FileStructureSnapshot(
        tasks_header_format="## Tasks",
        blank_after_tasks_header=False,
        blank_between_tasks=False,
        blank_after_tasks_section=False,
        header_lines=(),
        footer_lines=(),
        has_original_header=False,
        metadata_lines=(),
        interleaved_content={},
        original_task_order=(),
    )
    assert snapshot1.tasks_header_format == "## Tasks"
    assert snapshot1.blank_after_tasks_header is False
    assert len(snapshot1.header_lines) == 0

    # Full snapshot with all fields
    snapshot2 = FileStructureSnapshot(
        tasks_header_format="# Tasks",
        blank_after_tasks_header=True,
        blank_between_tasks=True,
        blank_after_tasks_section=True,
        header_lines=("Header 1", "Header 2"),
        footer_lines=("Footer 1",),
        has_original_header=True,
        metadata_lines=("Metadata 1",),
        interleaved_content={"1": ("Comment 1", "Comment 2"), "2": ("Comment 3",)},
        original_task_order=(),
    )
    assert snapshot2.tasks_header_format == "# Tasks"
    assert snapshot2.blank_after_tasks_header is True
    assert snapshot2.blank_between_tasks is True
    assert len(snapshot2.header_lines) == 2
    assert len(snapshot2.interleaved_content) == 2
    assert "1" in snapshot2.interleaved_content
    assert len(snapshot2.interleaved_content["1"]) == 2


def test_file_structure_snapshot_equality():
    """Phase 15: Test that FileStructureSnapshot equality works correctly."""
    snapshot1 = FileStructureSnapshot(
        tasks_header_format="## Tasks",
        blank_after_tasks_header=True,
        blank_between_tasks=False,
        blank_after_tasks_section=False,
        header_lines=(),
        footer_lines=(),
        has_original_header=False,
        metadata_lines=(),
        interleaved_content={},
        original_task_order=(),
    )

    snapshot2 = FileStructureSnapshot(
        tasks_header_format="## Tasks",
        blank_after_tasks_header=True,
        blank_between_tasks=False,
        blank_after_tasks_section=False,
        header_lines=(),
        footer_lines=(),
        has_original_header=False,
        metadata_lines=(),
        interleaved_content={},
        original_task_order=(),
    )

    snapshot3 = FileStructureSnapshot(
        tasks_header_format="## Tasks",
        blank_after_tasks_header=False,  # Different
        blank_between_tasks=False,
        blank_after_tasks_section=False,
        header_lines=(),
        footer_lines=(),
        has_original_header=False,
        metadata_lines=(),
        interleaved_content={},
        original_task_order=(),
    )

    assert snapshot1 == snapshot2  # Same values
    assert snapshot1 != snapshot3  # Different values


def test_file_structure_snapshot_interleaved_content():
    """Phase 15: Test FileStructureSnapshot interleaved_content field."""
    snapshot = FileStructureSnapshot(
        tasks_header_format="## Tasks",
        blank_after_tasks_header=False,
        blank_between_tasks=False,
        blank_after_tasks_section=False,
        header_lines=(),
        footer_lines=(),
        has_original_header=False,
        metadata_lines=(),
        interleaved_content={
            "1": ("# Comment for task 1", "  Additional note"),
            "2": ("# Comment for task 2",),
        },
        original_task_order=(),
    )

    assert "1" in snapshot.interleaved_content
    assert "2" in snapshot.interleaved_content
    assert len(snapshot.interleaved_content["1"]) == 2
    assert len(snapshot.interleaved_content["2"]) == 1
    assert "# Comment for task 1" in snapshot.interleaved_content["1"][0]
    assert "# Comment for task 2" in snapshot.interleaved_content["2"][0]
