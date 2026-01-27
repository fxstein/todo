# Task Metadata Persistence Design

**Task:** #263 - Design task metadata persistence for timestamps
**Status:** APPROVED - Hybrid Approach with Lazy Backfilling
**Date:** 2026-01-27
**Decision:** Option C (HTML comments) + inline completion dates. No migration scripts - lazy backfill on task mutations.

## Problem Statement

MCP resources exposed that task timestamps (`created_at`, `updated_at`, `completed_at`) are not being persisted. Currently:

- `created_at` and `updated_at` are generated fresh at parse-time using `datetime.now()`
- These timestamps are nearly identical (1 microsecond apart) because they're set during Task construction
- Historical data about when tasks were created/modified is lost between sessions

### Current Timestamp Handling

| Field | Persisted? | Current Behavior |
|-------|------------|------------------|
| `created_at` | No | Generated at parse-time |
| `updated_at` | No | Generated at parse-time |
| `completed_at` | Partial | Date only `(YYYY-MM-DD)` for completed tasks |
| `archived_at` | Yes | Date from markdown `(YYYY-MM-DD)` |
| `deleted_at` | Yes | Full format `(deleted YYYY-MM-DD, expires YYYY-MM-DD)` |
| `expires_at` | Yes | Full format with deleted_at |

---

## Storage Options

### Option A: Inline Markdown (Extend Current Pattern)

Extend the existing inline date pattern to include all timestamps.

**Format:**
```markdown
- [ ] **#1** Task description `#tag` (created 2026-01-15)
- [x] **#2** Completed task `#tag` (created 2026-01-10, completed 2026-01-20)
```

**Pros:**
- Human-readable in plain markdown
- Consistent with existing deletion metadata pattern
- No extra files or sections needed
- Git-friendly (changes visible in diffs)

**Cons:**
- Clutters task lines significantly
- Only date precision (no time)
- Parsing becomes complex with multiple optional fields
- `updated_at` would add visual noise for every edit

**Recommendation:** Not suitable for `updated_at` due to visual noise.

---

### Option B: Separate Metadata File

Store timestamps in a separate JSON file in the state directory.

**Location:** `.ai-todo/state/metadata.json`

**Format:**
```json
{
  "version": 1,
  "tasks": {
    "1": {
      "created_at": "2026-01-15T10:30:00.000000",
      "updated_at": "2026-01-20T14:45:30.123456"
    },
    "2": {
      "created_at": "2026-01-10T09:00:00.000000",
      "updated_at": "2026-01-20T16:00:00.000000",
      "completed_at": "2026-01-20T16:00:00.000000"
    }
  }
}
```

**Pros:**
- Doesn't clutter TODO.md
- Full timestamp precision (microseconds)
- Easy to extend with additional metadata
- Clean separation of concerns
- Fast JSON parsing

**Cons:**
- Extra file to maintain
- Risk of metadata getting out of sync with TODO.md
- State directory is in `.cursorignore` (agents can't read it)
- Not visible in TODO.md for human review

**Recommendation:** Good for internal tooling, but sync risk is significant.

---

### Option C: Hidden HTML Comments in TODO.md (Recommended)

Store timestamps in an HTML comment block at the bottom of TODO.md, similar to TASK RELATIONSHIPS.

**Location:** Bottom of TODO.md in metadata section

**Format:**
```markdown
<!-- TASK_TIMESTAMPS
1:2026-01-15T10:30:00
2:2026-01-10T09:00:00:2026-01-20T16:00:00
-->
```

Compact line format: `task_id:created_at[:updated_at[:completed_at]]`

**Pros:**
- Single source of truth (stays in TODO.md)
- Doesn't visually clutter task lines
- Full timestamp precision
- Git-tracked and visible in diffs
- Follows existing pattern (TASK RELATIONSHIPS uses HTML comments)
- Human-readable if needed

**Cons:**
- Adds parsing complexity
- File size grows with task count
- Comment block could become large for many tasks

**Recommendation:** Best balance of persistence, visibility, and cleanliness.

---

## Recommendation: Hybrid Approach (Option C + Inline for Key Dates)

**Selected Approach:**

1. **Keep inline dates** for `completed_at` on completed tasks (human-readable status)
2. **Add HTML comment block** for `created_at` and `updated_at` (hidden but tracked)
3. **Don't persist `updated_at` for every change** - only track last significant update

### Proposed Format

**Inline (visible):**
```markdown
- [ ] **#1** Task description `#tag`
- [x] **#2** Completed task `#tag` (2026-01-20)
```

**Hidden comment block:**
```markdown
<!-- TASK_METADATA
# Format: task_id:created_at[:updated_at]
# Timestamps in ISO 8601 format (UTC)
1:2026-01-15T10:30:00Z
2:2026-01-10T09:00:00Z:2026-01-20T16:00:00Z
263:2026-01-27T23:27:00Z
-->
```

### Update Rules

1. **`created_at`**: Set once when task is created, never changes
2. **`updated_at`**: Updated on meaningful changes:
   - Description modified
   - Tags added/removed
   - Status changed
   - Notes added/modified
   - **Not updated** on: Read operations, list operations
3. **`completed_at`**: Set when task marked complete (also shown inline)

### Lazy Backfill Strategy (No Migration Scripts)

Instead of running a migration, timestamps are backfilled lazily when tasks are touched:

**On task mutation (add, modify, archive, delete, complete):**

1. **If task has no `created_at` in metadata:**
   - Use earliest available date from task (completion/archive/deletion date)
   - If no date available, use current time
   - Write to metadata block

2. **Always update `updated_at`** to current time on any mutation

3. **Untouched tasks remain without metadata** until they are modified

**Benefits:**
- No migration script needed
- Gradual, natural backfill as users work
- No risk of corrupting existing data
- Simpler implementation

**Tradeoff:**
- Old untouched tasks show current time as `created_at` until modified
- MCP resources may show inconsistent timestamps for old tasks (acceptable)

---

## Implementation Plan

### Phase 1: Parser Updates
1. Add parsing for `<!-- TASK_METADATA ... -->` block
2. Populate Task.created_at and Task.updated_at from parsed data
3. Fallback to datetime.now() if no stored metadata (current behavior)

### Phase 2: Writer Updates
1. Generate TASK_METADATA comment block on write
2. On mutation: backfill `created_at` if missing, always update `updated_at`
3. Preserve existing timestamps for unchanged tasks

### Phase 3: Testing
1. Unit tests for parsing/writing metadata
2. Integration tests for timestamp persistence across sessions
3. Tests for lazy backfill behavior

---

**APPROVED:** Hybrid Approach (Option C + inline dates) with lazy backfilling (2026-01-27)
