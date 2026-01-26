# Naming Unification Implementation Plan

**Task:** #219.3 - Create implementation plan with rollout phases
**Date:** 2026-01-26

## Overview

This document outlines the implementation plan for renaming the project from `todo.ai` to `ai-todo` based on the decisions in [NAMING_UNIFICATION_ANALYSIS.md](../analysis/NAMING_UNIFICATION_ANALYSIS.md).

## Phase 1: Pre-Rename Preparation

**Goal:** Prepare codebase for rename without breaking anything.

### 1.1 Code Changes (task#219.6)

- [ ] Update `todo_ai/` → `ai_todo/` directory
- [ ] Update all internal imports
- [ ] Update `pyproject.toml`:
  - Entry points: `todo-ai` → `ai-todo`
  - Remove `todo-ai-mcp` entry point
  - Update package find pattern: `todo_ai*` → `ai_todo*`
- [ ] Update GitHub URLs in pyproject.toml (prepare for new repo name)

### 1.2 Data Directory Migration (task#219.6.1-7)

- [ ] Update FileOps to use `.ai-todo/` as default
- [ ] Update config.py paths
- [ ] Rename state files (`.todo.ai.serial` → `.ai-todo.serial`)
- [ ] Implement auto-migration on startup
- [ ] Add migration logging
- [ ] Update .gitignore templates
- [ ] Test migration

### 1.3 Shell Script Deprecation

- [ ] Create `legacy/` directory
- [ ] Move `todo.ai` → `legacy/todo.ai`
- [ ] Move `todo.bash` → `legacy/todo.bash`
- [ ] Delete `install.sh`

### 1.4 Cursor Rules Update

- [ ] Update `.cursorrules`
- [ ] Update `.cursor/rules/*.mdc`
- [ ] Update generated user rules in code

## Phase 2: Documentation Update (task#219.8)

**Goal:** Update all documentation with new naming.

### 2.1 Main Documentation

- [ ] Update `README.md` (merge with task#203 changes)
- [ ] Update `docs/FAQ.md`
- [ ] Update `docs/README.md` (index)

### 2.2 User Guides

- [ ] Update `docs/user/MCP_SETUP.md`
- [ ] Update `docs/user/PYTHON_MIGRATION_GUIDE.md`
- [ ] Update `docs/guides/GETTING_STARTED.md`
- [ ] Update `docs/guides/INSTALLATION.md`

### 2.3 Design Documents

- [ ] Update `docs/design/README_REDESIGN_V3.md`
- [ ] Update any other docs referencing old names

### 2.4 Config File Comments

- [ ] Update `.todo.ai/config.yaml` header comment template

## Phase 3: CI/CD Updates

**Goal:** Update automation for new naming.

### 3.1 GitHub Actions

- [ ] Update `ci-cd.yml`:
  - CLI command references: `todo-ai` → `ai-todo`
  - Coverage paths: `--cov=todo_ai` → `--cov=ai_todo`
  - Release assets: update paths to `legacy/`

### 3.2 Pre-commit

- [ ] Update any pre-commit hooks referencing old names

## Phase 4: GitHub Rename

**Goal:** Rename repository on GitHub.

### 4.1 Repository Rename

- [ ] Go to GitHub Settings → General → Repository name
- [ ] Change `todo.ai` → `ai-todo`
- [ ] Verify redirect works

### 4.2 Post-Rename Verification

- [ ] Verify all GitHub Actions still work
- [ ] Verify PyPI publishing still works
- [ ] Verify git clone with new URL works
- [ ] Verify old URL redirects properly

## Phase 5: Release

**Goal:** Publish new version with all changes.

### 5.1 Version Bump

- [ ] Bump to v3.1.0 (or v4.0.0 for major breaking change?)
- [ ] Update CHANGELOG.md with migration notes

### 5.2 PyPI Release

- [ ] Build and publish to PyPI
- [ ] Verify `uv tool install ai-todo` installs `ai-todo` command
- [ ] Verify `uvx ai-todo serve` works

### 5.3 Announcement

- [ ] Update GitHub release notes
- [ ] Note breaking changes and migration path

## Rollback Plan

If critical issues are discovered:

1. **GitHub rename:** Can be reverted in settings (redirects both ways)
2. **Code changes:** Revert commits
3. **PyPI:** Cannot unpublish, but can release patch with fixes

## Testing Checklist

Before merging:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Manual test: fresh install via `uv tool install ai-todo`
- [ ] Manual test: `uvx ai-todo serve` works
- [ ] Manual test: migration from `.todo.ai/` to `.ai-todo/` works
- [ ] Manual test: existing TODO.md files work with new version

## Timeline

| Phase | Description | Dependencies |
|-------|-------------|--------------|
| 1 | Code changes | None |
| 2 | Documentation | Phase 1 |
| 3 | CI/CD updates | Phase 1 |
| 4 | GitHub rename | Phases 1-3 complete |
| 5 | Release | Phase 4 complete |

All phases can be done in a single session given the low user base (7 stars).
