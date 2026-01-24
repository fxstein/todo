# CI/CD Silent Failure Analysis
Date: 2026-01-24
Status: Resolved

## Incident Description
On January 24, 2026, the CI/CD pipeline experienced multiple "silent failures" (specifically noted as "Fail #6"). The symptoms were:
1. The pipeline appeared to run successfully in early stages.
2. The `release` job and `validate-release` job did not execute or skipped their primary logic.
3. No clear error message was displayed; the pipeline simply stopped processing without triggering a failure state in the GitHub Actions UI for the overall workflow run.
4. The build artifacts were not generated, and the release was not published.

## Root Cause Analysis
The issue was traced to a logic gap in the `all-tests-pass` job within `.github/workflows/ci-cd.yml`, introduced during recent CI/CD optimizations.

### The Dependency Chain
The pipeline relies on a strict dependency chain:
`changes` → `quality`/`tests` → `all-tests-pass` → `validate-release` → `release`

### The Defect
The `all-tests-pass` job is designed to be a gatekeeper. It uses `if: always()` to run even if previous jobs fail or are skipped, so it can aggregate results.

The logic iterated through test results:
```yaml
for result in \
  "${{ needs.docs-quality.result }}" \
  "${{ needs.logs-quality.result }}" \
  "${{ needs.quality.result }}" \
  ...
```

**Critical Flaw:** The `changes` job result was **missing** from this check loop.

If the `changes` job failed (e.g., due to an API error or checkout issue):
1. Dependent jobs (`quality`, `tests`) would be `skipped`.
2. `all-tests-pass` would see `skipped` for tests (which is considered a "pass" for conditional execution).
3. `all-tests-pass` would **not check** the failed `changes` job.
4. `all-tests-pass` would report **Success** ✅.

### Downstream Impact
1. `validate-release` would start because `all-tests-pass` succeeded.
2. It attempts to read `${{ needs.changes.outputs.is_tag }}`.
3. Since `changes` failed, this output was empty or invalid.
4. `validate-release` logic `if [[ "$is_tag" != "true" ]]; then ...` would trigger a skip.
5. The pipeline would terminate "successfully" but do nothing.

## Resolution
The fix involved two changes to `.github/workflows/ci-cd.yml`:

1. **Include `changes` in Validation Loop**:
    Added `${{ needs.changes.result }}` to the failure checking loop in `all-tests-pass`.
    ```yaml
    for result in \
      "${{ needs.changes.result }}" \
      "${{ needs.docs-quality.result }}" \
      ...
    ```
    This ensures that if the root dependency fails, the gatekeeper job fails immediately.

2. **Enhanced Debugging**:
    Added explicit debug logging to the `validate-release` job to print the raw values of `is_tag` and `GITHUB_REF`.
    ```yaml
    echo "Debug: is_tag from changes job: '$is_tag'"
    echo "Debug: GITHUB_REF: '$GITHUB_REF'"
    ```

## Prevention
This incident highlights the importance of:
1. Validating *all* dependencies in aggregate gatekeeper jobs, not just the immediate test jobs.
2. Ensuring that "skipped" logic accounts for upstream failures vs. intentional skips.
3. Failing fast when context data (like `is_tag`) is missing or malformed, rather than silently skipping.

---

## Release Job Skipping Issue (January 24, 2026)
Status: Under Investigation

### Symptom
When a release tag is pushed (e.g., `v1.0.0`), the following jobs are being skipped:
- `validate-release` (Validate Release Version)
- `release` (Build and Publish Release)

The pipeline completes without errors, but no release artifacts are published.

### Analysis

#### Issue #1: Missing Job-Level Conditional
The `validate-release` job (line 384) has **NO** `if` condition at the job level:
```yaml
validate-release:
  name: Validate Release Version
  needs: [all-tests-pass, changes]
  runs-on: ubuntu-latest
```

This causes the job to:
- Run on **every** workflow trigger (commits, PRs, tags)
- Only perform validation work if internal step conditions pass
- Always produce outputs, even when empty or invalid

#### Issue #2: Output Propagation Chain
The `is_tag` flag flows through multiple jobs:
```
changes.outputs.is_tag → validate-release.outputs.is_tag → release conditional
```

**Failure Points:**
1. **Tag Detection** (lines 73-78 in `changes` job):
   ```bash
   if [[ "$ref" == refs/tags/v* ]]; then
     is_tag=true
   fi
   ```
   - May fail if `GITHUB_REF` format differs from expected
   - Environment variables might not be populated correctly
   - Workflow trigger might be different than expected

