import pytest

from todo_ai.core.file_ops import FileOps
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
