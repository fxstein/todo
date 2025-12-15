# Beta and Pre-Release Strategy for todo.ai

**Document Version:** 1.0
**Date:** December 15, 2025
**Status:** PROPOSED

---

## Executive Summary

This document outlines the strategy for implementing beta and pre-release capabilities in todo.ai's release process. Given that todo.ai is transitioning from a shell script to a Python-based tool with MCP server capabilities and cloud/AI integration, a robust pre-release strategy is essential for managing risk, gathering feedback, and ensuring quality.

**Recommendation:** Implement a multi-tier release strategy with alpha, beta, and release candidate phases before stable releases.

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

**For todo.ai (analogous):**
1. Publish alpha to test PyPI channel
2. Publish beta to production PyPI (pre-release flag)
3. Publish RC to production PyPI (pre-release flag)
4. Publish stable to production PyPI

**Feature Flags:**
- Enable experimental features for alpha/beta users
- Disable in stable unless explicitly enabled
- Example: `TODOAI_EXPERIMENTAL_MCP_V2=1`

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

## 3. Implementation Strategy for todo.ai

### 3.1 Release Lifecycle

**Phase 1: Alpha (Internal Testing)**

**Trigger:** Major refactor complete, core features working
**Audience:** Maintainers, contributors
**Testing:** Automated tests + manual workflows
**Changes Allowed:** Breaking changes, API redesign

**Criteria for Beta:**
- All automated tests passing
- Core commands working
- No known critical bugs
- Basic documentation complete

**Phase 2: Beta (External Testing)**

**Trigger:** Alpha stable, ready for early adopters
**Audience:** GitHub watchers, early adopters, power users
**Testing:** Real-world usage, edge cases, compatibility
**Changes Allowed:** Bug fixes, minor features, documentation
**Recommended Duration:** 2-4 weeks

**Criteria for RC:**
- No critical bugs reported recently
- Positive feedback from beta users
- All planned features implemented
- Migration path tested

**Phase 3: Release Candidate (Final Validation)**

**Trigger:** Beta stable, production-ready
**Audience:** Brave stable users, final testers
**Testing:** Production-like scenarios, stress testing
**Changes Allowed:** Critical bug fixes only, documentation
**Recommended Duration:** 1 week

**Criteria for Stable:**
- No bugs reported in RC period
- Performance benchmarks met
- Documentation complete and reviewed
- Migration guide validated

**Phase 4: Stable (General Availability)**

**Trigger:** RC passes all validation
**Audience:** All users
**Testing:** Production monitoring, user feedback
**Changes:** Patch releases for bugs, minor releases for features

### 3.2 Version Numbering Strategy

**For Python Package (PyPI):**

```python
# pyproject.toml
version = "1.0.0a1"  # Alpha 1
version = "1.0.0b1"  # Beta 1
version = "1.0.0rc1" # Release Candidate 1
version = "1.0.0"    # Stable
```

**For Git Tags:**

```bash
# SemVer format for consistency with GitHub releases
v1.0.0-alpha.1
v1.0.0-beta.1
v1.0.0-rc.1
v1.0.0
```

**Conversion Table:**

| PyPI (PEP 440) | Git Tag (SemVer) | Description |
|----------------|------------------|-------------|
| `1.0.0a1` | `v1.0.0-alpha.1` | First alpha |
| `1.0.0a2` | `v1.0.0-alpha.2` | Second alpha |
| `1.0.0b1` | `v1.0.0-beta.1` | First beta |
| `1.0.0rc1` | `v1.0.0-rc.1` | First RC |
| `1.0.0` | `v1.0.0` | Stable |

### 3.3 Installation Methods by Channel

**Alpha Channel:**
```bash
# From test PyPI (recommended)
uv tool install --index-url https://test.pypi.org/simple/ --prerelease=allow todo-ai

# From Git tag
uv tool install git+https://github.com/fxstein/todo.ai.git@v1.0.0-alpha.1

# Alternative: pipx
pipx install git+https://github.com/fxstein/todo.ai.git@v1.0.0-alpha.1

# Alternative: pip
pip install --pre --index-url https://test.pypi.org/simple/ todo-ai
```