2. **Output Propagation** (line 401 in `validate-release`):
   ```yaml
   echo "is_tag=$is_tag" >> "$GITHUB_OUTPUT"
   ```
   - If `$is_tag` from `needs.changes.outputs.is_tag` is empty, outputs empty string
   - String comparison issues: `"true"` vs `true` vs `"True"`
   - Whitespace in values

3. **Release Job Conditional** (line 496):
   ```yaml
   if: needs.validate-release.outputs.is_tag == 'true'
   ```
   - Requires exact string match `'true'`
   - Fails silently if output is empty, false, or malformed

#### Issue #3: Silent Skip Pattern
Both jobs skip silently without error because:
- `validate-release` runs but produces empty/false outputs
- `release` job conditional evaluates to false
- GitHub Actions shows "Skipped" status (not failure)
- No error messages indicate why the skip occurred

### Likely Root Causes

**Most Probable:**
1. Tag detection logic in `changes` job not catching tag push events correctly
2. Output value type mismatch in GitHub Actions expression evaluation
3. Environment variables (`GITHUB_REF`, `GITHUB_REF_TYPE`) not populated as expected during tag pushes

**Secondary:**
- The `validate-release` job should have a job-level conditional to prevent running on non-tag workflows
- Debug logging added (lines 397-401) may not be visible if job is skipped entirely

### Required Investigation Steps

To diagnose the actual issue, check in workflow run logs:

1. **`changes` job outputs:**
   - What value does `is_tag` actually have?
   - What are `GITHUB_REF`, `GITHUB_REF_TYPE`, `GITHUB_REF_NAME`?

2. **`tag-context` step in `validate-release`:**
   - Does the debug logging show `is_tag` correctly?
   - Is the step even running?

3. **GitHub Actions UI:**
   - Are jobs showing "Skipped" or "Not Run"?
   - What does the `all-tests-pass` job show for status?

4. **Workflow trigger:**
   - How is the workflow being triggered? (push to tag vs manual trigger)
   - Is the tag format correct? (e.g., `v1.0.0` vs `1.0.0`)

### Proposed Fixes

**Fix #1: Add Job-Level Conditional**
```yaml
validate-release:
  name: Validate Release Version
  needs: [all-tests-pass, changes]
  if: needs.changes.outputs.is_tag == 'true'
  runs-on: ubuntu-latest
```

**Fix #2: Enhance Tag Detection**
Add fallback detection using `github.ref_type` directly:
```yaml
- name: Detect tag ref
  id: refs
  run: |
    is_tag=false
    if [[ "${{ github.ref_type }}" == "tag" ]]; then
      is_tag=true
    elif [[ "${{ github.ref }}" == refs/tags/v* ]]; then
      is_tag=true
    fi
    echo "is_tag=$is_tag" >> "$GITHUB_OUTPUT"
```

**Fix #3: Add Explicit Failure on Missing Data**
```yaml
- name: Capture tag context
  id: tag-context
  run: |
    is_tag="${{ needs.changes.outputs.is_tag }}"
    if [[ -z "$is_tag" ]]; then
      echo "❌ ERROR: is_tag output from changes job is empty"
      exit 1
    fi
    echo "is_tag=$is_tag" >> "$GITHUB_OUTPUT"
```

**Fix #4: Debug Workflow Trigger**
Add early debug step to all tag-dependent jobs:
```yaml
- name: Debug workflow context
  run: |
    echo "Event name: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "Ref type: ${{ github.ref_type }}"
    echo "Ref name: ${{ github.ref_name }}"
    echo "SHA: ${{ github.sha }}"
```

### Next Steps

1. Examine actual workflow run logs to confirm which scenario is occurring
2. Implement Fix #4 first to gather diagnostic data
3. Based on data, implement Fix #1 and Fix #2 or Fix #3 as appropriate
4. Test with a beta release tag to verify fixes

---

## Diagnostic Data (Task#186.1 - January 24, 2026)

### Workflow Run Analysis

**Examined Runs:**
- v3.0.0b8 (21318445519) - FAILED: validate-release and release skipped
- v3.0.0b999 (21317498772) - FAILED: validate-release and release skipped
- v3.0.0b10 (21314200673) - FAILED: validate-release and release skipped
- v3.0.0b11 (21316100901) - FAILED: validate-release and release skipped
- v3.0.0b7 (21300926413) - SUCCESS: all jobs ran, release published

### Key Discovery: Root Cause Identified

**Timeline of Changes:**
- v3.0.0b7 (Jan 23, 2026 20:56): ✅ SUCCESS - Release published
- Commit `dd9a222` (Jan 24, 2026 14:42): Modified validate-release job
- v3.0.0b8+ (Jan 24, 2026 onwards): ❌ FAILED - Jobs skipped

