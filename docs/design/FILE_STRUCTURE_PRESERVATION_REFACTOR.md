# Design: File Structure Preservation Refactor

**Created:** 2025-01-XX
**Status:** Proposed
**Version:** 1.0
**Related Task:** #163 (Python Refactor - Blank Line Preservation)

## Executive Summary

This document proposes a radical simplification of the file structure preservation logic in `todo_ai/core/file_ops.py`. The current implementation suffers from complex interdependencies between mutable state variables that modify each other in uncontrolled ways, making it difficult to debug and maintain. The proposed refactor introduces an **immutable structure snapshot** pattern that captures file formatting once and preserves it deterministically across all operations.

**Key Goals:**
- ✅ Eliminate mutable state interdependencies
- ✅ Simplify command implementations (remove special-case blank line handling)
- ✅ Make structure preservation explicit and debuggable
- ✅ Achieve 100% parity with shell script output
- ✅ Create scalable architecture for future structure elements

---

## Problem Statement

### Current Architecture Issues

The current implementation has several critical problems:

#### 1. **Dual Responsibility in FileOps**
`FileOps` class is responsible for both:
- **Parsing** file structure (blank lines, headers, footers)
- **Generating** entire file from Task objects

This creates a conflict: parsing captures structure, but generation must reconstruct it from mutable state that can be overwritten.

#### 2. **State Preservation Problems**

**Current State Variables:**
```python
self.tasks_header_has_blank_line: bool  # Mutable - can be overwritten
self.original_tasks_header_has_blank_line: bool  # Intended to be immutable, but...
self._blank_line_overridden: bool  # Temporary override flag
```

**Problems:**
- `original_tasks_header_has_blank_line` is set during parsing, but can be overwritten when `read_tasks()` is called again after file modifications
- `save_changes()` re-reads the file, potentially overwriting the "original" state with an intermediate modified state
- Multiple state variables create conflicts when commands override each other

#### 3. **Command Interdependencies**

**Current Flow:**
```python
def add_command(...):
    file_ops.read_tasks()  # Captures original state
    # ... add task ...
    file_ops.tasks_header_has_blank_line = False  # Override
    file_ops._blank_line_overridden = True
    file_ops.write_tasks(...)  # Uses override
    # Manual file editing to fix blank lines
    # Restore state for future operations
    file_ops.tasks_header_has_blank_line = file_ops.original_tasks_header_has_blank_line
```

**Problems:**
- Commands must know about structure preservation internals
- Manual file editing after `write_tasks()` (violates single responsibility)
- State restoration logic scattered across commands
- Commands interfere with each other's state

#### 4. **Fundamental Mismatch with Shell Script**

**Shell Script Approach:**
- Uses **targeted edits**: `sed` for replacements, `head/tail` for insertions
- Preserves existing file structure by only modifying specific lines
- Never regenerates the entire file
- Blank lines are preserved automatically (file is only modified at specific points)

**Python Current Approach:**
- Reads entire file into Task objects
- Regenerates entire file from Task objects via `_generate_markdown()`
- Tries to preserve blank lines through state variables
- State gets lost/reset when file is re-read

**Result:** Python must reconstruct structure that shell script preserves naturally.

---

## Proposed Solution: Immutable Structure Snapshot

### Core Principle

**Separate file structure preservation from task data management.**

Structure is captured **once** from the pristine file and stored in an **immutable snapshot**. This snapshot is used for all file generation, regardless of how many times the file is read or modified.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FileStructureSnapshot                     │
│                  (Immutable, Frozen Dataclass)              │
│                                                              │
│  - tasks_header_format: str                                  │
│  - blank_after_tasks_header: bool                           │
│  - blank_between_tasks: bool                                 │
│  - blank_after_tasks_section: bool                           │
│  - header_lines: tuple[str, ...]                             │
│  - footer_lines: tuple[str, ...]                             │
│                                                              │
│  Captured ONCE from pristine file, never modified           │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ used by
                          │
