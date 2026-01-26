# Naming Unification Analysis

**Task:** #219.1 - Write naming analysis document
**Status:** In Progress
**Date:** 2026-01-26

## Executive Summary

The todo.ai project suffers from naming fragmentation across platforms, creating confusion for users and documentation complexity. This analysis evaluates the current state, identifies pain points, and proposes options for unification.

**Decision:** Unify to `ai-todo` across all platforms. Deprecate shell script (move to `legacy/`, do not rename).

---

## Current State

### Name Inventory

| Context | Current Name | Notes |
|---------|--------------|-------|
| **GitHub Repository** | `todo.ai` | fxstein/todo.ai |
| **PyPI Package** | `ai-todo` | Forced by PyPI (todo.ai unavailable) |
| **CLI Command** | `todo-ai` | Installed via `uv tool install ai-todo` |
| **MCP Server** | `todo-ai` | `todo-ai serve` |
| **Legacy MCP** | `todo-ai-mcp` | Deprecated alias |
| **Shell Script** | `todo.ai` / `./todo.ai` | Legacy v2.x |
| **Project Concept** | "todo.ai" | Marketing/branding |

### Current Installation Commands

```bash
# PyPI package name
uv tool install ai-todo      # Package: ai-todo
pipx install ai-todo         # Package: ai-todo

# But installs CLI named:
todo-ai                      # Command: todo-ai

# uvx invocation requires:
uvx --from ai-todo todo-ai   # Package ≠ Command

# Shell script:
./todo.ai                    # Different from CLI
```

---

## Confusion Points

### 1. Package vs Command Mismatch

**Problem:** PyPI package is `ai-todo` but CLI command is `todo-ai`.

```bash
# Confusing:
uv tool install ai-todo   # Package name
todo-ai list              # Command name (different!)

# Users expect:
uv tool install foo
foo list                  # Same name
```

### 2. uvx Requires `--from` Flag

**Problem:** `uvx ai-todo` doesn't work because the executable isn't named `ai-todo`.

```bash
# Fails:
uvx ai-todo serve

# Works but verbose:
uvx --from ai-todo todo-ai serve
```

### 3. Repository vs Package Name

**Problem:** GitHub repo is `todo.ai` but package is `ai-todo`.

- Clone: `git clone github.com/fxstein/todo.ai`
- Install: `pip install ai-todo`

Users searching PyPI for "todo.ai" won't find it.

### 4. Shell Script vs CLI

**Problem:** Legacy shell script uses `./todo.ai` but Python CLI uses `todo-ai`.

```bash
# Legacy:
./todo.ai list

# Modern:
todo-ai list
```

### 5. Documentation Burden

Every document must explain multiple names:
- "Install `ai-todo` via PyPI"
- "Run `todo-ai` command"
- "Or use `./todo.ai` shell script"
- "MCP server via `todo-ai serve`"

### 6. MCP Configuration Complexity

```json
{
  "command": "uvx",
  "args": ["--from", "ai-todo", "todo-ai", "serve"]
}
```

Would be simpler as:
```json
{
  "command": "uvx",
  "args": ["ai-todo", "serve"]
}
```

---

## Options

### Option A: Unify to `ai-todo` (Recommended)

**Change:** Rename everything to `ai-todo` to match PyPI.

| Item | Current | New |
|------|---------|-----|
| GitHub Repo | fxstein/todo.ai | fxstein/ai-todo |
| CLI Command | todo-ai | ai-todo |
| Shell Script | todo.ai | ai-todo (or deprecate) |
| Brand/Concept | todo.ai | ai-todo |

**Pros:**
- Single name everywhere
- PyPI already uses this name
- `uvx ai-todo` works directly
- Simpler documentation
- Simpler MCP config

**Cons:**
- GitHub repo rename required
- Breaks existing bookmarks/clones (GitHub redirects)
- Shell script rename or deprecation
- Some documentation updates

### Option B: Unify to `todo-ai`

**Change:** Keep CLI name, change PyPI package name.

**Pros:**
- CLI stays the same
- More "natural" English word order

**Cons:**
- **Cannot change PyPI package name** (would require new package)
- Would have two packages: `ai-todo` (old) + `todo-ai` (new)
- Confusing migration

