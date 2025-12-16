# Beta and Pre-Release Strategy for todo.ai

**Document Version:** 2.0
**Date:** December 16, 2025
**Status:** APPROVED (Simplified)

---

## Executive Summary

This document outlines the strategy for implementing beta and pre-release capabilities in todo.ai's release process. Given that todo.ai is transitioning from a shell script to a Python-based tool with MCP server capabilities and cloud/AI integration, a robust pre-release strategy is essential for managing risk, gathering feedback, and ensuring quality.

**Approved Approach:** Implement a **simplified 2-tier release strategy** with beta and stable releases.

**Key Simplifications:**
- **2 tiers instead of 4:** Beta + Stable (eliminated Alpha and RC)
- **Single version format:** PEP 440 everywhere (no SemVer conversion)
- **Single PyPI target:** Main PyPI only (no TestPyPI)
- **No feature flags:** Use beta releases for testing (YAGNI principle)
- **Automatic enforcement:** Major releases must have beta first (script-enforced)

**Philosophy:** Keep it simple, make it bulletproof, integrate naturally with existing two-phase release process (prepare → execute).

**Document Version History:**
- v1.0: Initial strategy - 4-tier approach (December 15, 2025)
- v1.1: Incorporated review findings (December 15, 2025)
- v2.0: **Simplified to 2-tier approach based on recommendations** (December 16, 2025)
  - Reduced complexity by 40-50%
  - Eliminated Alpha, RC, TestPyPI, feature flags
  - Added automatic major release enforcement
  - Integrated with existing release process

**Related Documents:**
- `BETA_PRERELEASE_RECOMMENDATIONS.md` - Detailed simplification analysis and recommendations

---

## Approved Simplifications (v2.0)

After thorough analysis, the original 4-tier approach has been simplified to a 2-tier approach for todo.ai:

### What Changed

**Eliminated Complexity:**
- ✂️ **Alpha tier** → Use feature branches + CI for internal testing
- ✂️ **RC tier** → Iterating betas (b1, b2, b3...) serves this purpose
- ✂️ **TestPyPI** → Dependency resolution issues outweigh benefits
- ✂️ **Feature flags** → Beta releases serve the same purpose (YAGNI)
- ✂️ **Dual version formats** → PEP 440 everywhere (no SemVer conversion)

**Added Safety:**
- 🔒 **Automatic enforcement:** Major releases must have beta (script blocks without beta)
- 🔒 **Beta maturity warnings:** Script warns if releasing stable < 7 days after beta (but allows proceed)
- 🔒 **Pre-flight validation:** 6+ comprehensive checks before execute
- 🔒 **Automatic versioning:** Beta numbering determined automatically from GitHub releases

**Preserved:**
- ✅ **Two-phase process:** Prepare → Review → Execute (unchanged)
- ✅ **Human review gate:** Required for all releases (unchanged)
- ✅ **CI/CD integration:** All existing checks still run
- ✅ **Backward compatibility:** All existing commands still work

### Result

- **40-50% complexity reduction** in release process
- **60-70% error risk reduction** through automation
- **Zero breaking changes** to existing workflows
- **Self-contained** process that prevents common mistakes

### Recommended Release Structure

```
├── Beta (pre-release testing)
│   ├── Format: v1.0.0b1, v1.0.0b2, v1.0.0b3...
│   ├── Target: PyPI (pre-release flag)
│   ├── Purpose: External testing, feedback gathering
│   ├── Duration: 7+ days for major, 2-3 days for minor (recommended)
│   └── Installation: uv tool install --prerelease=allow todo-ai
│
└── Stable (production)
    ├── Format: v1.0.0
    ├── Target: PyPI (stable)
    ├── Purpose: General availability
    └── Installation: uv tool install todo-ai
```

**The following sections provide the background rationale for why beta releases matter and industry best practices that informed this strategy.**

---

## 1. Why Beta and Pre-Releases Matter

### 1.1 Industry Context

Modern software development, particularly in cloud and AI ecosystems, follows iterative release patterns:

- **Google Chrome:** Canary → Dev → Beta → Stable (4-tier)
- **Kubernetes:** Alpha → Beta → GA (3-tier)
- **Python:** Alpha → Beta → RC → Final (4-tier)
- **Node.js:** Experimental → Stable → LTS (3-tier)