┌─────────────────────────────────────────────────────────────┐
│                        FileOps                               │
│                                                              │
│  - _structure_snapshot: FileStructureSnapshot | None         │
│                                                              │
│  read_tasks() -> list[Task]                                 │
│    - If snapshot is None: capture it ONCE                    │
│    - Parse tasks (can re-read multiple times)               │
│                                                              │
│  write_tasks(tasks: list[Task]) -> None                     │
│    - Use _structure_snapshot for generation                 │
│    - No mutable state needed                                │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ used by
                          │
┌─────────────────────────────────────────────────────────────┐
│                    Command Layer                             │
│                                                              │
│  save_changes()                                             │
│  add_command()                                              │
│  restore_command()                                          │
│  complete_command()                                         │
│  ...                                                        │
│                                                              │
│  - No special blank line handling                            │
│  - No manual file editing                                    │
│  - No state restoration                                      │
│  - Structure preserved automatically                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Detailed Design

### 1. FileStructureSnapshot (Immutable)

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FileStructureSnapshot:
    """Immutable snapshot of file structure captured from pristine file.

    This snapshot is captured ONCE when FileOps first reads a file, and
    is never modified, even if the file is re-read after modifications.
    This ensures consistent structure preservation across all operations.
    """
    # Tasks section header format
    tasks_header_format: str  # "# Tasks" or "## Tasks"

    # Blank line preservation
    blank_after_tasks_header: bool  # True if blank line after header
    blank_between_tasks: bool  # True if blank lines between tasks in Tasks section
    blank_after_tasks_section: bool  # True if blank line after Tasks (before other sections)

    # File sections
    header_lines: tuple[str, ...]  # Immutable tuple of header lines
    footer_lines: tuple[str, ...]  # Immutable tuple of footer lines

    # Metadata
    has_original_header: bool  # True if file had header before Tasks section
    metadata_lines: tuple[str, ...]  # HTML comments, relationships, etc.

    # Interleaved content (non-task lines in Tasks section)
    # Key: task_id (of preceding task), Value: tuple[str, ...] (lines of comments/whitespace)
    # Preserves user comments, notes, or other content between tasks
    # Note: Using dict[str, tuple] instead of list[str] for immutability (frozen dataclass requirement)
    # Alternative considered: Token Stream (list of Chunks: Task/Header/RawContent), but dict is simpler
    interleaved_content: dict[str, tuple[str, ...]]
