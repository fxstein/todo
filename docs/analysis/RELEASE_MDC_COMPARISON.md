# Release.mdc Comparison: todo.ai vs ascii-guard

## Overview

| Aspect | todo.ai releases.mdc | ascii-guard ascii-guard-releases.mdc |
|--------|---------------------|-------------------------------------|
| **Length** | 31 lines (concise) | 639 lines (comprehensive) |
| **Structure** | Simple 3-step process | Detailed 4-step process with extensive safeguards |
| **Focus** | High-level workflow | Detailed workflow with error handling, CI/CD, environment checks |

---

## Key Differences

### 1. **Human Gate Emphasis**

**todo.ai:**
- ✅ Mentions prepare/execute workflow
- ⚠️ Does NOT explicitly emphasize mandatory human review between phases
- ⚠️ No explicit "STOP and wait" instructions

**ascii-guard:**
- ✅ **CRITICAL section** at top: "Two-Phase Process with Human Gate"
- ✅ Explicit warnings: "⚠️ NEVER skip the human review gate"
- ✅ Clear instructions: "STOP and wait for human" after prepare
- ✅ Multiple reminders throughout to wait for explicit "execute" command

**Impact:** ascii-guard is much more explicit about preventing automatic execution after prepare.

---

### 2. **CI/CD Check Requirement**

**todo.ai:**
- ❌ **NOT MENTIONED** - No CI/CD check requirement

**ascii-guard:**
- ✅ **Step 0: MANDATORY CI/CD Check** (lines 96-135)
- ✅ Must run `./scripts/wait-for-ci.sh` BEFORE starting release
- ✅ Must stop if CI/CD is failing
- ✅ Must check again after any commits during release
- ✅ Zero tolerance: "NEVER proceed while CI/CD is failing"

**Impact:** ascii-guard prevents releases when CI/CD is broken.

---

### 3. **Error Handling**

**todo.ai:**
- ❌ **NOT MENTIONED** - No error handling guidelines

**ascii-guard:**
- ✅ **CRITICAL: Error Handling During Releases** section (lines 139-229)
- ✅ "ZERO TOLERANCE FOR ERRORS" policy
- ✅ Detailed examples of what counts as errors
- ✅ Clear "STOP on ANY Error" rule
- ✅ Recovery process documented
- ✅ Example error responses (good vs bad)

**Impact:** ascii-guard provides comprehensive error handling guidance.

---

### 4. **File Naming and Workflow**

**todo.ai:**
- Uses `release/RELEASE_SUMMARY.md` as **single source of truth**
- Summary can be edited after prepare
- Execute regenerates notes from current RELEASE_SUMMARY.md
- No separate AI summary file

**ascii-guard:**
- Uses `release/AI_RELEASE_SUMMARY.md` (AI-written summary)
- Uses `release/RELEASE_NOTES.md` (complete notes with commits)
- **MUST commit AI summary immediately** after creating it
- **MUST run prepare within 60 seconds** of committing summary
- Summary is input to prepare, notes are output for review

**Impact:** Different file workflow - ascii-guard has stricter timing requirements.

---

### 5. **Summary File Timing**

**todo.ai:**
- Summary can be created and edited at any time
- Can edit after prepare step
- No timing constraints

**ascii-guard:**
- **CRITICAL:** AI summary must be committed immediately
- **CRITICAL:** Prepare must run within 60 seconds of commit
- Script validates file age (< 60 seconds) to prevent reuse of old summaries
- This enforces fresh summary generation for each release

**Impact:** ascii-guard prevents agents from reusing stale summaries.

---

### 6. **Project-Specific Content**

**todo.ai:**
- Generic release process
- No project-specific requirements
- Works for any project type

**ascii-guard:**
- **Python Environment Management** section (lines 26-93)
  - uv package management rules
  - Virtual environment requirements
  - Pre-commit hook integration
- **GitHub Actions Integration** section (lines 413-435)
  - PyPI publishing via trusted publishing
  - Workflow explanation
- **Package Building** requirements
- **Version Files:** `pyproject.toml` and `src/ascii_guard/__init__.py`

**Impact:** ascii-guard includes project-specific requirements that don't apply to todo.ai.

---

### 7. **Workflow Detail Level**

**todo.ai:**
- **Step 1:** Generate summary → save to RELEASE_SUMMARY.md
- **Step 2:** Run prepare with `--summary` flag
- **Step 3:** Run execute
- High-level, minimal detail

**ascii-guard:**
- **Step 0:** CI/CD check (mandatory)
- **Step 1:** Generate AI summary → commit immediately
- **Step 2:** Prepare (with timing validation)
- **Step 3:** Review & Edit (detailed editing options)
- **Step 4:** Execute
- Includes:
  - Complete workflow examples
  - AI Agent Workflow section
  - Natural language triggers
  - Common edits guidance
  - Error troubleshooting

**Impact:** ascii-guard provides much more detailed guidance for agents.