**Beta Channel:**
```bash
# Pre-release from PyPI (recommended)
uv tool install --prerelease=allow todo-ai

# Specific beta version
uv tool install todo-ai==1.0.0b1

# Alternative: pipx
pipx install --pre todo-ai

# Alternative: pip
pip install --pre todo-ai
```

**Stable Channel:**
```bash
# Latest stable (recommended)
uv tool install todo-ai

# Specific stable version
uv tool install todo-ai==1.0.0

# Alternative: pipx
pipx install todo-ai

# Alternative: pip
pip install todo-ai
```

---

## 4. Technical Implementation

### 4.1 Release Script Enhancements

**New Flags:**

```bash
# Prepare alpha release
./release/release.sh --prepare --alpha

# Prepare beta release
./release/release.sh --prepare --beta

# Prepare release candidate
./release/release.sh --prepare --rc

# Prepare stable release (default)
./release/release.sh --prepare
```

**Implementation Changes:**

```bash
# release/release.sh additions

# Parse pre-release flag
PRERELEASE_TYPE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --alpha)
            PRERELEASE_TYPE="alpha"
            shift
            ;;
        --beta)
            PRERELEASE_TYPE="beta"
            shift
            ;;
        --rc)
            PRERELEASE_TYPE="rc"
            shift
            ;;
        # ... other flags
    esac
done

# Generate pre-release version
generate_prerelease_version() {
    local base_version="$1"
    local type="$2"

    if [[ -z "$type" ]]; then
        # Stable release
        echo "$base_version"
        return
    fi

    # Get existing pre-releases of this type
    local existing=$(gh release list --json tagName --jq '.[]|select(.tagName|startswith("v'$base_version'-'$type'"))|.tagName')

    # Find highest pre-release number
    local highest=0
    while IFS= read -r tag; do
        local num=$(echo "$tag" | sed -n 's/.*'$type'\.\([0-9]*\)/\1/p')
        if [[ $num -gt $highest ]]; then
            highest=$num
        fi
    done <<< "$existing"

    # Increment
    local next=$((highest + 1))

    # Format for git tag (SemVer)
    local git_tag="v${base_version}-${type}.${next}"

    # Format for PyPI (PEP 440)
    local pypi_version="${base_version}${type:0:1}${next}"

    echo "$git_tag|$pypi_version"
}
```

### 4.2 GitHub Actions Updates

