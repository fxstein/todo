---
name: release-workflow
description: Guides release preparation and execution for ai-todo. Use when the user asks to 'prepare release', 'execute release', 'release', or mentions creating a new version.
---

# Release Workflow for ai-todo

## Quick Reference

- **Prepare:** `./release/release.sh --prepare [--beta] [--set-version X.Y.Z] --summary release/AI_RELEASE_SUMMARY.md`
- **Dry Run:** `./release/release.sh --prepare --dry-run` (preview without committing)
- **Execute:** `./release/release.sh --execute`
- **Abort:** `./release/release.sh --abort [version]` (cleanup failed release)
- **Detailed docs:** [release/RELEASE_PROCESS.md](../../../release/RELEASE_PROCESS.md)

## Prepare a Release

When user asks to "prepare release" or "prepare beta release":

1. **Pre-flight checks:** Verify repository is ready for release:
   - **Check branch:** `git branch --show-current` (must be `main`)
   - **Check sync:** `git fetch origin && git status` (must be in sync with origin/main)
   - **Check clean:** `git status --porcelain` (must be empty - no uncommitted changes)
   - **If any check fails:** ⚠️ Warn user with specific issue and ask "Do you want to proceed anyway?"
   - **If user declines:** Stop and let them fix the issue first.
2. **Wait for CI:** `./scripts/wait-for-ci.sh`
3. **Generate summary:** Create 2-3 paragraphs highlighting user-facing changes. Save to `release/AI_RELEASE_SUMMARY.md`.
   - **For beta-to-beta releases:** Analyze commits since the last beta tag.
   - **For stable releases (graduating from beta):** Analyze ALL commits since the last **stable** release (not the last beta). This ensures the summary covers the entire beta cycle.
   - See "Generating Release Summary" section below for detailed guidance.
4. **Run prepare:** `./release/release.sh --prepare [--beta] --summary release/AI_RELEASE_SUMMARY.md`
5. **STOP.** Show preview and let user review before proceeding.

## Generating Release Summary

**Role:** You are a Technical Release Manager for a professional Open Source project.

**Task:** Draft a release summary based on commit messages for **end-users** (not developers).

**Commit Range:**
- **For beta-to-beta releases:** Analyze commits since the last beta tag (e.g., `v4.0.0b2..HEAD`)
- **For stable releases (graduating from beta):** Analyze ALL commits since the last stable release (e.g., `v3.0.2..HEAD`)

**Constraints & Formatting:**
1. **Format:** Write exactly 2-4 paragraphs of narrative text. Do not use bulleted lists or markdown headers (e.g., no `#` or `##`).
2. **Content:** Focus only on the most significant features, user-facing changes, and critical fixes. Filter out minor chores, typo fixes, or internal refactors unless they directly impact end users.
3. **Documentation:** If commits added new documentation files (`.md`, `.pdf`), mention them with direct GitHub links:
   - Get repo URL: `git remote get-url origin` (convert SSH to HTTPS if needed)
   - Format: `[filename](https://github.com/user/repo/blob/main/path/to/file.md)`
4. **Tone:** Professional, concise, and encouraging. Write for users who want to understand what's new and why they should upgrade.
5. **Output:** Save to `release/AI_RELEASE_SUMMARY.md`

**Example Structure:**
```
This release focuses on [theme/primary improvement]. [Key feature 1] provides [user benefit]. [Key feature 2] enhances [capability].

[Second major area of improvement]. [Specific change] now allows users to [benefit]. [Another change] improves [aspect] by [improvement].

Additional improvements include [grouped minor features]. Several bug fixes improve robustness including [specific fixes that matter to users].
```

**Generate Commits:**
```bash
# For beta-to-beta:
git log v4.0.0b2..HEAD --pretty=format:"%h %s" --no-merges

# For stable (graduating from beta):
git log v3.0.2..HEAD --pretty=format:"%h %s" --no-merges
```

## Execute a Release

When user asks to "execute release":

1. **Run execute:** `./release/release.sh --execute`
2. **Monitor:** Watch GitHub Actions until success.

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

- **Detailed Process:** [release/RELEASE_PROCESS.md](../../../release/RELEASE_PROCESS.md)
- **Version Strategy:** Beta vs Stable release guidelines in RELEASE_PROCESS.md
- **Migration Handling:** See RELEASE_PROCESS.md for adding migrations to releases
- **Release Scripts:** All scripts are in `release/` directory