```

**Key Properties:**
- **Immutable** (frozen dataclass) - cannot be modified after creation
- **Captured once** - set when FileOps first reads the file
- **Never overwritten** - even when file is re-read after modifications
- **Explicit** - all structure elements are visible in one place
- **Debuggable** - can inspect snapshot to see what structure will be used

### 2. FileOps (Simplified)

```python
class FileOps:
    """Handles file operations for TODO.md and .todo.ai directory."""

    def __init__(self, todo_path: str = "TODO.md"):
        self.todo_path = Path(todo_path)
        self.config_dir = self.todo_path.parent / ".todo.ai"
        self.serial_path = self.config_dir / ".todo.ai.serial"

        # Structure snapshot - captured once, never modified
        self._structure_snapshot: FileStructureSnapshot | None = None
        self._snapshot_mtime: float = 0.0  # File modification time when snapshot was captured
        # Used to detect external file modifications (e.g., user edits in editor)
        # If file mtime > snapshot_mtime, snapshot is stale and must be recaptured

        # Relationships (can change as tasks are modified)
        self.relationships: dict[str, dict[str, list[str]]] = {}
        self.deleted_task_formats: dict[str, str] = {}

        # Ensure config directory exists
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)

    def read_tasks(self) -> list[Task]:
        """Read tasks from TODO.md.

        On first call, captures structure snapshot from pristine file.
        Subsequent calls can re-read tasks, but snapshot remains unchanged.
        """
        if not self.todo_path.exists():
            # No file - use default structure
            self._structure_snapshot = self._create_default_snapshot()
            return []

        # Check if file was modified externally (e.g., by user in editor)
        # If so, invalidate snapshot and recapture
        current_mtime = self.todo_path.stat().st_mtime
        if self._structure_snapshot is None or current_mtime > self._snapshot_mtime:
            self._structure_snapshot = self._capture_structure_snapshot()
            self._snapshot_mtime = current_mtime

        # Parse tasks (can re-read multiple times, snapshot stays the same if file unchanged)
        return self._parse_tasks_only()

    def write_tasks(self, tasks: list[Task]) -> None:
        """Write tasks to TODO.md using preserved structure snapshot.

        If snapshot doesn't exist (shouldn't happen in normal flow),
        read_tasks() first to capture it.
        """
        if self._structure_snapshot is None:
            # Fallback: read once to get snapshot
            self.read_tasks()

        content = self._generate_markdown(tasks, self._structure_snapshot)
        self.todo_path.write_text(content, encoding="utf-8")

    def _capture_structure_snapshot(self) -> FileStructureSnapshot:
        """Capture structure snapshot from pristine file.

        This is called ONCE when FileOps first reads a file.
        The snapshot is immutable and never modified.
        """
        if not self.todo_path.exists():
            return self._create_default_snapshot()

        content = self.todo_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Parse structure elements
        header_lines = []
        footer_lines = []
        tasks_header_format = None
        blank_after_tasks_header = False
        blank_between_tasks = False
        blank_after_tasks_section = False
        has_original_header = False
        metadata_lines = []
        interleaved_content: dict[str, list[str]] = {}  # Will be converted to tuple

        # ... parsing logic to detect all structure elements ...
        # IMPORTANT: Capture non-task lines (comments, notes) between tasks
        # The parser must STOP discarding unknown lines to achieve 100% parity with sed-like behavior
        # Store them keyed by preceding task_id to preserve position
        # This ensures user comments like "# NOTE: Urgent" between tasks are preserved

        return FileStructureSnapshot(
            tasks_header_format=tasks_header_format or "## Tasks",
            blank_after_tasks_header=blank_after_tasks_header,
            blank_between_tasks=blank_between_tasks,
            blank_after_tasks_section=blank_after_tasks_section,
            header_lines=tuple(header_lines),
            footer_lines=tuple(footer_lines),
            has_original_header=has_original_header,
            metadata_lines=tuple(metadata_lines),
            interleaved_content={k: tuple(v) for k, v in interleaved_content.items()},
        )

    def _parse_tasks_only(self) -> list[Task]:
        """Parse only tasks from file (structure already captured).

        This can be called multiple times without affecting the snapshot.
        """
        if not self.todo_path.exists():
            return []

        content = self.todo_path.read_text(encoding="utf-8")
        # Parse tasks only (structure parsing skipped)
        return self._parse_tasks_from_content(content)

    def _generate_markdown(
        self,
        tasks: list[Task],
        snapshot: FileStructureSnapshot
    ) -> str:
        """Generate markdown using immutable structure snapshot.

        All structure decisions are based on the snapshot, not mutable state.
        """
        lines = []

        # 1. Header - use snapshot
        if snapshot.header_lines:
            lines.extend(snapshot.header_lines)
            if lines and lines[-1].strip() != "":
                lines.append("")
        elif snapshot.has_original_header:
            # Default header if file had one originally
            lines.extend([
                "# todo.ai ToDo List",
                "",
                "> **⚠️ IMPORTANT: This file should ONLY be edited through the `todo.ai` script!**",
                "",
            ])

        # 2. Tasks section - use snapshot
        lines.append(snapshot.tasks_header_format)
        if snapshot.blank_after_tasks_header and active_tasks:
            lines.append("")

        # 3. Tasks - use snapshot for blank lines between
        # Also insert interleaved content (comments, notes) after each task
        for i, task in enumerate(active_tasks):
            lines.append(format_task(task))
            # Insert interleaved content if any (preserves user comments/notes)
            if task.id in snapshot.interleaved_content:
                lines.extend(snapshot.interleaved_content[task.id])
            # Add blank line if snapshot indicates (normalized or original pattern)
            if snapshot.blank_between_tasks and i < len(active_tasks) - 1:
                lines.append("")

        # 4. Blank after Tasks section - use snapshot
        if snapshot.blank_after_tasks_section and active_tasks and (archived_tasks or deleted_tasks):
            lines.append("")

        # 5. Archived section
        if archived_tasks:
            lines.append("## Archived")
            # ... archived tasks ...

        # 6. Deleted section
        if deleted_tasks:
            lines.append("## Deleted")
            # ... deleted tasks ...

        # 7. Footer - use snapshot
        if snapshot.footer_lines:
            if lines and lines[-1].strip() != "":
                lines.append("")
            lines.extend(snapshot.footer_lines)

        return "\n".join(lines) + "\n"