---

### 8. **Safeguards and "NEVER DO" Rules**

**todo.ai:**
- ❌ No explicit safeguards section
- ❌ No "NEVER DO" rules

**ascii-guard:**
- ✅ **Safeguards** section (lines 439-458)
- ✅ Explicit "❌ NEVER DO THIS" list:
  - Don't modify release.sh logic
  - Don't bypass CI/CD
  - Don't publish to PyPI manually
  - Don't push tags manually
- ✅ Explicit "✅ ALWAYS DO THIS" list:
  - Always create AI summary first
  - Always commit summary immediately
  - Always run prepare within 60 seconds
  - Always wait for human review

**Impact:** ascii-guard has explicit guardrails to prevent mistakes.

---

### 9. **Version Override**

**todo.ai:**
- ⚠️ Not explicitly mentioned in the rule

**ascii-guard:**
- ✅ **Step 3** includes version override option
- ✅ Natural language triggers documented
- ✅ `--set-version` command explained
- ✅ Validation rules explained

**Impact:** ascii-guard provides clearer guidance on version overrides.

---

### 10. **Release Notes Editing**

**todo.ai:**
- ✅ Mentions editing RELEASE_SUMMARY.md after prepare
- ⚠️ Minimal detail on editing process

**ascii-guard:**
- ✅ **Step 3: Review & Edit Release Notes** (lines 293-359)
- ✅ Explains two-file system (AI summary vs release notes)
- ✅ Three editing options documented
- ✅ Common edits guidance
- ✅ Clear explanation: "THIS IS THE FILE TO REVIEW/EDIT"

**Impact:** ascii-guard provides much clearer editing guidance.

---

## Summary of Critical Differences

### Missing in todo.ai releases.mdc:

1. ❌ **No explicit human gate enforcement** - doesn't strongly emphasize stopping after prepare
2. ❌ **No CI/CD check requirement** - doesn't prevent releases when CI/CD is broken
3. ❌ **No error handling guidelines** - no policy on what to do when errors occur
4. ❌ **No safeguards section** - no explicit "NEVER DO" rules
5. ❌ **No timing constraints** - doesn't prevent reuse of stale summaries
6. ⚠️ **Less detailed workflow** - minimal guidance compared to ascii-guard

### Unique to ascii-guard (project-specific):

1. ✅ Python/uv environment management rules
2. ✅ GitHub Actions/PyPI publishing workflow
3. ✅ Package building requirements
4. ✅ Project-specific file locations

### Recommendations for todo.ai:

1. **Add explicit human gate enforcement:**
   - Add section emphasizing "STOP and wait" after prepare
   - Add warnings about never auto-executing

2. **Add CI/CD check (if applicable):**
   - If todo.ai has CI/CD, add mandatory check requirement
   - If not, document why it's not needed

3. **Add error handling section:**
   - Define what counts as an error
   - Provide error response examples
   - Document recovery process

4. **Add safeguards section:**
   - List of "NEVER DO" rules
   - List of "ALWAYS DO" rules

5. **Consider timing constraints:**
   - If stale summary reuse is a concern, add timing validation
   - Document when summaries should be regenerated

6. **Expand workflow detail:**
   - Add more examples
   - Document common scenarios
   - Provide troubleshooting guidance

---

## File Structure Comparison

### todo.ai releases.mdc:
```
1. Front matter (description, alwaysApply)
2. Step 1: Generate summary → RELEASE_SUMMARY.md
3. Step 2: Prepare with --summary flag
4. Step 3: Execute
5. CRITICAL note about RELEASE_SUMMARY.md being source of truth
```

### ascii-guard ascii-guard-releases.mdc:
```
1. CRITICAL: Two-Phase Process with Human Gate
2. Python Environment Management (project-specific)
3. Step 0: MANDATORY CI/CD Check
4. CRITICAL: Error Handling During Releases
5. Step 1: Generate AI Release Summary
6. Step 2: Prepare Release
7. Step 3: Review & Edit Release Notes
8. Step 4: Execute Release
9. Complete Workflow Example
10. Key GitHub Actions Integration
11. Safeguards
12. Error Handling (troubleshooting)
13. Version Numbering
14. Files and Tracking
15. AI Agent Workflow
```

---

## Conclusion

**ascii-guard's release.mdc is significantly more comprehensive** with:
- ✅ Explicit human gate enforcement
- ✅ CI/CD check requirements
- ✅ Comprehensive error handling
- ✅ Detailed safeguards
- ✅ Timing constraints to prevent stale summaries
- ✅ Extensive workflow examples

**todo.ai's release.mdc is more concise** but lacks:
- ❌ Explicit safeguards
- ❌ Error handling guidance
- ❌ CI/CD requirements
- ❌ Strong human gate enforcement

**Recommendation:** todo.ai should adopt the safeguards, error handling, and human gate emphasis from ascii-guard, while keeping the simpler file workflow that works for its use case.
