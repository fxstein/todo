# Version 2.6.0 Incident Analysis and Resolution

## Executive Summary

**Issue:** Version 2.6.0 was never released but appeared in the codebase, causing version 2.5.1 to be skipped and 2.7.0 to be released instead.

**Root Cause:** The VERSION variable in `todo.ai` file was manually edited (likely by an AI agent), creating a "phantom version" that didn't exist in GitHub releases.

**Resolution:** Made GitHub releases the single source of truth for versioning, with file VERSION becoming a secondary placeholder.

---

## Incident Timeline (November 15, 2025)

### Normal Release: v2.5.0
```
13:47:57 - Released v2.5.0 successfully ✅
           File VERSION: 2.5.0
           GitHub: v2.5.0
```

### Post-Release Development
```
13:48:21 - Marked tasks complete 
14:12:06 - Added pre-commit check
21:46:40 - Created task#157 for issue#38
21:49:19 - Fixed get_highest_task_number()
21:55:49 - Created universal converter script
22:08:42 - Fixed increment_serial()
22:17:32 - Fixed sed backup
```

### The Phantom Version Incident
```
22:17:42 - 🔴 RELEASE START: "Current version: 2.6.0"
           ❌ VERSION in file: 2.6.0 (NEVER RELEASED!)
           ✅ GitHub latest: v2.5.0
           
22:17:52 - Updated from 2.6.0 to 2.7.0
           ❌ Skipped 2.5.1 (intended version)
           ❌ Skipped 2.6.0 (phantom version)
           
22:17:53 - Released v2.7.0 ❌
```

### Evidence of the Problem

1. **Release Log Shows Version Mismatch:**
   ```
   Updating version in todo.ai from 2.6.0 to 2.7.0
   Last tag: v2.5.0
   ```
   Version 2.6.0 existed in file but v2.5.0 was the last GitHub release!

2. **Release Summary Was Wrong:**
   - File: `release/RELEASE_SUMMARY.md`
   - Content: "**todo.ai v2.5.1 Hotfix Release**"
   - Actual release created: **v2.7.0**

3. **Uncommitted Changes in todo.bash:**
   - Had VERSION="2.6.0" manually edited
   - Violates zsh-first development rule
   - Evidence of direct file manipulation

---

## Root Cause Analysis

### What Happened

1. After v2.5.0 release, someone (likely an AI agent) manually changed VERSION in `todo.ai` to "2.6.0"
2. The release script read VERSION from the file instead of querying GitHub
3. The script saw "2.6.0" as current and bumped to "2.7.0"
4. Release summary described "v2.5.1" but v2.7.0 was released
5. Someone also edited `todo.bash` directly (violating development rules)

### Why It Happened

**Architectural Flaw:** The release script used `get_current_version()` which read from the file:

```zsh
# OLD (BROKEN) - File was source of truth
get_current_version() {
    grep '^VERSION=' todo.ai | sed 's/VERSION="\([^"]*\)"/\1/'
}
```

**Problem:** Files can be accidentally or maliciously edited, creating phantom versions.

---

## Solution Implemented

### Architectural Change: GitHub as Source of Truth

**NEW APPROACH:**
- GitHub releases = PRIMARY source of truth (immutable, API-queryable)
- File VERSION = SECONDARY placeholder (updated during release)
- Validation warnings when file doesn't match GitHub

### Code Changes

#### 1. Get Version from GitHub (PRIMARY)
```zsh
get_github_version() {
    # Query GitHub API for latest release
    local latest_tag=$(gh release list --limit 1 --json tagName --jq '.[0].tagName' 2>/dev/null || echo "")
    if [[ -z "$latest_tag" ]]; then
        return 1  # No releases
    fi
    echo "${latest_tag#v}"  # Remove 'v' prefix
}
```

#### 2. Get Version from File (VALIDATION ONLY)
```zsh
get_file_version() {
    grep '^VERSION=' todo.ai | sed 's/VERSION="\([^"]*\)"/\1/'
}
```

#### 3. Use GitHub as Source of Truth
```zsh
get_current_version() {
    local github_version=$(get_github_version 2>/dev/null)
    
    if [[ -n "$github_version" ]]; then
        # GitHub version exists - use as source of truth
        echo "$github_version"
    else
        # No GitHub releases yet - fall back to file (first release only)
        echo $(get_file_version)
    fi
}
```

#### 4. Validate Consistency
```zsh
validate_version_consistency() {
    local github_version=$(get_github_version 2>/dev/null)
    local file_version=$(get_file_version)
    
    if [[ "$file_version" != "$github_version" ]]; then
        echo "⚠️  VERSION MISMATCH DETECTED"
        echo "File version (todo.ai):    ${file_version}"
        echo "GitHub version (releases): ${github_version}"
        echo "GitHub releases are the source of truth."
        log_release_step "VERSION MISMATCH" "..."
    fi
}
```

