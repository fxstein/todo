# Linear Integration Assessment

**Task:** #266.1 — Assessment: document current Linear setup & MCP audit
**Date:** 2026-01-28
**Scope:** fxstein Linear workspace, ai-todo GitHub repo, Cursor rules, and Linear MCP tool payloads.

---

## 1. Current Configuration Inventory

### 1.1 Linear Workspace (fxstein)

| Item | Status |
|------|--------|
| Workspace | **fxstein** (accessible via Linear MCP) |
| Teams | **ai-todo** (id: `6e5ad3a4-ca85-4717-a40b-425d361e5191`), **Fxstein** (id: `78310e05-6a9c-4ea7-b500-1bfbad5e9b11`) |
| Current user (MCP `get_user` "me") | fxstein; id: `dfec2470-d1d9-4c0a-bf49-611340a53e84` |
| Cycles | `list_cycles` for team ai-todo returned `[]` — no cycles configured for that team, or not exposed in the same way |
| Sample issue | AIT-1 (Test Issue) — team ai-todo, has GitHub attachment (#50) |

### 1.2 Cursor / MCP

| Item | Status |
|------|--------|
| `.cursor/mcp.json` | Only **ai-todo** server defined (project-level). Linear MCP is assumed to be configured at **user** level (e.g. `user-linear`). |
| Cursor rule | `.cursor/rules/linear-ai-todo-integration.mdc` — describes Linear (macro) + ai-todo (micro) kickoff/closing workflow |
| Rule references | Uses `user-linear.get_viewer()` and `user-linear.get_issues({ assignee_id: <user_id> })` — **see gaps below** |

### 1.3 GitHub (ai-todo repo)

| Item | Status |
|------|--------|
| Repo | fxstein/ai-todo (branching, PRs to `main`) |
| Workflows | `.github/workflows/ci-cd.yml` — push to main, tags `v*`, pull_request to main. **No Linear-specific steps or secrets.** |
| Issue template | `.github/ISSUE_TEMPLATE/bug_report.yml` — standard bug form. **No Linear issue ID or link.** |
| Branch/PR rules | No branch naming or PR title conventions tied to Linear in repo config (no branch name in PR title requirement, etc.). |

---

## 2. MCP Tool Payload Verification (CRITICAL)

The following tools were **actually run** to capture real responses.

### 2.1 Tools used

- **user-linear.get_user** — `query: "me"` → current user
- **user-linear.list_issues** — `assignee: "me"`, and unfiltered `limit: 10` → list of issues
- **user-linear.get_issue** — `id: "<issue-uuid>"`, `includeRelations: true` → single issue detail
- **user-linear.list_teams** — → teams in workspace
- **user-linear.list_cycles** — `teamId: "<ai-todo-team-id>"` → cycles for team

### 2.2 Do we get the branch name?

**Yes.** Both `list_issues` and `get_issue` return **`gitBranchName`**.

- Example (AIT-1): `"gitBranchName": "fxstein/ait-1-test-issue"`
- Format in sample data: `{displayName}/{identifier-kebab-title}` (e.g. `fxstein/ait-1-test-issue`, `fxstein/fxs-3-connect-your-tools`).

So we **can** automate branch creation/linking from the issue payload.

### 2.3 Do we get the cycle?

**No, not in the issue payload.**

- **list_issues** accepts a filter `cycle` (name, number, or ID), but the **issue object** in the response does **not** include a `cycle` or `cycleId` field.
- **get_issue** response also does **not** include cycle.
- **list_cycles** exists and takes `teamId`; for the ai-todo team it returned `[]` (no cycles or not configured).

So for automation we **cannot** read “which cycle this issue is in” from the issue response. We can only filter issues by cycle when listing.

### 2.4 Do we get the assignee?

**No, not in the issue payload.**

- **list_issues** accepts `assignee` (e.g. `"me"`, user ID, name, email) and filters correctly (e.g. `assignee: "me"` returns only my issues; in our run it returned `[]` because no issues were assigned to me).
- The **issue objects** returned by **list_issues** and **get_issue** do **not** include `assignee`, `assigneeId`, or `assigneeName`.

So we **cannot** read “who is assigned” from the issue response for automation. We can only filter by assignee when listing.

---

## 3. Raw JSON: MCP Issue Response (for automation)

Below is the **exact** structure returned by **user-linear.get_issue** for one issue (AIT-1), so we know what we can rely on for automation.

```json
{
  "id": "9d8c7da7-a7b0-4ed7-ae0a-ad7afce10b43",
  "identifier": "AIT-1",
  "title": "Test Issue",
  "description": "Testing Integration",
  "url": "https://linear.app/fxstein/issue/AIT-1/test-issue",
  "gitBranchName": "fxstein/ait-1-test-issue",
  "createdAt": "2026-01-28T18:49:15.000Z",
  "updatedAt": "2026-01-28T18:50:55.390Z",
  "status": "Backlog",
  "labels": [],
  "attachments": [
    {
      "id": "5cce54a8-024c-4c59-a4d1-ca2852e132ac",
      "title": "#50 Test Issue",
      "url": "https://github.com/fxstein/ai-todo/issues/50"
    }
  ],
  "documents": [],
  "createdBy": "fxstein",
  "createdById": "dfec2470-d1d9-4c0a-bf49-611340a53e84",
  "team": "ai-todo",
  "teamId": "6e5ad3a4-ca85-4717-a40b-425d361e5191",
  "relations": {
    "blocks": [],
    "blockedBy": [],
    "relatedTo": [],
    "duplicateOf": null
  }
}
```

**list_issues** returns an object `{ "issues": [ ... ], "hasNextPage": false }` where each element of `issues` has the **same shape** as above (no `relations` unless you used a different endpoint; in our run each issue had the same fields as above, with truncated descriptions in some cases).

### Fields we can use for automation

| Field | Present | Use |
|-------|--------|-----|
| `id` | Yes | Stable UUID for API calls (get_issue, update_issue). |
| `identifier` | Yes | Human-readable ID (e.g. AIT-1) for branch names, PR titles, commit refs. |
| `title` | Yes | Display and PR title. |
| `description` | Yes | Requirements / body. |
| `url` | Yes | Deep link to Linear. |
| **`gitBranchName`** | **Yes** | **Branch naming automation.** |
| `status` | Yes | State (e.g. Backlog, Todo) for workflow. |
| `team`, `teamId` | Yes | Mapping to repos/releases if needed. |
| `createdBy`, `createdById` | Yes | Author. |
| `labels` | Yes | Tags/categories. |
| `attachments` | Yes | e.g. GitHub issue links. |
| `relations` | Yes (get_issue) | Blocking/related/duplicate. |
| **`assignee` / `assigneeId`** | **No** | Cannot read assignee from payload. |
| **`cycle` / `cycleId`** | **No** | Cannot read cycle from payload. |

---

## 4. What Is Working

- **Linear MCP** is usable: get_user, list_issues, get_issue, list_teams, list_cycles, update_issue, etc.
- **Branch name** is available: `gitBranchName` in both list_issues and get_issue — sufficient for branch naming and PR automation.
- **IDs and status**: `id`, `identifier`, `status`, `team`, `teamId` are present — enough to drive “life of a ticket” flows (e.g. branch from identifier, update status via update_issue).
- **GitHub ↔ Linear link**: AIT-1 has an attachment pointing to GitHub issue #50 — manual or existing integration works; no automation in repo yet.
- **Cursor rule** exists and describes the intended Linear + ai-todo workflow (kickoff, plan, close).

---

## 5. What Is Missing or Wrong

### 5.1 MCP payload gaps (for automation)

- **Assignee**: Not in issue payload. We can filter by assignee in list_issues but cannot “show assignee” or “verify assignee” from get_issue/list_issues response. If the Linear MCP or API can be extended to return assignee on the issue, that would unblock assignee-based automation.
- **Cycle**: Not in issue payload. We can filter list_issues by cycle and use list_cycles(teamId), but we cannot read “this issue’s cycle” from the issue object. Cycle-based automation would require either a different API/MCP shape or inferring from list_issues(cycle=...).

### 5.2 Cursor rule vs actual API

- Rule says **`user-linear.get_viewer()`** — there is no `get_viewer` tool. Use **`get_user`** with **`query: "me"`** to get the current user.
- Rule says **`user-linear.get_issues({ assignee_id: <user_id> })`** — the actual tool is **`list_issues`** with **`assignee: "me"`** (or assignee by user ID/name/email). Parameter name is `assignee`, not `assignee_id`, and "me" is supported.
- **update_issue**: Rule says `linear.update_issue(id="AIT-204", status="In Review")`. Actual tool is **`update_issue`** with **`id`** (UUID or identifier?) and **`state`** (not `status`). Need to confirm whether `id` accepts identifier like "AIT-204" or only UUID; and use **`state`** for status.

### 5.3 GitHub integration

- No Linear issue ID or branch name in PR title/branch checks in GitHub (Actions or branch rules).
- No GitHub Actions step that links PRs to Linear (e.g. comment with branch name or transition status).
- No repo-level convention doc for “branch name = Linear ID + description” or “PR title must include Linear identifier”.

### 5.4 Secrets and config

- No Linear-related secrets in `.github/workflows/ci-cd.yml`. If we want Actions to update Linear (e.g. on merge), we would need a Linear API key or similar in GitHub secrets.
- Linear MCP is not in project `mcp.json` (only ai-todo); it’s user-level. That’s fine for Cursor but should be documented so new devs know how to get “Linear + ai-todo” in one environment.

---

## 6. Summary Table

| Capability | Working | Missing / Note |
|------------|--------|----------------|
| Get current user | Yes (`get_user("me")`) | Rule references non-existent `get_viewer()` |
| List my issues | Yes (`list_issues(assignee: "me")`) | Rule uses wrong tool/param name |
| Get single issue | Yes (`get_issue(id)`) | — |
| Branch name in payload | Yes (`gitBranchName`) | — |
| Cycle in payload | No | Only filter on list; list_cycles(teamId) returned [] for ai-todo |
| Assignee in payload | No | Only filter on list |
| Update issue (e.g. status) | Yes (`update_issue`) | Rule uses `status`, API uses `state`; confirm `id` format |
| GitHub ↔ Linear in repo | Partial (attachment on AIT-1) | No automation, no branch/PR rules |
| Cursor rule accuracy | Partial | Fix get_viewer → get_user, get_issues → list_issues, status → state |

---

## 7. Next Steps (for implementation plan)

1. **Cursor rule**: Update `.cursor/rules/linear-ai-todo-integration.mdc` to use `get_user("me")`, `list_issues({ assignee: "me" })`, and `update_issue(id, state: "In Review")` (and confirm id/state values).
2. **Data model / automation**: Decide how to handle assignee and cycle (e.g. accept “filter-only” for now, or request MCP/API changes to include assignee/cycle on issue).
3. **Branch/PR standards**: Define branch naming (e.g. `user/ID-desc`) and PR title format; document in repo and optionally enforce via GitHub.
4. **GitHub Actions**: If we want “on merge → update Linear”, add a step and document required secrets (e.g. Linear API key).
5. **Day 1 guide**: Document how to configure Linear MCP (user-level) and ai-todo (project-level), and how to run the kickoff workflow from the Cursor rule.

---

*Assessment produced for task #266.1. Linear MCP tools were run live; payload structure is from actual `get_issue` response for AIT-1.*