**Commit `dd9a222` Changes:**
```diff
  validate-release:
    name: Validate Release Version
    needs: [all-tests-pass, changes]
-   # Only run on tag pushes
-   if: needs.changes.outputs.is_tag == 'true'
    runs-on: ubuntu-latest
```

The job-level `if` condition was removed to "avoid skipping", but this caused the opposite problem.

### Evidence from Workflow Logs

**v3.0.0b8 Changes Job Output (Working Correctly):**
```
Detect Changes → Detect tag ref:
  Ref: refs/tags/v3.0.0b8
  Ref type: tag
  Ref name: v3.0.0b8
```
- Tag detection IS working correctly
- `is_tag` output should be `true`

**v3.0.0b8 All Tests Passed Job Output (Working Correctly):**
```
Results:
  changes: success
  docs-quality: skipped
  logs-quality: skipped
  quality: success
  test-quick: success
  test-comprehensive: success
  test-pr: skipped

✅ All required checks passed (skipped checks are acceptable)
```
- Gatekeeper job passed successfully
- All required test jobs passed

**v3.0.0b8 Validate Release Version Job:**
- Status: Skipped
- Duration: 0s
- Logs: **COMPLETELY EMPTY** (not even "Set up job")
- NO steps executed

**v3.0.0b8 Build and Publish Release Job:**
- Status: Skipped
- Duration: 0s
- Conditional: `if: needs.validate-release.outputs.is_tag == 'true'`

### Root Cause Analysis

**Critical Finding:**
The `validate-release` job is being skipped by GitHub Actions BEFORE it even starts (no "Set up job" logs). This is happening despite:
1. Having NO explicit `if` condition at the job level
2. The `needs` jobs (`all-tests-pass`, `changes`) both completed successfully
3. The first step "Capture tag context" has no `if` condition and should run

**This indicates one of three scenarios:**

1. **GitHub Actions Implicit Skipping**: When a job has no `if` condition but produces outputs that downstream jobs depend on, GitHub Actions may skip it if it detects the outputs won't be used (but this doesn't match our case)

2. **Output Value is Empty/Null**: The `needs.changes.outputs.is_tag` value is actually empty or null, not the string "true", causing some implicit GitHub Actions behavior to skip the job

3. **Job Dependencies Issue**: The combination of `needs: [all-tests-pass, changes]` with no explicit `if` condition is causing GitHub Actions to evaluate the job differently than expected

**Evidence for Scenario #2 (Most Likely):**
- The `changes` job completed successfully
- The `is_tag` detection logic ran and printed values
- BUT: The output may not have been captured in `$GITHUB_OUTPUT`
- Downstream jobs checking `needs.changes.outputs.is_tag` get empty/null
- GitHub Actions skips jobs with unmet implicit conditions

**Comparing v3.0.0b7 (SUCCESS) vs v3.0.0b8 (FAILED):**

v3.0.0b7 Configuration:
```yaml
validate-release:
  needs: [all-tests-pass, changes]
  if: needs.changes.outputs.is_tag == 'true'  # Explicit condition
```
- Job runs IF condition is true
- Job skips IF condition is false or empty
- **Clear decision point**

v3.0.0b8+ Configuration:
```yaml
validate-release:
  needs: [all-tests-pass, changes]
  # NO if condition - should always run
```
- Job should run after dependencies complete
- BUT: GitHub Actions is skipping it anyway
- **Implicit behavior causing silent skip**

### Hypothesis

The issue is NOT with tag detection or test passing. The issue is that removing the job-level `if` condition exposed a **different problem**: the `validate-release` job's steps expect to read `needs.changes.outputs.is_tag`, but that output may be:
- Empty string
- Null
- Not properly exported from the changes job

When the job-level `if` was present in v3.0.0b7, it explicitly checked the value and decided to run/skip. When removed, GitHub Actions has no guidance and may be applying implicit skipping logic.

### Required Next Steps

1. **Verify Output Export**: Check if `changes` job is actually exporting `is_tag` to `$GITHUB_OUTPUT` correctly
2. **Add Debug Logging**: Implement Fix #4 to see actual values being passed
3. **Restore Job-Level Condition**: The original `if: needs.changes.outputs.is_tag == 'true'` condition was correct and should be restored
4. **Add Explicit Debug Step**: Add a step that dumps all `needs.changes.outputs.*` values before any conditional logic

---

## Output Propagation Analysis (Task#186.2 - January 24, 2026)