```

**Key Changes:**
- Structure snapshot captured once and never overwritten
- `read_tasks()` can be called multiple times without losing structure
- `write_tasks()` uses snapshot, not mutable state
- No conditional logic based on override flags
- Deterministic output based on original file structure

### 3. Command Layer (Simplified)

```python
# Global cache for FileOps instances (preserves snapshot across commands)
_file_ops_cache: dict[str, FileOps] = {}

def save_changes(manager: TaskManager, todo_path: str = "TODO.md") -> None:
    """Save tasks - structure is automatically preserved via snapshot.

    No special state handling needed - snapshot is immutable.
    """
    file_ops = _file_ops_cache.get(todo_path)
    if file_ops is None:
        file_ops = FileOps(todo_path)
        file_ops.read_tasks()  # Captures snapshot
        _file_ops_cache[todo_path] = file_ops

    # No need to re-read or restore state - snapshot is immutable
    file_ops.write_tasks(manager.list_tasks())

def add_command(description: str, tags: list[str], todo_path: str = "TODO.md"):
    """Add a new task - no special blank line handling needed."""
    file_ops = _file_ops_cache.get(todo_path)
    if file_ops is None:
        file_ops = FileOps(todo_path)
        file_ops.read_tasks()  # Captures snapshot
        _file_ops_cache[todo_path] = file_ops

    tasks = file_ops.read_tasks()  # Snapshot already captured
    manager = TaskManager(tasks)

    # ... add task logic ...

    file_ops.write_tasks(manager.list_tasks())  # Uses snapshot automatically
    # No manual file editing needed!

def restore_command(task_id: str, todo_path: str = "TODO.md"):
    """Restore a deleted task - no special blank line handling needed."""
    file_ops = _file_ops_cache.get(todo_path)
    if file_ops is None:
        file_ops = FileOps(todo_path)
        file_ops.read_tasks()  # Captures snapshot
        _file_ops_cache[todo_path] = file_ops

    tasks = file_ops.read_tasks()
    manager = TaskManager(tasks)

    # ... restore task logic ...

    file_ops.write_tasks(manager.list_tasks())  # Uses snapshot automatically
    # No manual file editing needed!