### Option C: Unify to `todo.ai`

**Change:** Rename CLI to match repo/brand.

**Pros:**
- Matches existing brand
- Matches shell script

**Cons:**
- **Cannot use on PyPI** (name unavailable)
- Dots problematic in CLI names on some systems
- Would still have `ai-todo` on PyPI

### Option D: Keep Current Names

**Change:** None. Document the differences clearly.

**Pros:**
- No migration effort
- No risk of breaking changes

**Cons:**
- Permanent documentation complexity
- User confusion continues
- uvx requires `--from` flag forever

---

## Comparison Matrix

| Criteria | A: ai-todo | B: todo-ai | C: todo.ai | D: Keep |
|----------|------------|------------|------------|---------|
| PyPI match | ✅ | ❌ | ❌ | ❌ |
| Simple uvx | ✅ | ❌ | ❌ | ❌ |
| GitHub rename | Required | Required | No | No |
| CLI rename | Yes | No | Yes | No |
| Doc simplicity | ✅ | ❌ | ❌ | ❌ |
| Migration risk | Low | High | N/A | None |
| User confusion | Fixed | Worse | N/A | Continues |

---

## Risk Assessment

### GitHub Rename Risks (Options A, B)

1. **Existing clones:** Users with existing clones need to update remote URL
   - Mitigation: GitHub provides automatic redirects

2. **Bookmarks/Links:** Old URLs redirect automatically
   - Mitigation: GitHub redirect lasts indefinitely

3. **Stars/Watchers:** Preserved during rename

4. **CI/CD:** GitHub Actions workflows continue working

### PyPI Risks

1. **Package name change impossible:** PyPI doesn't allow renaming
   - `ai-todo` is permanent
   - New package would require deprecation notice on old

### User Migration Risks

1. **7 GitHub stars:** Very low user base
   - Minimal migration impact
   - Good time to make breaking changes

---

## Implementation Considerations

### If Option A (ai-todo) is chosen:

1. **GitHub:** Rename repo fxstein/todo.ai → fxstein/ai-todo
2. **CLI:** Rename `todo-ai` → `ai-todo` in pyproject.toml
3. **Shell:** Rename `todo.ai` → `ai-todo` (or deprecate)
4. **Docs:** Search/replace all name references
5. **MCP:** Simplify config to `uvx ai-todo serve`
6. **URLs:** Update all documentation links

### Files Requiring Updates

- `pyproject.toml` (entry points)
- `README.md`
- `docs/**/*.md` (all documentation)
- `.cursor/mcp.json` examples
- `.cursorrules`
- `.cursor/rules/*.mdc`
- GitHub Actions workflows
- Install scripts

---

## Decisions

### Decision 1: Unified Name

**Chosen: Option A — `ai-todo`**

Rationale:
1. PyPI name is immutable — we must align to it
2. Only 7 GitHub stars — minimal migration impact
3. Eliminates all naming confusion
4. Simplifies uvx usage significantly
5. Reduces documentation complexity
6. Now is the best time (before more adoption)

### Decision 2: Shell Script Handling

**Chosen: Deprecate and relocate (do not rename)**

- Move `todo.ai` and `todo.bash` to `legacy/` directory
- Keep original filenames for users who still need them
- Mark as deprecated in documentation
- Remove from repository root to reduce confusion

### Decision 3: CLI Command Alias

**Chosen: No alias (clean break)**

- Remove `todo-ai` entry point immediately
- Only `ai-todo` command available
- With 7 GitHub stars, clean break is simpler than maintaining dual entry points

### Decision 4: Install Script

**Chosen: Remove entirely**

- Delete `install.sh` from repository
- Users install via `uv tool install ai-todo` or `pipx install ai-todo`
- Simplifies repository, no legacy install path to maintain

### Decision 5: Sequencing

**Chosen: Parallel (update docs + rename together)**

- Update all documentation locally to use `ai-todo` names
- Execute GitHub repo rename and code changes
- Push everything together as single coherent release
- Task #203 (README redesign) merges into this release

### Decision 6: Legacy MCP Alias

**Chosen: Remove entirely**

- Delete `todo-ai-mcp` entry point
- Only `ai-todo serve` available for MCP server
- No legacy aliases to maintain
