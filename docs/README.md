# Documentation Index

Welcome to the todo.ai documentation! This page provides a complete overview of all available documentation organized by category.

## Quick Links

**New to todo.ai?** Start here:
- [Getting Started](guides/GETTING_STARTED.md) - Quick start guide with setup instructions
- [Installation](guides/INSTALLATION.md) - Installation instructions and troubleshooting

**Need help with a specific feature?**
- [Numbering Modes](guides/NUMBERING_MODES_GUIDE.md) - Complete guide to all numbering modes
- [Usage Patterns](guides/USAGE_PATTERNS.md) - Real-world usage scenarios
- [Coordination Setup](guides/COORDINATION_SETUP.md) - Setup guides for coordination services

**Contributing to todo.ai?**
- [Development Guidelines](development/DEVELOPMENT_GUIDELINES.md) - Development workflow and best practices
- [Documentation Structure](STRUCTURE.md) - How documentation is organized

## Documentation Structure

### 📚 guides/ - User Guides

User-facing documentation for getting started and using todo.ai features.

| Document | Description |
|----------|-------------|
| [Getting Started](guides/GETTING_STARTED.md) | Quick start guide with setup instructions |
| [Installation](guides/INSTALLATION.md) | Installation methods and troubleshooting |
| [Usage Patterns](guides/USAGE_PATTERNS.md) | Real-world usage scenarios and workflows |
| [Numbering Modes](guides/NUMBERING_MODES_GUIDE.md) | Complete guide to task numbering modes |
| [Coordination Setup](guides/COORDINATION_SETUP.md) | Setup guides for coordination services |

### 🏗️ design/ - Technical Design

Technical design specifications explaining system architecture and feature design.

| Document | Description |
|----------|-------------|
| [Bug Reporting Design](design/BUG_REPORTING_DESIGN.md) | Bug reporting feature design and workflow |
| [Git Hooks Design](design/GIT_HOOKS_DESIGN.md) | Git hooks integration design |
| [Hybrid Task Numbering](design/HYBRID_TASK_NUMBERING_DESIGN.md) | Task numbering system design |
| [Migration System](design/MIGRATION_SYSTEM_DESIGN.md) | Migration system architecture |
| [Multi-User Design](design/MULTI_USER_DESIGN.md) | Multi-user collaboration design |
| [Smart Installer](design/SMART_INSTALLER_DESIGN.md) | Smart installer design and decision logic |
| [Tagging System](design/TODO_TAGGING_SYSTEM_DESIGN.md) | Task tagging system design |
| [Uninstall Feature](design/UNINSTALL_DESIGN.md) | Uninstall feature design |

### 👨‍💻 development/ - Contributor Documentation

Documentation for contributors and developers working on todo.ai.

| Document | Description |
|----------|-------------|
| [Development Guidelines](development/DEVELOPMENT_GUIDELINES.md) | Development workflow and best practices |
| [Migration Guide](development/MIGRATION_GUIDE.md) | Guide for writing migration functions |
| [Test Plan](development/NUMBERING_MODES_TEST_PLAN.md) | Test plan for numbering modes |
| [Tool Improvements](development/TODO_TOOL_IMPROVEMENTS.md) | Planned improvements and roadmap |

### 🔬 analysis/ - Research and Analysis

Research documents, analysis reports, and comparison studies.

| Document | Description |
|----------|-------------|
| [CI/CD Process Parity](analysis/CI_CD_PROCESS_PARITY_ASSESSMENT.md) | Assessment and implementation of modern CI/CD infrastructure (uv, pre-commit, GitHub Actions) |
| [Bash vs Zsh Analysis](analysis/BASH_VS_ZSH_ANALYSIS.md) | Bash vs zsh comparison and recommendations |
| [Code Size Analysis](analysis/CODE_SIZE_ANALYSIS.md) | Codebase size analysis and optimization |
| [GitHub API Coordination](analysis/GITHUB_API_COORDINATION_ANALYSIS.md) | GitHub API coordination analysis |
| [Implementation Alternatives](analysis/IMPLEMENTATION_ALTERNATIVES_ANALYSIS.md) | Alternative implementation approaches |
| [Multi-User Conflicts](analysis/MULTI_USER_CONFLICT_ANALYSIS.md) | Multi-user conflict scenarios |
| [Multi-User Tool Research](analysis/MULTI_USER_TOOL_RESEARCH.md) | Research on multi-user coordination tools |
| [Task Numbering Schema](analysis/TASK_NUMBERING_SCHEMA_ANALYSIS.md) | Task numbering schema analysis |

### 📦 archive/ - Historical Documentation

Completed migrations, historical context, and deprecated documentation.

| Document | Description |
|----------|-------------|
| [Commit Format Migration](archive/COMMIT_FORMAT_MIGRATION.md) | Commit format migration (completed) |
| [Cursor Rules Migration](archive/CURSOR_RULES_MIGRATION.md) | Cursor rules migration (completed) |
| [Release Numbering Mapping](archive/RELEASE_NUMBERING_MAPPING.md) | Release numbering analysis (historical) |
| [Smart Installer Preview](archive/README_PREVIEW_WITH_SMART_INSTALLER.md) | Smart installer README preview (superseded) |

## Contributing Documentation

When adding new documentation:

1. **Choose the right category:**
   - User guides → `guides/`
   - Technical designs → `design/`
   - Development docs → `development/`
   - Research/analysis → `analysis/`
   - Historical docs → `archive/`

2. **Use descriptive filenames:**
   - Use UPPERCASE with underscores
   - Include document type suffix: `_GUIDE.md`, `_DESIGN.md`, `_ANALYSIS.md`

3. **Update this index:**
   - Add your new document to the appropriate table above
   - Maintain alphabetical order within sections

4. **Cross-reference appropriately:**
   - Link to related docs using relative paths
   - Example: `../design/FEATURE_DESIGN.md`

See [STRUCTURE.md](STRUCTURE.md) for complete documentation structure guidelines.

## Need Help?

- **Issues or bugs:** [Report on GitHub](https://github.com/fxstein/todo.ai/issues)
- **Questions:** Check [Usage Patterns](guides/USAGE_PATTERNS.md) for common scenarios
- **Contributing:** See [Development Guidelines](development/DEVELOPMENT_GUIDELINES.md)

---

**Last Updated:** 2025-11-11
**Repository:** https://github.com/fxstein/todo.ai