```

**Key Changes:**
- No special blank-line handling in commands
- No manual file editing after `write_tasks()`
- No state restoration needed
- Commands are simpler and don't interfere with each other
- Structure preservation is automatic and transparent

---

## Benefits

### 1. **Immutable State**
- Structure captured once and never changes
- No risk of state being overwritten
- No conflicts between commands

### 2. **Separation of Concerns**
- **FileOps**: File I/O and structure preservation
- **Commands**: Task operations only
- No command-specific file editing

### 3. **Simpler Logic**
- No override flags (`_blank_line_overridden`)
- No state restoration (`tasks_header_has_blank_line = original_tasks_header_has_blank_line`)
- No manual file editing in commands
- Deterministic generation based on snapshot

### 4. **Easier Debugging**
- Structure is explicit (snapshot object)
- Can inspect snapshot to see what structure will be used
- No hidden state mutations
- Clear separation between structure and data

### 5. **Scalable**
- Easy to add new structure elements to snapshot
- Commands don't need to know about structure preservation
- New commands automatically preserve structure
- Future structure elements (e.g., custom sections) can be added without command changes

---

## Migration Strategy

### Phase 0: Enhanced Parsing (Pre-requisite)
1. Update `FileOps._parse_markdown()` to capture non-task lines in Tasks section
2. Store interleaved content (comments, notes) keyed by preceding task ID
3. Test that interleaved content survives read/write cycle
4. **Test:** Verify no data loss in files with user comments/notes

### Phase 1: Create Structure Snapshot (Non-Breaking)
1. Create `FileStructureSnapshot` dataclass with `interleaved_content` field
2. Add `_capture_structure_snapshot()` method to FileOps
3. Modify `_parse_markdown()` to populate snapshot including interleaved content
4. Store snapshot in FileOps with `_snapshot_mtime` tracking
5. **Test:** Verify existing tests still pass, verify interleaved content captured

### Phase 2: Use Snapshot for Generation (Non-Breaking)
1. Modify `_generate_markdown()` to accept snapshot parameter
2. Update `write_tasks()` to use snapshot
3. Implement mtime validation in `read_tasks()` to detect external modifications
4. Insert interleaved content during generation
5. Keep old state variables for now (dual mode)
6. **Test:** Verify existing tests still pass, test mtime invalidation

### Phase 3: Remove Old State Variables (Breaking)
1. Remove `tasks_header_has_blank_line`
2. Remove `original_tasks_header_has_blank_line`
3. Remove `_blank_line_overridden`
4. Remove all override logic from `_generate_markdown()`
5. **Test:** Run full test suite, fix any regressions

### Phase 4: Simplify Commands (Breaking)
1. Remove manual file editing from `add_command()`
2. Remove manual file editing from `restore_command()`
3. Remove state restoration logic from all commands
4. Remove `preserve_blank_line_state` parameter from `write_tasks()`
5. **Test:** Run full test suite, verify parity tests pass

### Phase 5: Cleanup
1. Remove unused methods and parameters
2. Update documentation
3. Add unit tests for `FileStructureSnapshot`
4. **Test:** Final validation with all parity tests

---

## Testing Strategy

### Unit Tests
- Test `FileStructureSnapshot` creation from various file formats
- Test snapshot immutability
- Test `_capture_structure_snapshot()` with different file structures
- Test `_generate_markdown()` with various snapshots

### Integration Tests
- Test that snapshot is captured once and never overwritten (unless file modified)
- Test that multiple `read_tasks()` calls don't affect snapshot (when file unchanged)
- Test that external file modifications invalidate snapshot (mtime check)
- Test that interleaved content is preserved across read/write cycles
- Test that commands preserve structure correctly
- Test MCP server with external file modifications

### Parity Tests
- Run all existing dataset parity tests
- Verify `test_workflow_sequence_with_dataset` passes
- Verify all 11/11 dataset parity tests pass
- Compare output with shell script for all operations

---

## Critical Considerations (From Recommendations)

### 1. Data Loss Risk (Parity Gap)
**Issue:** The shell script preserves *everything* via targeted edits (`sed`, `head`, `tail`). The Python implementation uses a **Parse → Model → Regenerate** cycle.

**Solution:** The snapshot must capture **interleaved content** (non-task lines) in the Tasks section. User comments, notes, or other content between tasks must be preserved.

**Implementation:** Added `interleaved_content: dict[str, tuple[str, ...]]` to `FileStructureSnapshot` to store non-task lines keyed by preceding task ID.

### 2. Stale State in Long-Running Processes
**Issue:** The global `_file_ops_cache` assumes short-lived CLI environment, but MCP server is persistent.

**Solution:** Implement modification time (`mtime`) validation. If file is modified externally (e.g., by user in editor), invalidate and recapture snapshot.

**Implementation:** Added `_snapshot_mtime` to `FileOps` and check `current_mtime > self._snapshot_mtime` before using cached snapshot.

### 3. Normalization vs. Preservation
**Issue:** Boolean flags (e.g., `blank_between_tasks`) imply uniform formatting, but real files may be inconsistent.

**Decision:** Adopt **Smart Normalization** as default behavior:
- If inconsistent blank lines detected during parsing, use *dominant* pattern
- **Threshold:** If >50% of task pairs have blank lines between them, enforce blank lines for all
- If <50% have blank lines, enforce no blank lines for all (normalize to majority)
- Document as known deviation from strict parity (acceptable trade-off for file health)
- Shell script preserves inconsistencies; Python normalizes for maintainability
- This ensures files become cleaner over time while maintaining reasonable parity

## Risk Assessment

### Low Risk
- **Snapshot creation**: Well-defined parsing logic
- **Immutable dataclass**: Standard Python pattern
- **Command simplification**: Removing code, not adding complexity
- **Mtime validation**: Standard file system pattern

### Medium Risk
- **Structure detection**: Must correctly identify all structure elements
- **Interleaved content parsing**: Must capture all non-task lines without losing context
- **Edge cases**: Files with unusual formatting or inconsistent spacing
- **Backward compatibility**: Ensure existing files work correctly
- **MCP server cache invalidation**: Must handle concurrent modifications correctly

### High Risk
- **Data loss**: If interleaved content parsing is incomplete, user comments/notes will be lost
- **Stale snapshot**: If mtime check fails, MCP server may overwrite user edits

### Mitigation
- Comprehensive test coverage before migration
- Gradual migration (phases 1-2 are non-breaking)
- Keep old code until new code is validated
- Extensive parity testing with files containing interleaved content
- Test MCP server with external file modifications
- Add explicit tests for interleaved content preservation

---

## Future Enhancements

### Additional Structure Elements
The snapshot pattern makes it easy to add new structure elements:

```python
@dataclass(frozen=True)
class FileStructureSnapshot:
    # ... existing fields ...

    # Future additions
    blank_before_archived: bool
    blank_before_deleted: bool
    custom_sections: tuple[str, ...]  # User-defined sections
    section_order: tuple[str, ...]  # Order of sections