**`.github/workflows/release.yml` changes:**

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

      - name: Detect pre-release type
        id: prerelease
        run: |
          TAG="${{ github.ref_name }}"
          if [[ "$TAG" =~ -alpha\. ]]; then
            echo "type=alpha" >> $GITHUB_OUTPUT
            echo "is_prerelease=true" >> $GITHUB_OUTPUT
            echo "pypi_target=testpypi" >> $GITHUB_OUTPUT
          elif [[ "$TAG" =~ -beta\. ]]; then
            echo "type=beta" >> $GITHUB_OUTPUT
            echo "is_prerelease=true" >> $GITHUB_OUTPUT
            echo "pypi_target=pypi" >> $GITHUB_OUTPUT
          elif [[ "$TAG" =~ -rc\. ]]; then
            echo "type=rc" >> $GITHUB_OUTPUT
            echo "is_prerelease=true" >> $GITHUB_OUTPUT
            echo "pypi_target=pypi" >> $GITHUB_OUTPUT
          else
            echo "type=stable" >> $GITHUB_OUTPUT
            echo "is_prerelease=false" >> $GITHUB_OUTPUT
            echo "pypi_target=pypi" >> $GITHUB_OUTPUT
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

      # Publish to Test PyPI for alpha releases
      - name: Publish to Test PyPI (alpha only)
        if: steps.prerelease.outputs.type == 'alpha'
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.TEST_PYPI_API_TOKEN }}
        run: |
          uv run twine upload --repository testpypi dist/*

      # Publish to production PyPI for beta, rc, and stable
      - name: Publish to PyPI
        if: steps.prerelease.outputs.type != 'alpha'
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: uv run twine upload dist/*

      - name: Attach files to GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
          prerelease: ${{ steps.prerelease.outputs.is_prerelease }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      # Notify Discord/Slack for major releases
      - name: Notify community
        if: steps.prerelease.outputs.type == 'stable'
        run: |
          # Add notification logic here
          echo "Stable release published: ${{ github.ref_name }}"
```

### 4.3 Version Management

**Update `pyproject.toml` dynamically:**

```bash
# release/release.sh function
update_version_files() {
    local git_tag="$1"
    local pypi_version="$2"

    # Update pyproject.toml (PEP 440 format)
    sed -i.bak 's/^version = .*/version = "'$pypi_version'"/' pyproject.toml

    # Update todo.ai shell script (SemVer format)
    sed -i.bak 's/^VERSION=.*/VERSION="'${git_tag#v}'"/' todo.ai

    # Update todo_ai/__init__.py (PEP 440 format)
    sed -i.bak 's/^__version__ = .*/__version__ = "'$pypi_version'"/' todo_ai/__init__.py

    rm -f pyproject.toml.bak todo.ai.bak todo_ai/__init__.py.bak
}
```

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

## 5. Testing Strategy by Release Type

### 5.1 Alpha Testing

**Scope:**
- All automated tests must pass
- Manual testing of new features
- Integration tests with test datasets

**Exit Criteria:**
- Zero failing automated tests
- Core commands working
- No known critical bugs

### 5.2 Beta Testing

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

**Exit Criteria:**
- No critical bugs reported for 1 week
- Positive feedback from 5+ beta testers
- Migration tested with real data
- Documentation reviewed

### 5.3 Release Candidate Testing

**Scope:**
- Production-like scenarios
- Performance benchmarks
- Load testing (large TODO.md files)
- Security audit

**Benchmarks:**
- File operations < 100ms for 1000 tasks
- MCP server response < 50ms
- Memory usage < 50MB idle

**Exit Criteria:**
- Zero bugs reported during RC period
- All benchmarks met or exceeded
- Security review completed

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

## 9. Implementation Phases

### Phase 1: Infrastructure

- [ ] Update release.sh with pre-release flags
- [ ] Update GitHub Actions for pre-release detection
- [ ] Add Test PyPI credentials to GitHub secrets
- [ ] Update documentation with beta installation instructions

### Phase 2: Alpha Release (Optional)

- [ ] Create v1.0.0-alpha.1 release
- [ ] Publish to Test PyPI
- [ ] Internal testing by maintainers
- [ ] Fix critical issues

### Phase 3: Beta Release

- [ ] Create v1.0.0-beta.1 release
- [ ] Announce to GitHub watchers
- [ ] Collect feedback from early adopters
- [ ] Iterate with beta.2, beta.3 as needed

### Phase 4: Release Candidate

- [ ] Create v1.0.0-rc.1 release
- [ ] Final testing period
- [ ] Documentation review
- [ ] Freeze feature additions

### Phase 5: Stable Release

- [ ] Create v1.0.0 stable release
- [ ] Major announcement
- [ ] Update all documentation
- [ ] Celebrate! 🎉

---

## 10. Recommendations

### Immediate Actions (For Current todo.ai State)

Given that todo.ai has:
- ✅ 100% feature parity achieved
- ✅ 150 automated tests passing
- ✅ Comprehensive test coverage
- ✅ MCP server implemented

**Recommendation:** **Start with Beta Phase**

Skip alpha (since internal testing is complete) and go directly to:

1. Implement beta release infrastructure
2. Release v1.0.0-beta.1
3. Beta testing period (2-4 weeks recommended)
4. Release v1.0.0-rc.1
5. RC validation period (1 week recommended)
6. Release v1.0.0 stable

### Long-term Strategy

**After 1.0.0 stable:**
- Maintain beta channel for new features
- Use RC for major version transitions (2.0.0)
- Consider nightly/dev builds for active contributors

**Version Cadence (Suggested):**
- **Stable releases:** Regular cadence for features
- **Beta releases:** Before each stable for validation
- **Patch releases:** As needed for critical bugs

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

For full pre-release support, add these secrets:

```
PYPI_API_TOKEN           # Production PyPI token
TEST_PYPI_API_TOKEN      # Test PyPI token (for alpha)
GITHUB_TOKEN            # Automatically provided by Actions
```

**Setup:**
1. Generate tokens on PyPI and Test PyPI
2. Add to GitHub: Settings → Secrets → Actions
3. Update GitHub Actions to use appropriate token per release type

---

**Document Status:** PROPOSED
**Next Steps:** Review with maintainers, approve strategy, implement infrastructure
**Owner:** Release Engineering Team
**Reviewers:** Project Maintainers, Community
