# PyPI Trusted Publisher Setup for todo.ai

**Date:** December 16, 2025
**Status:** Required for v3.0.0b1 release

---

## Overview

This guide explains how to set up PyPI's Trusted Publisher feature for todo.ai, which allows GitHub Actions to publish packages **without requiring API tokens**. This is more secure and eliminates token management.

**Benefits of Trusted Publisher:**
- ✅ No API tokens to manage or rotate
- ✅ More secure (uses OpenID Connect - OIDC)
- ✅ Automatic authentication from GitHub Actions
- ✅ PyPI's recommended authentication method

---

## Prerequisites

- PyPI account (free at https://pypi.org/account/register/)
- Access to https://github.com/fxstein/todo.ai repository
- Admin permissions on the PyPI project (for adding trusted publishers)

---

## Step 1: Create PyPI Account (If Needed)

1. Go to https://pypi.org/account/register/
2. Create account with email and password
3. Verify email address
4. Enable 2FA (highly recommended)

---

## Step 2: Create PyPI Project

**Option A: Reserve the name first (before first release)**

1. Go to https://pypi.org/manage/projects/
2. Click "Your projects"
3. Look for "todo-ai" to verify name is available
4. The project will be created automatically on first successful publish

**Option B: Create via first release**

- PyPI will auto-create the project when GitHub Actions publishes for the first time
- You must set up trusted publisher first (Step 3)

---

## Step 3: Add GitHub as Trusted Publisher

This is the **critical step** that enables OIDC authentication.

### For a New Project (Pending Publisher)

If the project doesn't exist yet:

1. Go to https://pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name:** `todo-ai`
   - **Owner:** `fxstein`
   - **Repository name:** `todo.ai`
   - **Workflow name:** `release.yml`
   - **Environment name:** (leave blank)
4. Click "Add"

**Result:** When GitHub Actions first publishes, PyPI will automatically create the project and trust this workflow.

### For an Existing Project

If the project already exists:

1. Go to https://pypi.org/manage/project/todo-ai/settings/publishing/
2. Scroll to "Add a new publisher"
3. Fill in the form:
   - **Owner:** `fxstein`
   - **Repository name:** `todo.ai`
   - **Workflow name:** `release.yml`
   - **Environment name:** (leave blank)
4. Click "Add"

**Result:** GitHub Actions can now publish to this project.

---

## Step 4: Verify GitHub Actions Workflow

The workflow is already configured correctly in `.github/workflows/release.yml`:

```yaml
jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write  # ← Required for OIDC

    steps:
      # ... build steps ...

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1  # ← Uses OIDC automatically
        with:
          print-hash: true
          verbose: true
```

**Key Points:**
- `id-token: write` permission enables OIDC
- `pypa/gh-action-pypi-publish` action handles OIDC authentication automatically
- No secrets or tokens needed in workflow

---

## Step 5: Test the Setup

After completing Steps 1-3, test with the beta release:

```bash
# Run the beta release
./release/release.sh --prepare --beta
# Review release notes
./release/release.sh --execute
```

**What happens:**
1. `release.sh` pushes tag (e.g., `v3.0.0b1`)
2. GitHub Actions workflow is triggered by tag push
3. Workflow builds Python package
4. Workflow authenticates to PyPI using OIDC (no tokens!)
5. Workflow publishes package to PyPI
6. Workflow attaches dist files to GitHub release

**Monitor progress:**
- GitHub Actions: https://github.com/fxstein/todo.ai/actions
- PyPI Project: https://pypi.org/project/todo-ai/

---

## Troubleshooting

### Error: "Repository is not trusted by PyPI"

**Cause:** Trusted publisher not configured on PyPI

**Fix:**
1. Go to https://pypi.org/manage/account/publishing/
2. Add pending publisher with exact details:
   - Owner: `fxstein`
   - Repository: `todo.ai`
   - Workflow: `release.yml`

### Error: "Token doesn't exist"

**Cause:** Old workflow configuration still references `PYPI_API_TOKEN`

**Fix:**
- Verify `.github/workflows/release.yml` uses `pypa/gh-action-pypi-publish@release/v1`
- Ensure no `TWINE_USERNAME` or `TWINE_PASSWORD` in workflow
- The current workflow is already updated correctly

### Error: "id-token permission required"

**Cause:** Workflow missing OIDC permission

**Fix:**
```yaml
permissions:
  id-token: write  # Add this
  contents: write
```

**Status:** Already configured correctly in current workflow

### Success But Package Not Found

**Cause:** May take a few minutes for PyPI to index new packages

**Fix:**
- Wait 2-5 minutes
- Check https://pypi.org/project/todo-ai/
- Try: `pip index versions todo-ai`

---

## Verification Checklist

Before attempting beta release, verify:

- [ ] PyPI account created and email verified
- [ ] 2FA enabled on PyPI (recommended)
- [ ] Pending publisher added on PyPI with correct details
- [ ] GitHub Actions workflow has `id-token: write` permission
- [ ] GitHub Actions workflow uses `pypa/gh-action-pypi-publish@release/v1`
- [ ] No API token secrets referenced in workflow

---

## References

- **PyPI Trusted Publishers:** https://docs.pypi.org/trusted-publishers/
- **GitHub OIDC:** https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- **PyPI Publish Action:** https://github.com/pypa/gh-action-pypi-publish

---

## Next Steps

After completing this setup:

1. ✅ Complete task #174 subtasks
2. ✅ Retry v3.0.0b1 beta release
3. ✅ Monitor GitHub Actions for successful publish
4. ✅ Verify package appears on PyPI
5. ✅ Test installation: `uv tool install --prerelease=allow todo-ai`

---

**Status:** Setup pending - complete Steps 1-3 before releasing
**Owner:** Release Engineering Team
**Created:** December 16, 2025
