# Release Summary

This patch release fixes a critical bug in the release workflow that caused v2.3.0 to be published with incorrect release notes.

## Bug Fix

**Stale Summary Detection**

The release script now validates that the release summary file is current before using it ([b27f7cb](https://github.com/fxstein/todo.ai/commit/b27f7cb)). This prevents publishing releases with outdated summaries from previous versions.

**How it works:**
- Compares summary file modification time with last release tag timestamp
- Shows clear warning if summary file is older than the last release
- In interactive mode: prompts user to continue or abort
- In non-interactive mode: automatically aborts to prevent mistakes

**What happened:** v2.3.0 was accidentally published with v2.2.1's release notes because the script used a stale `RELEASE_SUMMARY.md` file without validation. This fix ensures release summaries are always current and accurate.

## Additional Changes

- Marked task #142 (release script bug fixes) as complete
- Created task #143 to track the stale summary detection implementation
