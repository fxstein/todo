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