### 1.2 Risk Management

**For todo.ai specifically:**

1. **Breaking Changes:** Migration from shell script to Python
2. **Data Integrity:** Task data must never be corrupted
3. **Integration Risk:** MCP server integration with Cursor/Claude Desktop
4. **Coordination Systems:** GitHub Issues, CounterAPI integration
5. **Multi-Platform:** macOS, Linux, Windows compatibility

**Without pre-releases:**
- Production users become unwitting beta testers
- Bugs reach stable channel immediately
- No rollback strategy for issues
- Reputation damage from broken releases

**With pre-releases:**
- Early adopters voluntarily test new features
- Issues caught before affecting stable users
- Gradual rollout reduces impact radius
- Clear communication of stability expectations

### 1.3 Cloud/AI Specific Considerations

**MCP Server Integration:**
- MCP protocol evolving (not yet 1.0)
- Cursor/Claude Desktop updates may break compatibility
- Need rapid iteration without destabilizing stable users

**AI Agent Usage:**
- Agents rely on tool stability for automation
- Breaking changes to command syntax impact agent workflows
- Need parallel testing channels (stable for production, beta for development)

**Cloud Coordination Services:**
- GitHub API changes require adaptation
- CounterAPI integration may need updates
- External service changes should be tested in isolation

---

## 2. Industry Best Practices

### 2.1 Semantic Versioning (SemVer) with Pre-release Tags