### New Release Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Version Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current version (GitHub):  2.7.0 ✓
File version (todo.ai):     2.7.0
```

Now the release script clearly shows:
- **GitHub version** = source of truth (what matters)
- **File version** = validation reference (informational)

---

## Benefits of the New Approach

### 1. **Prevents Phantom Versions**
- Manual file edits can't create fake versions
- GitHub releases are immutable
- Version history is authoritative

### 2. **Version Consistency**
- Warns when file doesn't match GitHub
- Makes discrepancies visible immediately
- Self-healing: file updated during next release

### 3. **Audit Trail**
- GitHub releases provide complete history
- Release log shows both GitHub and file versions
- Easy to detect manipulation attempts

### 4. **AI Agent Safety**
- Agents can't accidentally create phantom versions
- File edits have no effect on version detection
- Reduces risk of "web of lies" scenarios

---

## Testing the Fix

### Test 1: Normal Operation
```bash
$ ./release/release.sh --prepare
🚀 Preparing release preview...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Version Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current version (GitHub):  2.7.0 ✓
File version (todo.ai):     2.7.0

📌 Last release: v2.7.0
```
✅ **Result:** Correctly detects v2.7.0 from GitHub

### Test 2: Version Mismatch Detection
If someone edits VERSION="2.8.0" in the file:
```bash
⚠️  VERSION MISMATCH DETECTED
File version (todo.ai):    2.8.0
GitHub version (releases): 2.7.0
GitHub releases are the source of truth.
```
✅ **Result:** Warning displayed, GitHub version used

---

## Commit Details

**Commit:** `83f4336c8ffe65bccf6adeeaad86e8092c840ed1`
**Message:** `backend: Make GitHub releases the source of truth for versioning`
**Type:** Backend infrastructure (PATCH release)

**Changes:**
- Modified: `release/release.sh` (+177/-194 lines)
- Added: `get_github_version()` function
- Added: `get_file_version()` function  
- Added: `validate_version_consistency()` function
- Changed: `get_current_version()` to query GitHub
- Updated: Release preview to show both versions

---

## Recommendations

### For Developers

1. **Never manually edit VERSION in todo.ai**
   - It's now just a placeholder
   - Will be overwritten during release
   - Has no effect on version detection

2. **Trust GitHub releases**
   - Check `gh release list` for current version
   - File VERSION may be out of sync temporarily
   - Release script will fix it automatically

3. **Follow zsh-first development**
   - NEVER edit `todo.bash` directly
   - It's auto-generated from `todo.ai`
   - Manual edits will be overwritten

### For AI Agents

1. **Query GitHub for version**
   ```bash
   gh release list --limit 1
   # OR
   ./release/release.sh --prepare  # Shows GitHub version
   ```

2. **Don't attempt version "corrections"**
   - File VERSION mismatches are harmless
   - Release script handles them automatically
   - Manual intervention creates problems

3. **Report discrepancies**
   - If file VERSION doesn't match GitHub
   - Log it, don't fix it manually
   - Let the release process handle it

---

## Lessons Learned

### What Went Wrong

1. **Single Source of Truth Was Mutable**
   - File-based version could be changed
   - No validation against authoritative source
   - Silent corruption was possible

2. **No Consistency Checking**
   - No warning when file didn't match reality
   - Phantom versions went undetected
   - Only visible in release logs after the fact

3. **Agent Autonomy Without Guardrails**
   - AI agent could edit critical version info
   - No validation of changes
   - Cascading errors created "web of lies"

### What We Fixed

1. **Immutable Source of Truth**
   - GitHub releases can't be accidentally edited
   - API-queryable and authoritative
   - Provides complete audit trail

2. **Active Validation**
   - Mismatch detection built into release process
   - Clear warnings when discrepancies exist
   - Informative display of both versions

3. **Self-Healing Design**
   - File VERSION updated automatically during release
   - Temporary mismatches are harmless
   - System recovers automatically

---

## Conclusion

The v2.6.0 phantom version incident exposed a fundamental design flaw: using a mutable file as the source of truth for versioning. By making GitHub releases the primary source with active validation, we've:

1. ✅ Prevented future phantom versions
2. ✅ Made version discrepancies visible
3. ✅ Created self-healing behavior
4. ✅ Improved safety for AI agent operations

The VERSION variable in `todo.ai` is now just a placeholder that's updated during releases. The true version history lives in GitHub releases, where it should be.

---

## References

- **Incident Commit:** 83f4336c8ffe65bccf6adeeaad86e8092c840ed1
- **Affected Versions:** v2.5.0 → v2.7.0 (skipped v2.5.1, v2.6.0)
- **Release Log:** `release/RELEASE_LOG.log` (lines 5-18)
- **Resolution Date:** 2025-11-15

