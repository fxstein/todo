# Beta Strategy Review & Recommendations

**Document Date:** December 15, 2025
**Reference Document:** `docs/design/BETA_PRERELEASE_STRATEGY.md`
**Status:** REVIEW_COMPLETED

---

## 1. Executive Summary

The proposed beta strategy provides a comprehensive plan for introducing pre-release cycles to `todo.ai`. It aligns closely with industry standards (PEP 440, SemVer) and effectively addresses the project's specific constraints (CLI tool, MCP integration). The strategy is **approved for implementation**, provided the specific technical gaps regarding dependency resolution, version parsing reliability, and release gating are addressed as detailed below.

## 2. Strengths & Best Practice Alignment

* **Standard Compliance:** accurately distinguishes between Git tags (SemVer) and Python packages (PEP 440) with a clear mapping strategy. This is essential for compatibility with the Python tooling ecosystem.
* **Release Channels:** The "Alpha (Internal) → Beta (Early Adopters) → RC (Stability) → Stable" pipeline represents a gold standard for robust software delivery.
* **Tooling Awareness:** The explicit inclusion of modern Python tooling (`uv`, `pipx`) in installation instructions demonstrates strong user empathy and forward-looking design.
* **Risk Management:** The emphasis on "Data Safety" (backups) and defined "Rollback" procedures (yanking, hotfixes) indicates a mature approach to stability.

## 3. Identified Gaps & Risks

### A. TestPyPI Dependency Resolution (Critical)
**Context:** Section 3.3 / 4.2 suggests publishing Alpha releases to TestPyPI.
**Issue:** TestPyPI is a separate package index. If `todo.ai` depends on packages (e.g., `rich`, `typer`) that exist on PyPI but are *not* on TestPyPI, installation will fail if users only provide `--index-url https://test.pypi.org/simple/`.
**Impact:** Alpha testers will encounter "package not found" errors, blocking testing.
**Best Practice:** Use `--extra-index-url` for TestPyPI while keeping the primary index as PyPI, allowing the installer to resolve dependencies from the main repository.

### B. Manual Version String Parsing
**Context:** Section 4.1 proposes using Bash `sed` and regex to parse version numbers.
**Issue:** Parsing the complexity of SemVer and PEP 440 (e.g., `rc1` vs `rc.1`, post-releases, dev-releases) using Bash regex is fragile and prone to edge-case errors.
**Risk:** Malformed tags could break the release pipeline or result in invalid package versions.
**Recommendation:** Use a small Python script (leveraging the standard `packaging` library) within the release workflow to handle version validation and increment logic.

### C. Human Gate for Pre-releases
**Context:** Section 3.1 outlines triggers for Alpha/Beta phases.
**Gap:** It is unclear if Alpha releases are subject to the project's mandatory **"Two-Phase Release Process"** (Prepare -> Human Gate -> Execute).
**Recommendation:** Explicitly state that *all* releases, including Alphas, must pass the Human Gate to prevent accidental publication, or define a specific exemption protocol for Alphas if continuous deployment is desired.

### D. MCP Server Automated Testing
**Context:** Section 5 relies on "Manual workflows" and "Real-world usage" for MCP testing.
**Gap:** MCP is a protocol. Relying solely on manual testing is risky as different clients (Cursor vs. Claude Desktop) may vary in implementation.
**Recommendation:** Implement "Headless" MCP testing—a test suite acting as a generic MCP client to verify JSON-RPC responses independent of a specific UI.

### E. Feature Flags Implementation
**Context:** Section 2.4 mentions feature flags (e.g., `TODOAI_EXPERIMENTAL_MCP_V2=1`).
**Gap:** The document lacks implementation details for how these flags will be managed in the codebase.
**Recommendation:** Include a centralized `FeatureFlag` utility class in `config.py` to manage these toggles consistently.

## 4. Implementation Recommendations

### 4.1 Refined Installation Commands

Update the Alpha installation instructions to ensure dependencies resolve correctly:

```bash
# Corrected Command (uses extra-index-url)
uv tool install --index-url https://pypi.org/simple/ --extra-index-url https://test.pypi.org/simple/ --prerelease=allow todo-ai
```

### 4.2 Release Process Adjustments

1. **GitHub "Latest" Tag:** Ensure the GitHub Actions workflow marks Alpha/Beta/RC releases as "Prerelease". This prevents them from being identified as the "Latest" release in the GitHub UI, which could confuse users.
2. **Release Note Context:** For Beta/RC releases, the automated notes should ideally highlight "Changes since last Stable" rather than just "Changes since last Beta" to provide testers full context, or clearly link to the full changelog.

### 4.3 Version Management

To minimize drift risk between `pyproject.toml`, `todo.ai`, and `__init__.py`:
* **Source of Truth:** Designate `pyproject.toml` as the single source of truth.
* **Automation:** Utilize a tool like `bump-my-version` or a custom Python script during the `prepare` phase to synchronously update all version occurrences, rather than independent `sed` commands.
