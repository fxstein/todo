---
name: release-workflow
description: Guides release preparation and execution for ai-todo. Use when the user asks to 'prepare release', 'execute release', 'release', or mentions creating a new version.
---

# Release Workflow for ai-todo

## Quick Reference

- **Prepare:** `./release/release.sh --prepare [--beta] [--set-version X.Y.Z] --summary release/AI_RELEASE_SUMMARY.md`
- **Execute:** `./release/release.sh --execute`
- **Detailed docs:** [release/RELEASE_PROCESS.md](../../../release/RELEASE_PROCESS.md)

## Prepare a Release

When user asks to "prepare release" or "prepare beta release":

1. **Wait for CI:** `./scripts/wait-for-ci.sh`
2. **Generate summary:** Create 2-3 paragraphs highlighting user-facing changes. Save to `release/AI_RELEASE_SUMMARY.md`.
   - **For beta-to-beta releases:** Analyze commits since the last beta tag.
   - **For stable releases (graduating from beta):** Analyze ALL commits since the last **stable** release (not the last beta). This ensures the summary covers the entire beta cycle.
3. **Run prepare:** `./release/release.sh --prepare [--beta] --summary release/AI_RELEASE_SUMMARY.md`
4. **STOP.** Show preview and let user review before proceeding.

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