```

### Structure Validation
Add validation to ensure snapshot matches file:

```python
def validate_snapshot(self, snapshot: FileStructureSnapshot) -> bool:
    """Verify that snapshot still matches current file structure."""
    current_snapshot = self._capture_structure_snapshot()
    return snapshot == current_snapshot
```

### Structure Migration
Support migrating structure between formats:

```python
def migrate_snapshot(
    self,
    old_snapshot: FileStructureSnapshot,
    new_format: str
) -> FileStructureSnapshot:
    """Migrate snapshot to new format."""
    # ... migration logic ...
```

---

## Conclusion

This refactor eliminates the complex interdependencies in the current implementation by introducing an immutable structure snapshot pattern. The new architecture is:

- **Simpler**: No override flags, no state restoration, no manual file editing
- **More maintainable**: Clear separation of concerns, explicit structure
- **Easier to debug**: Structure is visible in snapshot object
- **Scalable**: Easy to add new structure elements
- **Reliable**: Immutable state prevents corruption

The migration can be done gradually with minimal risk, and the new architecture will make it much easier to achieve and maintain 100% parity with the shell script output.

---

## References

- Current implementation: `todo_ai/core/file_ops.py`
- Command implementations: `todo_ai/cli/commands/__init__.py`
- Parity tests: `tests/validation/test_dataset_parity.py`
- Shell script reference: `todo.ai` (lines 2043-2057 for `add`, 3361-3377 for `restore`)
- Recommendations: `docs/design/FILE_STRUCTURE_REFACTOR_RECOMMENDATIONS.md`
- MCP server: `todo_ai/mcp/server.py`
