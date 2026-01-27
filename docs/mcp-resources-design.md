# MCP Resources Design Document

**Task:** #262 - Expose task lists as MCP resources for IDE integration
**Status:** APPROVED - Option A selected
**Date:** 2026-01-27
**GitHub Issue:** #48
**Decision:** Option A (Minimal Set) with Approach 1 (built-in notifications)

## Executive Summary

Add MCP resources to the ai-todo server to expose task data as subscribable, read-only endpoints. This enables live task panels, resource subscriptions, efficient caching, and better multi-agent synchronization.

## Research Findings

### FastMCP Resource Capabilities

FastMCP supports resources via the `@mcp.resource()` decorator:

```python
@mcp.resource("tasks://open")
def get_open_tasks() -> str:
    """Returns JSON list of open tasks."""
    return json.dumps(tasks)
```

**Key Features:**
- URI-based addressing (`scheme://path` or `scheme://path/{param}`)
- Dynamic templates with `{parameter}` placeholders
- Automatic `list_changed` notifications when resources are added/removed
- Return types: `str`, `bytes`, or `ResourceResult` for full control
- Async support for I/O-bound operations
- MIME type specification (default: `text/plain`, we'll use `application/json`)

### Current Server State

| Component | Count | Notes |
|-----------|-------|-------|
| Tools | 28 | All task operations |
| Prompts | 1 | `active_context` |
| Resources | 0 | **Gap to address** |

## Proposed Resource Schema

### Option A: Minimal Set (Recommended)

Focus on the most useful resources with clear separation of concerns.

| Resource URI | Description | MIME Type |
|--------------|-------------|-----------|
| `tasks://open` | All open tasks (pending + in-progress) | `application/json` |
| `tasks://active` | Currently active tasks (#inprogress) | `application/json` |
| `tasks://{id}` | Single task details with subtasks | `application/json` |
| `config://settings` | Current ai-todo configuration | `application/json` |

**Rationale:**
- `tasks://open` is the primary "what should I work on" view
- `tasks://active` is the "what am I currently doing" view (mirrors existing `get_active_tasks` tool)
- `tasks://{id}` enables drill-down into specific tasks
- `config://settings` exposes configuration for context

### Option B: Extended Set

Includes additional resources for comprehensive coverage.

| Resource URI | Description | MIME Type |
|--------------|-------------|-----------|
| `tasks://open` | All open tasks (pending + in-progress) | `application/json` |
| `tasks://active` | Currently active tasks (#inprogress) | `application/json` |
| `tasks://pending` | Pending tasks only (not started) | `application/json` |
| `tasks://completed` | Recently completed tasks | `application/json` |
| `tasks://archived` | Archived tasks | `application/json` |
| `tasks://{id}` | Single task details | `application/json` |
| `config://settings` | ai-todo configuration | `application/json` |
| `stats://summary` | Task statistics (counts by status) | `application/json` |

**Trade-off:** More comprehensive but may be overkill for initial implementation.

### Option C: Full Parity with Tools

Mirror every list-like tool as a resource.

**Trade-off:** Maximum coverage but blurs the line between tools (actions) and resources (observations).

## JSON Data Structures

### Task Object

```json
{
  "id": "262",
  "description": "Implement MCP resources",
  "status": "pending",
  "tags": ["enhancement", "mcp"],
  "notes": ["Research FastMCP patterns"],
  "is_subtask": false,
  "subtask_count": 3,
  "created_at": "2026-01-27T23:08:44Z",
  "updated_at": "2026-01-27T23:08:44Z",
  "completed_at": null
}
```

### Task List Response

```json
{
  "tasks": [
    { "id": "262", "description": "...", ... },
    { "id": "51", "description": "...", ... }
  ],
  "count": 2,
  "filter": "open",
  "timestamp": "2026-01-27T23:15:00Z"
}
```

### Single Task Response (tasks://{id})

```json
{
  "task": {
    "id": "262",
    "description": "GitHub Issue #48: Expose task lists as MCP resources",
    "status": "pending",
    "tags": ["enhancement", "github-issue", "mcp", "v3.1"],
    "notes": ["Add MCP resources to expose task data..."],
    "is_subtask": false
  },
  "subtasks": [
    { "id": "262.1", "description": "Investigate...", "status": "completed", ... },
    { "id": "262.2", "description": "Analyze...", "status": "completed", ... }
  ],
  "relationships": {
    "depends-on": [],
    "blocks": []
  },
  "timestamp": "2026-01-27T23:15:00Z"
}
```

### Config Response

```json
{
  "numbering": {
    "mode": "single-user",
    "next_id": 263
  },
  "security": {
    "tamper_proof": true
  },
  "coordination": {
    "enabled": false,
    "type": null
  },
  "timestamp": "2026-01-27T23:15:00Z"
}
```

## Change Notification Strategy

### Approach 1: Rely on Built-in Notifications (Recommended)

FastMCP automatically sends `notifications/resources/list_changed` when resources are modified via `mcp.add_resource()` or `mcp.disable()`/`mcp.enable()`.

For content changes within existing resources (e.g., task added), clients should:
1. Subscribe to the resource
2. Re-fetch when they need fresh data (pull-based)

**Pros:** Simple, no custom notification code needed
**Cons:** No push notifications for content changes

### Approach 2: Manual Content Change Notifications

Call `mcp.notify_resource_changed(uri)` after task mutations.

```python
@mcp.tool()
def add_task(title: str, ...) -> str:
    result = _capture_output(add_command, ...)
    # Notify clients that task lists changed
    mcp.notify_resource_list_changed()  # Or specific resource
    return result
```

**Pros:** Real-time updates
**Cons:** Need to add notification calls to every mutating tool

### Recommendation

Start with **Approach 1** (built-in only). Most MCP clients (including Cursor) poll resources when needed rather than expecting push notifications. We can add Approach 2 later if real-time updates become a requirement.

## Implementation Plan

### Phase 1: Core Resources

1. Add `tasks://open` resource (pending + in-progress tasks)
2. Add `tasks://active` resource (in-progress only)
3. Add `tasks://{id}` dynamic resource template
4. Add `config://settings` resource

### Phase 2: Change Notifications (Optional)

1. Add `notify_resource_list_changed()` calls to mutating tools
2. Test subscription behavior with MCP Inspector

### Phase 3: Extended Resources (Optional)

1. Add `tasks://completed`, `tasks://archived` if needed
2. Add `stats://summary` if requested

## Code Location

All resource implementations will be added to `ai_todo/mcp/server.py` alongside existing tools and prompts.

## Open Questions

1. Should `tasks://open` include subtasks inline or only root tasks?
   - **Recommendation:** Root tasks only with `subtask_count` field
2. Should timestamps be ISO 8601 or Unix epoch?
   - **Recommendation:** ISO 8601 for human readability
3. How many tasks to include in list resources (pagination)?
   - **Recommendation:** All tasks initially, add `{?limit,offset}` query params later if needed

---

**APPROVED:** Option A - Minimal Set with built-in notifications (2026-01-27)