**Standard:** [Semantic Versioning 2.0.0](https://semver.org/)

**Format:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Examples:**
- `1.0.0-alpha.1` - First alpha of version 1.0.0
- `1.0.0-beta.2` - Second beta
- `1.0.0-rc.1` - First release candidate
- `1.0.0` - Stable release

**Rules:**
- Pre-release versions have lower precedence than stable
- `1.0.0-alpha < 1.0.0-beta < 1.0.0-rc < 1.0.0`
- Pre-release metadata can use dots: `1.0.0-beta.1 < 1.0.0-beta.2`

### 2.2 PEP 440 (Python Versioning)

**Standard:** [PEP 440](https://www.python.org/dev/peps/pep-0440/)

**Format:** `X.Y.Z[{a|b|rc}N]`

**Examples:**
- `1.0.0a1` - Alpha 1
- `1.0.0b2` - Beta 2
- `1.0.0rc1` - Release Candidate 1
- `1.0.0` - Final release

**PyPI Behavior:**
- Automatically detects pre-releases
- Users must explicitly opt-in: `pip install --pre todo-ai`
- `pip install todo-ai` only installs stable versions

**Recommendation for todo.ai:** Use PEP 440 format for Python package, SemVer for git tags.

### 2.3 Release Channels (Google Chrome Model)

**Tiers:**

| Channel | Purpose | Update Frequency | Users | Risk |
|---------|---------|------------------|-------|------|
| **Canary** | Bleeding edge | Daily/Hourly | Developers | High |
| **Dev** | New features | Weekly | Early adopters | Medium-High |
| **Beta** | Pre-release testing | 2-4 weeks | Testers | Medium |
| **Stable** | Production | 6-8 weeks | General public | Low |

**For todo.ai:**

| Channel | Version Format | Purpose | Users | Update Frequency |
|---------|---------------|---------|-------|------------------|
| **Alpha** | `1.0.0a1` | Internal testing, breaking changes OK | Maintainers | As needed |
| **Beta** | `1.0.0b1` | External testing, feature-complete | Early adopters | Regular |
| **RC** | `1.0.0rc1` | Final testing, no new features | Testers | Before stable |
| **Stable** | `1.0.0` | Production ready | All users | Regular cadence |

### 2.4 Cloud Native Patterns

**Progressive Rollout (Kubernetes/Cloud):**
1. Deploy to development cluster (alpha)
2. Deploy to staging cluster (beta)
3. Deploy to 10% production traffic (canary)
4. Deploy to 100% production (stable)

**For todo.ai (simplified):**
1. Develop features in feature branches (with CI/CD testing)
2. Publish beta to PyPI (pre-release flag)
3. Publish stable to PyPI

**Feature Testing Strategy:**
- ✂️ **No feature flags** - Use beta releases instead (YAGNI principle)
- Experimental features → Develop in branches, test with CI
- User testing → Release as beta
- Ready for production → Release as stable
- Simpler code, fewer edge cases, clearer user experience

### 2.5 AI/LLM Tool Best Practices

**OpenAI Plugin Evolution:**
- Beta plugins clearly marked in marketplace
- Separate testing environment for new features
- Versioned API endpoints for backward compatibility

**Anthropic MCP Tooling:**
- MCP protocol versions explicitly declared
- Tools declare compatibility requirements
- Graceful degradation for unsupported features

**For todo.ai MCP Server:**
- Declare MCP protocol version in server metadata
- Test against multiple MCP client versions
- Provide compatibility shims for older clients

---

## 3. Implementation Strategy for todo.ai (Simplified)

### 3.1 Release Lifecycle (2-Tier Approach)

**Phase 1: Beta (Pre-Release Testing)**

**Purpose:** External testing, feedback gathering, validation before stable release

**Audience:** Early adopters, power users, GitHub watchers

**Testing:** Real-world usage, edge cases, cross-platform compatibility, MCP integration

**Changes Allowed:** Bug fixes, minor features, documentation updates

**Duration:**
- **Major releases:** 7+ days recommended (warning if < 7 days, but allows proceed)
- **Minor releases:** 2-3 days recommended
- **Patch releases:** No beta needed (direct to stable)

**Trigger Conditions:**
- **Required:** Major version bumps (e.g., 2.0.0 → 3.0.0) - script enforces
- **Recommended:** Significant new features or refactoring
- **Optional:** Minor enhancements (user choice)
- **Not needed:** Bug fixes, documentation-only changes

**Criteria for Stable:**
- No critical bugs reported in beta period
- Positive or neutral feedback from beta users
- All planned features working as expected
- Migration path tested (if applicable)
- Recommended duration met (warning if not, but not blocking)

**Phase 2: Stable (General Availability)**

**Purpose:** Production-ready release for all users

**Audience:** All users

**Testing:** Production monitoring, user feedback, issue tracking

**Changes:**
- Patch releases (X.Y.Z+1) for bug fixes
- Minor releases (X.Y+1.0) for new features
- Major releases (X+1.0.0) for breaking changes

**Protection:**
- Major releases must have had at least one beta (script-enforced)
- All releases follow two-phase process (prepare → review → execute)
- Human gate required for all releases

### 3.2 Version Numbering Strategy (PEP 440 Only)

**Unified Format - PEP 440 Everywhere:**

```python
# pyproject.toml, todo_ai/__init__.py, Git tags all use same format
version = "1.0.0b1"  # Beta 1
version = "1.0.0b2"  # Beta 2
version = "1.0.0"    # Stable
```

**Git Tags:**

```bash
# PEP 440 format (with 'v' prefix for git convention)
v1.0.0b1   # Beta 1
v1.0.0b2   # Beta 2
v1.0.0     # Stable
```

**Version Examples:**

| Release Type | PyPI Version | Git Tag | Description |
|--------------|--------------|---------|-------------|
| First beta | `1.0.0b1` | `v1.0.0b1` | First beta for version 1.0.0 |
| Second beta | `1.0.0b2` | `v1.0.0b2` | Second beta (after fixes) |
| Stable | `1.0.0` | `v1.0.0` | Production release |

**Key Simplification:**
- No format conversion needed (just remove 'v' prefix for PyPI)
- No SemVer/PEP 440 dual tracking
- Single source of truth for version numbers

### 3.3 Installation Methods by Channel

**Beta Channel (Pre-Release):**
```bash
# Latest beta from PyPI (recommended)
uv tool install --prerelease=allow todo-ai

# Specific beta version
uv tool install todo-ai==1.0.0b1

# From Git tag (for testing unreleased code)
uv tool install git+https://github.com/fxstein/todo.ai.git@v1.0.0b1
```

**Stable Channel (Production):**
```bash
# Latest stable (recommended)
uv tool install todo-ai

# Specific stable version
uv tool install todo-ai==1.0.0

# Upgrade to latest stable
uv tool upgrade todo-ai
```

**Alternative Installation Tools:**

<details>
<summary>Using pipx or pip</summary>

```bash
# Beta with pipx
pipx install --pre todo-ai

# Stable with pipx
pipx install todo-ai

# Beta with pip
pip install --pre todo-ai

# Stable with pip
pip install todo-ai
```
</details>

> **Recommendation:** Use `uv tool` for faster, more reliable installation.

---

## 4. Technical Implementation (Simplified)

### 4.1 Release Script Enhancements

**Command Structure:**

```bash
# Prepare beta release
./release/release.sh --prepare --beta

# Prepare stable release (default)
./release/release.sh --prepare

# Execute either type (reads from .prepare_state)
./release/release.sh --execute
```

**Key Functions to Implement:**

**1. Auto-Detect Major Releases & Enforce Beta:**
- Compare major version of proposed release vs last stable
- If major bump AND preparing stable: Check if beta exists
- If no beta: Block with error and show how to create beta
- If beta exists: Allow proceed

**2. Beta Version Auto-Increment:**
- Query GitHub releases for existing betas (e.g., v1.0.0b*)
- If none: Use b1
- If exist: Find highest number, increment by 1
- Returns version like 1.0.0b3

**3. Beta Maturity Warnings:**
- Only for stable releases after beta
- Calculate days since beta published
- Warn if < 7 days (major) or < 2 days (minor)
- Always allow proceed (warning only, never blocks)

**4. Pre-Flight Validation:**
- Check 6+ conditions before execute:
  - Prepare state exists
  - CI/CD passing
  - No uncommitted changes
  - GitHub authenticated
  - Build dependencies available
  - Beta maturity (warning only)

**5. Enhanced State File:**
- Save comprehensive metadata in `.prepare_state`:
  - version, git_tag, release_type
  - base_version, is_major, prepared_at, prepared_by
- Execute phase reads all context from state file

### 4.2 GitHub Actions Updates (Simplified)

**`.github/workflows/release.yml` - Simplified workflow:**

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      # Simplified detection: if tag ends with 'b' + digits, it's a beta
      - name: Detect pre-release type
        id: prerelease
        run: |
          TAG="${{ github.ref_name }}"
          if [[ "$TAG" =~ b[0-9]+$ ]]; then
            echo "type=beta" >> $GITHUB_OUTPUT
            echo "is_prerelease=true" >> $GITHUB_OUTPUT
          else
            echo "type=stable" >> $GITHUB_OUTPUT
            echo "is_prerelease=false" >> $GITHUB_OUTPUT
          fi

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Build package
        run: uv run python -m build

      - name: Check package
        run: uv run twine check dist/*

      # Single PyPI publish step for both beta and stable
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: uv run twine upload dist/*

      # GitHub release with pre-release flag auto-set
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          prerelease: ${{ steps.prerelease.outputs.is_prerelease }}
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # Optional: Notify for stable releases
      - name: Notify community
        if: steps.prerelease.outputs.type == 'stable'
        run: |
          echo "Stable release published: ${{ github.ref_name }}"
```

**Key Simplifications:**
- ✂️ Removed alpha/RC detection logic
- ✂️ Removed TestPyPI publish step
- ✂️ Single PyPI target for all releases
- ✂️ Simple regex: `b[0-9]+$` = beta
- ✂️ Reduced from ~25 steps to ~15 steps

### 4.3 Version Management (Simplified)

**Single Format - PEP 440 Everywhere:**

**Files to Update:**
- `pyproject.toml` - `version = "1.0.0b1"`
- `todo.ai` - `VERSION="1.0.0b1"`
- `todo_ai/__init__.py` - `__version__ = "1.0.0b1"`
- Git tag - `v1.0.0b1` (same with 'v' prefix)

**Conversion:**
```bash
# Simple: just remove 'v' prefix for PyPI
git_tag="v1.0.0b1"
pypi_version="${git_tag#v}"  # → "1.0.0b1"
```

**Version Validation:**
- Use Python's `packaging.version.Version()` to validate format
- Ensures all versions are valid PEP 440
- No regex parsing - use standard library

**Key Simplification:**
- No format conversion between SemVer and PEP 440
- Single source of truth across all files
- Git tag = PyPI version (minus 'v' prefix)

### 4.4 Documentation Updates

**README.md additions:**

```markdown
## Installation

### Stable Release (Recommended)
```bash
# Using uv (recommended)
uv tool install todo-ai

# Alternative: pipx
pipx install todo-ai

# Alternative: pip
pip install todo-ai
```

### Beta Testing
Help test upcoming features:
```bash
# Using uv (recommended)
uv tool install --prerelease=allow todo-ai

# Alternative: pipx
pipx install --pre todo-ai

# Alternative: pip
pip install --pre todo-ai
```

### Development Version
```bash
# Using uv (recommended)
uv tool install git+https://github.com/fxstein/todo.ai.git@main

# Alternative: pipx
pipx install git+https://github.com/fxstein/todo.ai.git@main
```

## Release Channels

- **Stable:** Fully tested, production-ready
- **Beta:** Feature-complete, testing phase
- **Alpha:** Bleeding edge, may have bugs

See [CHANGELOG.md](CHANGELOG.md) for version history.
```

---

## 5. Testing Strategy (Simplified)

### 5.1 Beta Testing

**Scope:**
- Real-world usage by early adopters
- Cross-platform testing (macOS, Linux, Windows)
- MCP server compatibility testing
- Migration testing from shell version

**Testing Matrix:**

| Platform | Shell | Python | MCP |
|----------|-------|--------|-----|
| macOS 13+ | ✓ | ✓ | ✓ |
| Ubuntu 20.04+ | ✓ | ✓ | ✓ |
| Windows WSL2 | ✓ | ✓ | ✓ |

**MCP Server Testing:**
- **Automated Testing:** Implement headless MCP client test suite
  - Test JSON-RPC protocol compliance
  - Verify tool schemas and responses
  - Test against MCP protocol specification
  - Independent of specific client implementation (Cursor/Claude Desktop)
- **Manual Testing:** Real-world usage with Cursor and Claude Desktop
  - Verify UI integration
  - Test user workflows
  - Collect feedback on usability

**Exit Criteria for Stable Release:**
- No critical bugs reported during beta period
- Positive or neutral feedback from beta testers
- Migration tested with real data (if applicable)
- Documentation reviewed
- MCP automated tests passing
- Recommended duration met (7+ days for major, 2-3 days for minor)

**Note:** RC phase eliminated - iterate betas (b1, b2, b3...) instead of separate RC tier.

---

## 6. Communication Strategy

### 6.1 Release Announcements

**Channels:**
- GitHub Releases (primary)
- GitHub Discussions
- Project README.md
- PyPI project description

**Template for Beta Announcement:**

```markdown
# todo.ai v1.0.0-beta.1

🎉 **We're excited to announce the first beta release of todo.ai Python version!**

## 🚀 What's New
- Full Python implementation with MCP server support
- 100% command parity with shell version
- Installable via uv: `uv tool install --prerelease=allow todo-ai`

## ⚠️ Beta Status
This is a **pre-release** version. While extensively tested, we recommend:
- Backing up your TODO.md before use
- Testing in non-critical projects first
- Reporting issues on GitHub

## 🧪 Help Us Test
We need your help to make 1.0.0 stable amazing:
1. Install: `uv tool install --prerelease=allow todo-ai` (or use pipx/pip)
2. Try it: Use it for real work
3. Report: Share feedback on GitHub Discussions

## 📊 What's Been Tested
- ✅ 150 automated tests passing
- ✅ All 32 commands implemented
- ✅ MCP server functional
- ✅ Migration from shell version

## 🐛 Known Issues
- [List any known issues]

## 📝 Full Changelog
[Link to detailed changelog]

---

**Install:** `uv tool install --prerelease=allow todo-ai`
**Report Issues:** https://github.com/fxstein/todo.ai/issues
**Discuss:** https://github.com/fxstein/todo.ai/discussions
```

### 6.2 Version Documentation

**CHANGELOG.md format:**

```markdown
# Changelog

## [Unreleased]

## [1.0.0] - 2025-01-15
### Added
- Python implementation with full command parity
- MCP server for AI agent integration
- ...

## [1.0.0-rc.1] - 2025-01-08
### Fixed
- Critical bug in task restoration
- ...

## [1.0.0-beta.2] - 2025-01-01
### Added
- Migration command for shell users
### Fixed
- Tag preservation in modify command
- ...

## [1.0.0-beta.1] - 2024-12-20
### Added
- Initial Python version
- All core commands
- ...
```

---

## 7. Rollback and Recovery

### 7.1 Version Pinning

**Allow users to pin versions:**

```bash
# Install specific version (recommended: uv)
uv tool install todo-ai==1.0.0

# Upgrade to latest stable
uv tool upgrade todo-ai

# Downgrade if issues
uv tool uninstall todo-ai
uv tool install todo-ai==0.9.5

# Alternative: pipx
pipx install todo-ai==1.0.0
pipx upgrade todo-ai
pipx install --force todo-ai==0.9.5
```

### 7.2 Emergency Rollback

**If critical bug found in release:**

1. **Yank from PyPI:**
   ```bash
   # Mark version as yanked (won't be installed by default)
   twine yank todo-ai 1.0.0 "Critical bug: task data corruption"
   ```

2. **Publish hotfix:**
   ```bash
   # Immediate patch release
   ./release/release.sh --prepare  # Creates 1.0.1
   ./release/release.sh --execute
   ```

3. **Notify users:**
   - GitHub Release with warning
   - PyPI description update
   - Email to watchers (if available)

### 7.3 Data Safety

**Always test migrations:**
- Backup TODO.md before any write operation
- Validate file format after changes
- Provide rollback command for migrations

---

## 8. Metrics and Success Criteria

### 8.1 Beta Success Metrics

**Quantitative:**
- 10+ beta testers actively using
- 100+ GitHub downloads of beta
- <5 critical bugs reported
- >80% positive feedback

**Qualitative:**
- Users successfully migrate from shell version
- MCP server works with Cursor/Claude Desktop
- Cross-platform compatibility confirmed

### 8.2 Monitoring

**Track:**
- PyPI download statistics
- GitHub issue rate
- Test coverage percentage
- User feedback sentiment

**Tools:**
- PyPI stats: https://pypistats.org/
- GitHub Insights: Issues, PRs, Traffic
- Test coverage: pytest-cov reports

---

## 9. Implementation Phases (Simplified)

### Phase 1: Core Beta Infrastructure

**Goal:** Enable basic beta releases with major release protection

- [ ] Add `--beta` flag parsing to release.sh
- [ ] Implement beta version auto-detection (query GitHub for existing betas)
- [ ] Implement major release enforcement (block if no beta exists)
- [ ] Update `.prepare_state` to include `release_type`
- [ ] Update GitHub Actions for simple pre-release detection (regex: `b[0-9]+$`)
- [ ] Update documentation with beta installation instructions

### Phase 2: Hardening & Validation

**Goal:** Add comprehensive safety checks

- [ ] Implement beta maturity warnings (never blocks, just warns)
- [ ] Add 6+ pre-flight validation checks
- [ ] Enhance error messages with remediation steps
- [ ] Test all error paths and validation gates

### Phase 3: Documentation & Cursor Rules

**Goal:** Complete user-facing documentation

- [ ] Update README.md with simplified installation
- [ ] Add Cursor AI rules for release decision making
- [ ] Update release process documentation
- [ ] Create beta testing guide for users

### Phase 4: First Beta Release

**Goal:** Validate the process works

- [ ] Create v1.0.0b1 release
- [ ] Announce to GitHub watchers
- [ ] Collect feedback from early adopters
- [ ] Iterate with b2, b3 as needed

### Phase 5: Stable Release

**Goal:** Production release

- [ ] Verify beta testing period met (7+ days for major)
- [ ] Create v1.0.0 stable release
- [ ] Major announcement
- [ ] Update all documentation
- [ ] Celebrate! 🎉

---

## 10. Recommendations

### Current State Assessment

Given that todo.ai has:
- ✅ 100% feature parity achieved
- ✅ 150+ automated tests passing
- ✅ Comprehensive test coverage
- ✅ MCP server implemented
- ✅ Existing two-phase release process

**Recommendation:** Implement beta support incrementally in phases above.

### Release Strategy Going Forward

**For Major Releases (e.g., 3.0.0):**
1. Always create beta first (v3.0.0b1) - script enforces this
2. Beta testing period: 7+ days recommended
3. Iterate betas if issues found (b2, b3...)
4. Release stable when ready (v3.0.0)

**For Minor/Patch Releases:**
- Minor: Beta optional (user choice based on risk)
- Patch: No beta needed (direct to stable)

**Version Cadence:**
- Beta releases: As needed for major releases and significant features
- Stable releases: When betas are validated
- Patch releases: As needed for critical bugs

---

## 11. References

**Standards:**
- [Semantic Versioning 2.0.0](https://semver.org/)
- [PEP 440 - Version Identification](https://www.python.org/dev/peps/pep-0440/)
- [Python Packaging User Guide](https://packaging.python.org/)

**Best Practices:**
- [Google Chrome Release Channels](https://www.chromium.org/getting-involved/dev-channel/)
- [Kubernetes Release Process](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-release/release.md)
- [Node.js Release Working Group](https://github.com/nodejs/Release)

**Tools:**
- [twine - PyPI Upload Tool](https://twine.readthedocs.io/)
- [GitHub Actions Release](https://github.com/softprops/action-gh-release)
- [Test PyPI](https://test.pypi.org/)

---

## Appendix A: Command Reference

**Create Beta Release:**
```bash
# Prepare beta release
./release/release.sh --prepare --beta
# Review release/RELEASE_NOTES.md
./release/release.sh --execute
```

**Install Beta:**
```bash
# Install latest beta (recommended: uv)
uv tool install --prerelease=allow todo-ai

# Install specific beta
uv tool install todo-ai==1.0.0b1

# Upgrade to latest stable
uv tool upgrade todo-ai

# Alternative: pipx
pipx install --pre todo-ai
pipx install todo-ai==1.0.0b1
pipx upgrade todo-ai
```

**Check Version:**
```bash
# Show installed version
todo-ai version

# List available versions (uv)
uv tool list | grep todo-ai

# List available versions (pipx)
pipx list | grep todo-ai
```

---

## Appendix B: GitHub Secrets Required

For beta and stable releases, add this secret:

```
PYPI_API_TOKEN           # Production PyPI token (for both beta and stable)
GITHUB_TOKEN            # Automatically provided by Actions (no setup needed)
```

**Setup:**
1. Generate API token on PyPI (https://pypi.org/manage/account/token/)
2. Add to GitHub: Settings → Secrets → Actions → New repository secret
3. Name it `PYPI_API_TOKEN` and paste the token value

**Simplified:** Only one PyPI token needed (no TestPyPI token required)

---

## Appendix C: Version History & Simplifications

### Version 2.0 Simplifications (December 16, 2025)

After detailed analysis (see `BETA_PRERELEASE_RECOMMENDATIONS.md`), the strategy was simplified:

| Original (v1.1) | Simplified (v2.0) | Rationale |
|----------------|-------------------|-----------|
| 4 tiers (Alpha/Beta/RC/Stable) | 2 tiers (Beta/Stable) | Alpha → feature branches, RC → iterate betas |
| TestPyPI + PyPI | PyPI only | Dependency resolution issues, added complexity |
| PEP 440 + SemVer formats | PEP 440 only | No conversion needed, single source of truth |
| Feature flags proposed | Eliminated (YAGNI) | Beta releases serve same purpose |
| Manual policies | Auto-enforced | Major releases must have beta (script-enforced) |

**Result:** 40-50% complexity reduction, 60-70% error risk reduction, zero breaking changes.

### Version 1.1 Review Findings (December 15, 2025)

| Issue | Risk Level | Resolution |
|-------|-----------|------------|
| TestPyPI dependency resolution | **Critical** | **Eliminated TestPyPI entirely in v2.0** |
| Manual version parsing fragility | **High** | Use Python `packaging` library |
| Human gate for all releases | **Medium** | Two-phase process maintained in v2.0 |
| MCP testing strategy | **Medium** | Implement headless JSON-RPC test suite |
| Feature flags | **Low** | **Eliminated in v2.0 (YAGNI principle)** |

---

**Document Status:** APPROVED (v2.0 - Simplified)
**Next Steps:** Implement phases 1-3 (see Section 9)
**Owner:** Release Engineering Team
**Related:** `BETA_PRERELEASE_RECOMMENDATIONS.md` - Detailed analysis
**Last Updated:** December 16, 2025
