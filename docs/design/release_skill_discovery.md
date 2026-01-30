# Release Workflow Cursor Skill - Discovery Analysis

**Task:** #270.1 (AIT-12)
**Date:** 2026-01-30
**Status:** Discovery Complete

---

## Executive Summary

The ai-todo project currently has release workflow instructions scattered across multiple Cursor rules that are **always applied** to every conversation, consuming valuable context window space. This discovery identifies all release-related content and proposes migrating it to a dedicated **Cursor Skill** that only loads when explicitly needed for release operations.

**Impact:** Reduces default context consumption while maintaining full release workflow guidance when needed.

---

## Current State

### 1. Cursor Rules (`.cursor/rules/`)

#### A. `release-workflow.mdc` (ACTIVE)
- **Status:** `alwaysApply: true` ⚠️
- **Size:** 37 lines
- **Purpose:** Provides instructions for "prepare release" and "execute release" commands
- **Key Content:**
  - Prepare release workflow (wait for CI, generate summary, run script, wait for approval)
  - Execute release workflow (run script, monitor CI)
  - Error handling guidelines
  - Forbidden actions (never auto-execute, never bypass CI, never use `--no-verify`)

**Migration Priority:** **HIGH** - This is always loaded and consumes context unnecessarily.

#### B. `linear-release-workflow.mdc` (DISABLED)
- **Status:** `alwaysApply: false` (explicitly disabled)
- **Size:** 50 lines
- **Purpose:** Automated release workflow with Linear tracking and approval gates
- **Key Content:**
  - 10-step automated workflow
  - ai-todo task structure creation
  - Linear comment monitoring for approvals
  - Detailed safety rules

**Migration Priority:** **MEDIUM** - Currently disabled, but could be useful if re-enabled as part of a skill.

### 2. Release Scripts (`release/`)

**Scripts identified:**
- `release.sh` - Main intelligent release automation script
- `publish_pypi.sh` - PyPI publishing automation
- `convert_zsh_to_bash.sh` - Shell conversion utility

**Migration Priority:** **LOW** - These are executable scripts, not instructions. They should be **referenced** by the skill but not duplicated.

### 3. Documentation (`release/`, `docs/`)

**Key document:**
- `release/RELEASE_PROCESS.md` - Comprehensive 720-line release process guide
  - Version numbering (semantic versioning)
  - Beta vs stable release strategy
  - AI agent workflow instructions
  - Manual release steps
  - Migration handling in releases
  - CI/CD optimization details

**Migration Priority:** **MEDIUM** - Should be referenced by the skill via progressive disclosure (link to it rather than duplicate content).

---

## Analysis: What Should Migrate to Cursor Skill?

### Core Skill Content (Direct Migration)

**From `release-workflow.mdc`:**
- ✅ Prepare release workflow
- ✅ Execute release workflow
- ✅ Error handling rules
- ✅ Forbidden actions

**Why:** These are the essential instructions the agent needs when performing a release.

### Supporting Content (Reference Links)

**From `RELEASE_PROCESS.md`:**
- 🔗 Link to detailed process documentation
- 🔗 Link to migration guidelines
- 🔗 Link to version numbering conventions

**Why:** Use progressive disclosure - link to detailed docs rather than duplicating 720 lines in the skill.

### Optional Enhancement

**From `linear-release-workflow.mdc` (currently disabled):**
- 🤔 Consider including the automated Linear workflow as an **advanced mode**
- 🤔 Or create a **separate skill** for fully automated releases

**Why:** The disabled workflow represents a more automated approach that might be valuable but is currently not in use.

---

## Recommendations

### 1. Create Primary Release Skill

**Name:** `release-workflow`
**Description:** "Guides release preparation and execution for ai-todo. Use when the user asks to 'prepare release', 'execute release', 'release', or mentions creating a new version."

**Content Structure:**

