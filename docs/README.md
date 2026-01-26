# Documentation Index

Welcome to the todo.ai documentation! This page provides a complete overview of all available documentation organized by category.

## Quick Links

**New to todo.ai?** Start here:

- [Getting Started](guides/GETTING_STARTED.md) - Quick start with MCP and CLI setup
- [FAQ](FAQ.md) - Common questions answered
- [MCP Setup Guide](user/MCP_SETUP.md) - Cursor AI integration

**Upgrading from v2.x?**

- [Migration Guide](user/PYTHON_MIGRATION_GUIDE.md) - Shell script to Python upgrade

**Need help with a specific feature?**

- [Numbering Modes](guides/NUMBERING_MODES_GUIDE.md) - Complete guide to all numbering modes
- [Usage Patterns](guides/USAGE_PATTERNS.md) - Real-world usage scenarios

## Documentation Structure

### 📘 user/ - User Guides

Essential guides for setting up and using todo.ai.

| Document | Description |
|----------|-------------|
| [MCP Setup Guide](user/MCP_SETUP.md) | Cursor AI integration with MCP |
| [Migration Guide](user/PYTHON_MIGRATION_GUIDE.md) | Upgrading from shell script to Python |

### 📚 guides/ - Feature Guides

Detailed guides for specific features and workflows.

| Document | Description |
|----------|-------------|
| [Getting Started](guides/GETTING_STARTED.md) | Quick start guide with setup instructions |
| [Installation](guides/INSTALLATION.md) | Installation methods and troubleshooting |
| [Usage Patterns](guides/USAGE_PATTERNS.md) | Real-world usage scenarios and workflows |
| [Numbering Modes](guides/NUMBERING_MODES_GUIDE.md) | Complete guide to task numbering modes |
| [Coordination Setup](guides/COORDINATION_SETUP.md) | Setup guides for coordination services |
| [Tamper Detection](guides/TAMPER_DETECTION.md) | File integrity protection |
| [Beta Testing](guides/BETA_TESTING_GUIDE.md) | Testing pre-release versions |

### ❓ FAQ

| Document | Description |
|----------|-------------|
| [FAQ](FAQ.md) | Frequently asked questions |

### 🏗️ design/ - Technical Design

Technical design specifications explaining system architecture and feature design.

| Document | Description |
|----------|-------------|
| [README Redesign](design/README_REDESIGN_V3.md) | v3.0 README structure design |
| [Bug Reporting Design](design/BUG_REPORTING_DESIGN.md) | Bug reporting feature design |
| [Git Hooks Design](design/GIT_HOOKS_DESIGN.md) | Git hooks integration design |
| [Hybrid Task Numbering](design/HYBRID_TASK_NUMBERING_DESIGN.md) | Task numbering system design |
| [Migration System](design/MIGRATION_SYSTEM_DESIGN.md) | Migration system architecture |
| [Multi-User Design](design/MULTI_USER_DESIGN.md) | Multi-user collaboration design |
| [Smart Installer](design/SMART_INSTALLER_DESIGN.md) | Smart installer design |
| [Tagging System](design/TODO_TAGGING_SYSTEM_DESIGN.md) | Task tagging system design |
| [Uninstall Feature](design/UNINSTALL_DESIGN.md) | Uninstall feature design |

### 👨‍💻 development/ - Contributor Documentation

Documentation for contributors and developers working on todo.ai.

| Document | Description |
|----------|-------------|
| [Development Guidelines](development/DEVELOPMENT_GUIDELINES.md) | Development workflow and best practices |
| [Setup](development/SETUP.md) | Development environment setup |
| [Migration Guide](development/MIGRATION_GUIDE.md) | Guide for writing migration functions |
| [Test Plan](development/NUMBERING_MODES_TEST_PLAN.md) | Test plan for numbering modes |
| [Tool Improvements](development/TODO_TOOL_IMPROVEMENTS.md) | Planned improvements and roadmap |

### 🔬 analysis/ - Research and Analysis

Research documents, analysis reports, and comparison studies.

| Document | Description |
|----------|-------------|
| [CI/CD Process Parity](analysis/CI_CD_PROCESS_PARITY_ASSESSMENT.md) | CI/CD infrastructure assessment |
| [Bash vs Zsh Analysis](analysis/BASH_VS_ZSH_ANALYSIS.md) | Shell comparison |
| [Code Size Analysis](analysis/CODE_SIZE_ANALYSIS.md) | Codebase optimization |
| [GitHub API Coordination](analysis/GITHUB_API_COORDINATION_ANALYSIS.md) | API coordination analysis |

### 📦 archive/ - Historical Documentation

Completed migrations and deprecated documentation.

| Document | Description |
|----------|-------------|
| [Commit Format Migration](archive/COMMIT_FORMAT_MIGRATION.md) | Commit format migration (completed) |
| [Cursor Rules Migration](archive/CURSOR_RULES_MIGRATION.md) | Cursor rules migration (completed) |

## Contributing Documentation

When adding new documentation:

1. **Choose the right category:**
   - User essentials → `user/`
   - Feature guides → `guides/`
   - Technical designs → `design/`
   - Development docs → `development/`
   - Research/analysis → `analysis/`
   - Historical docs → `archive/`

2. **Use descriptive filenames:**
   - Use UPPERCASE with underscores
   - Include document type suffix: `_GUIDE.md`, `_DESIGN.md`, `_ANALYSIS.md`

3. **Update this index:**
   - Add your new document to the appropriate table above

4. **Cross-reference appropriately:**
   - Link to related docs using relative paths

See [STRUCTURE.md](STRUCTURE.md) for complete documentation structure guidelines.

## Need Help?

- **Issues or bugs:** [Report on GitHub](https://github.com/fxstein/todo.ai/issues)
- **Questions:** Check [FAQ](FAQ.md) for common answers
- **Contributing:** See [Development Guidelines](development/DEVELOPMENT_GUIDELINES.md)

---

**Repository:** https://github.com/fxstein/todo.ai