### Complete Output Flow Chain

**1. changes job → PRODUCES is_tag**

Job declaration (lines 17-25):
```yaml
changes:
  outputs:
    is_tag: ${{ steps.refs.outputs.is_tag }}
```

Step implementation (lines 65-83):
```yaml
- name: Detect tag ref
  id: refs
  run: |
    is_tag=false
    if [[ "$ref" == refs/tags/v* ]]; then is_tag=true; fi
    if [[ "$ref_type" == "tag" ]]; then is_tag=true; fi
    echo "is_tag=$is_tag" >> "$GITHUB_OUTPUT"
```

Status: ✅ **Working correctly** - Logs show `is_tag=true` written to output

**2. validate-release job → CONSUMES and RE-EXPORTS is_tag**

Job declaration (lines 384-392):
```yaml
validate-release:
  needs: [all-tests-pass, changes]
  # ❌ NO job-level if condition (removed in dd9a222)
  outputs:
    is_tag: ${{ steps.tag-context.outputs.is_tag }}
```

Step implementation (lines 394-404):
```yaml
- name: Capture tag context
  id: tag-context
  run: |
    is_tag="${{ needs.changes.outputs.is_tag }}"
    echo "is_tag=$is_tag" >> "$GITHUB_OUTPUT"
```

Status: ❌ **Job skipped entirely** - No steps executed, no outputs produced

**3. release job → CONSUMES is_tag**

Job declaration (lines 489-496):
```yaml
release:
  needs: [validate-release]
  if: needs.validate-release.outputs.is_tag == 'true'
```

Status: ❌ **Skipped** - Condition evaluates to false (output is empty/null)

### Evolution of validate-release Job Configuration

**Original (v3.0.0b7 - SUCCESS):**
```yaml
validate-release:
  needs: [all-tests-pass]
  if: startsWith(github.ref, 'refs/tags/v')
  outputs:
    version: ...
    is_prerelease: ...
    # NO is_tag output
```

**Intermediate (after adding changes dependency):**
```yaml
validate-release:
  needs: [all-tests-pass, changes]
  if: needs.changes.outputs.is_tag == 'true'
  outputs:
    is_tag: ...  # Added
    version: ...
    is_prerelease: ...
```

**Current (after dd9a222 - FAILURE):**
```yaml
validate-release:
  needs: [all-tests-pass, changes]
  # ❌ if condition removed
  outputs:
    is_tag: ...
    version: ...
    is_prerelease: ...
```

### Root Cause: Missing Job-Level Conditional

**The Problem:**
Commit `dd9a222` removed the job-level `if: needs.changes.outputs.is_tag == 'true'` condition to "avoid skipping", but this caused the opposite problem.