```markdown
---
name: release-workflow
description: Guides release preparation and execution for ai-todo. Use when the user asks to 'prepare release', 'execute release', 'release', or mentions creating a new version.
---

# Release Workflow for ai-todo

## Quick Reference

- **Prepare:** `./release/release.sh --prepare [--beta] --summary release/AI_RELEASE_SUMMARY.md`
- **Execute:** `./release/release.sh --execute`
- **Detailed docs:** See [release/RELEASE_PROCESS.md](../../release/RELEASE_PROCESS.md)

## Prepare a Release

When user asks to "prepare release" or "prepare beta release":

1. Wait for CI: `./scripts/wait-for-ci.sh`
2. Generate 2-3 paragraphs highlighting user-facing changes. Save to `release/AI_RELEASE_SUMMARY.md`.
   - **For beta-to-beta releases**: Analyze commits since the last beta tag.
   - **For stable releases (graduating from beta)**: Analyze ALL commits since the last **stable** release (not the last beta). This ensures the summary covers the entire beta cycle.
3. Run: `./release/release.sh --prepare [--beta] --summary release/AI_RELEASE_SUMMARY.md`
4. **STOP.** Show preview and let user review before proceeding.

## Execute a Release

When user asks to "execute release":

1. Run: `./release/release.sh --execute`
2. Monitor GitHub Actions until success.

## Error Handling

**If ANY error occurs:**
1. **STOP IMMEDIATELY.**
2. Report the error.
3. **WAIT FOR USER.** Do not attempt auto-recovery.

## Forbidden Actions

- ❌ Never auto-execute after prepare.
- ❌ Never bypass CI/CD failures.
- ❌ **NEVER use `--no-verify` on git commits.**

## Additional Resources

- **Detailed Process:** [release/RELEASE_PROCESS.md](../../release/RELEASE_PROCESS.md)
- **Version Strategy:** Beta vs Stable release guidelines
- **Migration Handling:** Adding migrations to releases
```

**Estimated Size:** ~50-60 lines (well under 500-line limit)

### 2. Remove from Global Rules

After skill creation:
- **Delete** or **disable** `release-workflow.mdc`
- **Keep disabled:** `linear-release-workflow.mdc` (already disabled)

This will **free up 37 lines** from the default context window.

### 3. Optional: Create Advanced Skill (Future)

If the automated Linear workflow proves valuable:
- Create separate skill: `release-workflow-automated`
- Include the 10-step automated workflow
- User can explicitly invoke when needed

---

## Migration Strategy

### Phase 1: Create Skill
1. Create `.cursor/skills/release-workflow/` directory
2. Create `SKILL.md` with content above
3. Test that agent can discover and apply the skill

### Phase 2: Cleanup
1. Delete `.cursor/rules/release-workflow.mdc`
2. Verify `linear-release-workflow.mdc` remains disabled
3. Commit changes

### Phase 3: Verification
1. Test: Ask agent to "prepare release" (should load skill)
2. Test: Ask agent general questions (should not load skill)
3. Verify context window is cleaner

---

## Benefits

### Before Migration
- **37 lines** of release instructions **always loaded**
- Consumes context in conversations that have nothing to do with releases
- Cannot be easily updated without affecting all conversations

### After Migration
- **0 lines** loaded by default
- Release instructions only load when explicitly needed
- Easier to maintain and update (single skill file)
- Can be enhanced without impacting default context

---

## Next Steps

1. ✅ **Discovery complete** (this document)
2. ⏭️ **Create skill** (subtask #270.2)
3. ⏭️ **Remove rule** (subtask #270.3)
4. ⏭️ **Verify** (subtask #270.4)

---

## Files to Create

- `.cursor/skills/release-workflow/SKILL.md`

## Files to Delete

- `.cursor/rules/release-workflow.mdc`

## Files to Keep (No Changes)

- `.cursor/rules/linear-release-workflow.mdc` (already disabled)
- `release/RELEASE_PROCESS.md` (documentation)
- All release scripts in `release/` (executable tools)
