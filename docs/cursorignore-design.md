# .cursorignore Security Design Document

**Task:** #260 - Add .cursorignore files for secrets/sensitive content
**Status:** APPROVED - Option A selected
**Date:** 2026-01-27
**GitHub Issue:** #29
**Decision:** Option A (Minimal Security Focus)

## Executive Summary

This document analyzes `.cursorignore` capabilities, documents security limitations, and proposes ignore patterns for the ai-todo project to protect sensitive content from AI agents.

## Research Findings

### 1. .cursorignore Format

- Uses `.gitignore` syntax
- Placed in project root directory
- Supports pattern matching: `*.log`, `**/logs`, `dist/`, `!exclude`
- Later patterns override earlier ones
- Supports hierarchical ignore (setting must be enabled)

### 2. Cursor Default Global Ignore Patterns

Cursor automatically ignores these across ALL projects:

| Category | Patterns |
|----------|----------|
| Environment | `**/.env`, `**/.env.*` |
| Credentials | `**/credentials.json`, `**/secrets.json` |
| Keys | `**/*.key`, `**/*.pem`, `**/id_rsa` |

### 3. Default Indexing Ignore List

Cursor also ignores for indexing (not access):
- Lock files: `package-lock.json`, `yarn.lock`, `*.lock`
- Binary/media files: `*.exe`, `*.dll`, `*.jpg`, `*.mp4`, etc.
- Cache directories: `.venv/`, `node_modules/`, `__pycache__/`, `.pytest_cache/`
- VCS directories: `.git/`, `.svn/`, `.hg/`

### 4. Critical Security Limitations

**Important: .cursorignore does NOT provide complete protection!**

| Limitation | Impact |
|------------|--------|
| **MCP/Tool Access** | Tool calls (terminal, MCP servers) bypass .cursorignore |
| **Recently Viewed** | Files recently viewed may still be included in context |
| **LLM Unpredictability** | Cursor states: "complete protection isn't guaranteed due to LLM unpredictability" |
| **Agent Mode** | Agent composer may access ignored directories |

**Implication for ai-todo:** Since ai-todo IS an MCP server, the .cursorignore patterns won't prevent ai-todo itself from accessing files. However, they will prevent OTHER AI features (Tab, Inline Edit, @ references) from accessing the ignored files.

## Current State Analysis

### Existing .cursorignore

```
.todo.ai/state/
```

This only ignores the legacy state directory.

### Files Requiring Protection in ai-todo

| File/Pattern | Sensitivity | Currently Ignored |
|--------------|-------------|-------------------|
| `.ai-todo/state/` | HIGH - Tamper detection state, shadow TODO.md | No (wrong path) |
| `.ai-todo/state/checksum` | HIGH - File integrity verification | No |
| `.ai-todo/state/tamper_mode` | MEDIUM - Security configuration | No |
| `.ai-todo/config.yaml` | LOW - Project configuration | No |
| `.ai-todo/.ai-todo.log` | LOW - Operation audit log | No |
| `.ai-todo/backups/` | MEDIUM - Task backups | Already in .gitignore |
| `release/.prepare_state` | MEDIUM - Release state | Already in .gitignore |

### Files Already Protected by Cursor Defaults

These don't need explicit patterns:
- `**/.env`, `**/.env.*` - Environment variables
- `**/credentials.json`, `**/secrets.json` - Credential files
- `**/*.key`, `**/*.pem`, `**/id_rsa` - Private keys

## Proposed Design

### Option A: Minimal Security Focus (Recommended)

Focus on ai-todo-specific sensitive files only, relying on Cursor defaults for common patterns.

```
# ai-todo Tamper Detection State (PROTECTED)
# Shadow copy and integrity checksums - agents should not access directly
.ai-todo/state/

# Legacy data directory state (backward compatibility)
.todo.ai/state/

# Internal operational data
.ai-todo/backups/
.todo.ai/backups/
```

**Rationale:**
- State directory contains checksum and shadow TODO.md for tamper detection
- Agents accessing these files could interfere with integrity verification
- Minimal patterns reduce complexity and maintenance

### Option B: Comprehensive Security

Include additional protection for logs and configuration.

```
# ai-todo Tamper Detection State (PROTECTED)
.ai-todo/state/
.todo.ai/state/

# Operational logs (may contain sensitive task content)
.ai-todo/.ai-todo.log
.todo.ai/.todo.ai.log

# Backups
.ai-todo/backups/
.todo.ai/backups/

# Release artifacts
release/.prepare_state
```

**Trade-off:** More protection but logs can be useful for debugging.

### Option C: Strict Lockdown

Ignore entire .ai-todo directory except config.

```
# Ignore all ai-todo internal state
.ai-todo/
.todo.ai/

# But allow reading config for reference
!.ai-todo/config.yaml
```

**Trade-off:** Maximum security but prevents agents from seeing migration status, logs for troubleshooting.

## Recommendation

**Option A (Minimal Security Focus)** is recommended because:

1. **Targeted Protection**: Focuses on files that could actually cause harm if accessed
2. **Cursor Defaults**: Relies on built-in protection for common sensitive patterns
3. **Practical Security**: Acknowledges that .cursorignore has limitations anyway
4. **Debugging Friendly**: Allows access to logs for troubleshooting

## Implementation Plan

1. Update `.cursorignore` with chosen patterns
2. Add comments explaining each pattern's purpose
3. Document security limitations in user documentation
4. Consider adding `.cursorignore` management to `ai-todo init`

## Security Best Practices Documentation

Users should be advised:

1. **Don't store secrets in TODO.md** - Task descriptions are visible to AI
2. **Use environment variables** - Cursor ignores `.env` files by default
3. **Separate credentials** - Keep API keys in dedicated ignored files
4. **Understand limitations** - .cursorignore is defense-in-depth, not absolute

## Open Questions

1. Should `ai-todo init` auto-generate .cursorignore patterns?
2. Should we document .cursorignore setup in installation guide?
3. Should we provide a sample .cursorignore for users' projects?

---

**APPROVED:** Option A - Minimal Security Focus (2026-01-27)