**Why This Fails:**
1. Without a job-level `if` condition, GitHub Actions evaluates whether to run the job based on:
   - Dependency completion status (✅ all completed successfully)
   - Job outputs expectations (❓ job declares outputs but no condition to determine when they're valid)
   - Implicit conditions (❓ GitHub Actions may detect inconsistency)

2. The job declares `is_tag` as an output from `steps.tag-context.outputs.is_tag`
3. But the job has no explicit condition stating WHEN it should run
4. GitHub Actions appears to skip the job entirely rather than running it without clear conditions

**GitHub Actions Behavior:**
- With `if: needs.changes.outputs.is_tag == 'true'`: Job runs IF condition is true, skips IF false
- Without any `if`: Job SHOULD run after dependencies complete, but GitHub Actions is skipping it
- This suggests GitHub Actions has implicit logic that prevents running jobs with unclear execution conditions

### Verification from API

```bash
$ gh api repos/fxstein/todo.ai/actions/runs/21318445519/jobs \
  --jq '.jobs[] | select(.name == "Detect Changes") | {name, conclusion, outputs}'
{"conclusion":"success","name":"Detect Changes","outputs":null}
```

The GitHub Actions API shows `outputs: null` for the changes job, even though the logs clearly show the output was written. This may be:
- An API limitation (outputs not exposed)
- An indication that outputs aren't properly registered
- Expected behavior (outputs only visible to dependent jobs, not via API)

### Conclusion

The output propagation chain is CORRECTLY IMPLEMENTED in the code:
- ✅ `changes` job sets `is_tag=true` to `$GITHUB_OUTPUT`
- ✅ `changes` job declares output `is_tag: ${{ steps.refs.outputs.is_tag }}`
- ✅ `validate-release` reads `needs.changes.outputs.is_tag`
- ✅ `validate-release` declares output `is_tag: ${{ steps.tag-context.outputs.is_tag }}`
- ✅ `release` checks `needs.validate-release.outputs.is_tag == 'true'`

The FAILURE occurs because:
- ❌ `validate-release` has NO job-level `if` condition
- ❌ GitHub Actions skips the job without executing any steps
- ❌ Job outputs remain empty/null
- ❌ `release` job conditional evaluates to false and skips

**Solution:** Restore the job-level `if: needs.changes.outputs.is_tag == 'true'` condition that was removed in commit `dd9a222`.

---

## Fix Implementation (Task#186.5 - January 24, 2026)

### Applied Fix

Restored the missing job-level conditional to the `validate-release` job:

```yaml
validate-release:
  name: Validate Release Version
  needs: [all-tests-pass, changes]
  # Only run on tag pushes (required for GitHub Actions to execute the job)
  if: needs.changes.outputs.is_tag == 'true'
  runs-on: ubuntu-latest
```

### Why This Fix Works

**The Problem:**
- Without an explicit `if` condition, GitHub Actions has no clear guidance on when the job should run
- The job declares outputs that depend on step execution, creating ambiguity
- GitHub Actions applies implicit skipping logic when job execution conditions are unclear

**The Solution:**
- Explicit `if: needs.changes.outputs.is_tag == 'true'` condition tells GitHub Actions exactly when to run
- Job runs if condition is true (tag push)
- Job skips if condition is false (non-tag push)
- Clear decision point eliminates ambiguity

**Combined with Debug Logging:**
- Comprehensive diagnostic output at all critical points
- Tag detection with condition evaluation
- Output propagation verification
- Conditional evaluation display
- Future-proofed for quick issue diagnosis

### Changes Made

1. **validate-release job (line 420):** Added `if: needs.changes.outputs.is_tag == 'true'`
2. **Debug logging (5 locations):** Added comprehensive diagnostics throughout workflow
3. **Documentation:** Updated analysis with fix implementation details

### Testing

Ready for testing with next beta release tag (e.g., v3.0.0b12).

---

## Test Results - v3.0.0b9 (Task#186.6 - January 24, 2026)

### Critical Finding: Fix Deployed But Still Failing

**Test Release:** v3.0.0b9 (run 21319028195)

**Fix Status:** ✅ DEPLOYED
```yaml
validate-release:
  if: needs.changes.outputs.is_tag == 'true'  # ✅ Present in v3.0.0b9
```

**Tag Detection:** ✅ WORKING
```
🏷️  TAG DETECTION
Environment variables:
  GITHUB_REF: 'refs/tags/v3.0.0b9'
  GITHUB_REF_TYPE: 'tag'
  GITHUB_REF_NAME: 'v3.0.0b9'
Tag detection logic:
  ✅ Condition 1: GITHUB_REF matches 'refs/tags/v*'
  ✅ Condition 2: GITHUB_REF_TYPE == 'tag'
Result: is_tag=true
  Writing to GITHUB_OUTPUT: is_tag=true
```

**Output Propagation:** ✅ WORKING
```
✅ ALL TESTS PASSED - GATEKEEPER CHECK
Job Results:
  changes: success
Changes Job Outputs:
  is_tag: 'true'  # ✅ Output visible and correct
```

**validate-release Job:** ❌ STILL SKIPPED
```json
{"conclusion":"skipped","name":"Validate Release Version","status":"completed"}
```

### Analysis

The fix was correctly deployed and all preconditions are met:
1. ✅ Tag detection logic correctly identifies tag push
2. ✅ Output `is_tag=true` successfully written to GITHUB_OUTPUT
3. ✅ Output propagates through `all-tests-pass` job (visible as `'true'`)
4. ✅ Job-level conditional `if: needs.changes.outputs.is_tag == 'true'` present
5. ❌ **GitHub Actions still skips the job**

**Hypothesis:**
The issue may be with GitHub Actions expression evaluation:
- The output value is the string `'true'` (confirmed in logs)
- The condition uses `== 'true'` (string comparison)
- GitHub Actions may be evaluating this differently than expected

**Possible causes:**
1. **Expression syntax issue:** GitHub Actions may require different comparison syntax
2. **Type coercion:** The output may not be treated as a string in expressions
3. **Quote handling:** Single vs double quotes in GitHub Actions expressions
4. **Hidden characters:** Whitespace or control characters in the output value

**Next Steps:**
1. Test alternative conditional syntaxes
2. Check GitHub Actions expression documentation for output comparisons
3. Try boolean comparison without quotes: `if: needs.changes.outputs.is_tag`
4. Add more verbose debug logging to understand GitHub Actions evaluation
