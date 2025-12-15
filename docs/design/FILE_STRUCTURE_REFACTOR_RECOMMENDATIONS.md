# Recommendations: File Structure Preservation Refactor

**Date:** 2025-12-15
**Status:** Recommendations Addressed
**Related Proposal:** [FILE_STRUCTURE_PRESERVATION_REFACTOR.md](./FILE_STRUCTURE_PRESERVATION_REFACTOR.md)

## Executive Summary

The proposal to introduce an **Immutable Structure Snapshot** pattern is a significant architectural improvement that solves the complexity of mutable state management in `FileOps`. However, an assessment of the current codebase and `FileOps` implementation reveals critical gaps that would lead to **data loss** and **inconsistency** with the legacy shell script if implemented as described.

This document outlines these findings and provides specific recommendations to address them before implementation begins.

---

## Critical Findings

### 1. Data Loss Risk (Parity Gap)
**Issue:** The legacy shell script uses `sed`, `head`, and `tail` for modifications. These tools preserve *everything* in the file except the specific lines being targeted. The Python implementation uses a **Parse → Model → Regenerate** cycle.

**Current Gap:** The `FileOps` parser currently discards any content within the "Tasks" section that does not match a specific pattern (Header, Task, or Metadata).
*   **Scenario:** A user adds a comment `# NOTE: Urgent` between two tasks in `TODO.md`.
*   **Shell Script:** Preserves the comment because it only touches the task lines.
*   **Proposed Python Refactor:** The parser ignores the comment line. The `FileStructureSnapshot` captures formatting *rules* but not content. When `write_tasks()` regenerates the file, the comment is permanently deleted.

### 2. Stale State in Long-Running Processes
**Issue:** The proposal introduces a global `_file_ops_cache` to persist the snapshot across commands. This assumes a short-lived CLI environment.

**Current Gap:** The project includes a persistent **MCP Server** (`todo_ai/mcp/server.py`).
*   **Scenario:** The MCP server is running. A user manually edits `TODO.md` in their editor (e.g., changes the header from `# Tasks` to `## My Tasks`).
*   **Impact:** The cached `FileOps` instance in the MCP server holds a stale snapshot. The next write operation by the MCP server will revert the user's manual changes to match the stale snapshot.

### 3. Normalization vs. Preservation
**Issue:** The snapshot uses boolean flags (e.g., `blank_between_tasks`) which imply a uniform rule for the entire file.

**Current Gap:** Real-world files often have inconsistent formatting (e.g., a blank line between the first two tasks, but not subsequent ones).
*   **Impact:** The snapshot approach forces normalization (uniform spacing) upon the first write. While this creates cleaner files, it is a deviation from strict parity with the shell script, which preserves inconsistencies.

---

## Recommendations

### 1. Enhanced "Interleaved" Parser
To achieve 100% parity with `sed`-like behavior, the parser must stop discarding unknown lines.

**Recommendation:**
Refactor the `Task` model or the parsing logic to capture "Interleaved Content".

*   **Option A (Task Attachment):** Attach non-task lines to the preceding task object as `trailing_content`.
*   **Option B (Token Stream - Preferred):** Maintain a list of "Chunks" where a Chunk can be a `Task`, a `Header`, or `RawContent`.

**Revised Structure:**
```python
@dataclass
class FileStructureSnapshot:
    # ... existing fields ...

    # New: Map of "inter-task" content to preserve position
    # Key: task_id (of preceding task), Value: list[str] (lines of comments/whitespace)
    interleaved_content: dict[str, list[str]]
```

### 2. Cache Invalidation Strategy
The cache must be aware of external file modifications.

**Recommendation:**
Implement a modification time (`mtime`) check before using any cached snapshot.

```python
class FileOps:
    def __init__(self, path):
        self.snapshot_mtime = 0
        self.snapshot = None

    def read_tasks(self):
        current_mtime = self.todo_path.stat().st_mtime
        if self.snapshot is None or current_mtime > self.snapshot_mtime:
            self.snapshot = self._capture_structure_snapshot()
            self.snapshot_mtime = current_mtime
        # ... proceed with parsing ...
```

### 3. Explicit Normalization Decision
The team must decide between "Strict Preservation" and "Smart Normalization".

**Recommendation:**
Adopt **Smart Normalization** as the default behavior, but document it as a known deviation.
*   The "Snapshot" approach is superior for maintaining file health over time compared to `sed`.
*   If inconsistent blank lines are detected during parsing, the snapshot should opt for the *dominant* pattern (e.g., if >50% of tasks have blank lines, enforce it for all).

---

## Revised Architecture Plan

1.  **Phase 1: Robust Parsing (Pre-requisite)**
    *   Update `FileOps._parse_markdown` to capture non-task lines in the Tasks section instead of discarding them.
    *   Store these lines in a temporary structure to ensure they survive a read/write cycle.

2.  **Phase 2: Immutable Snapshot with Validation**
    *   Implement `FileStructureSnapshot` as proposed.
    *   Add `interleaved_content` storage to the snapshot.
    *   Implement `mtime` validation in the `FileOps` cache.

3.  **Phase 3: Migration**
    *   Proceed with the proposed removal of mutable state variables.
