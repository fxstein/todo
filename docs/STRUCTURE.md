# Documentation Structure

This document defines the organization of the `docs/` folder.

## Directory Structure

```
docs/
├── README.md           # Documentation index and navigation
├── STRUCTURE.md        # This file - structure documentation
├── guides/             # User-facing guides and tutorials
├── design/             # Technical design specifications
├── development/        # Contributor and development documentation
├── analysis/           # Research and analysis documents
└── archive/            # Historical and completed migration docs
```

## Categories

### guides/ (User-Facing Documentation)

Documentation for end users and getting started guides.

**Files:**
- `GETTING_STARTED.md` - Quick start guide for new users
- `INSTALLATION.md` - Installation instructions and troubleshooting
- `USAGE_PATTERNS.md` - Common usage scenarios and workflows
- `NUMBERING_MODES_GUIDE.md` - Complete guide to task numbering modes
- `COORDINATION_SETUP.md` - Setup guides for coordination services

**When to add here:** User-facing guides, tutorials, how-to documentation

### design/ (Technical Design Specifications)

Technical design documents explaining system architecture and feature design.

**Files:**
- `BUG_REPORTING_DESIGN.md` - Bug reporting feature design
- `GIT_HOOKS_DESIGN.md` - Git hooks integration design
- `HYBRID_TASK_NUMBERING_DESIGN.md` - Task numbering system design
- `MIGRATION_SYSTEM_DESIGN.md` - Migration system architecture
- `MULTI_USER_DESIGN.md` - Multi-user collaboration design
- `SMART_INSTALLER_DESIGN.md` - Smart installer design and logic
- `TODO_TAGGING_SYSTEM_DESIGN.md` - Task tagging system design
- `UNINSTALL_DESIGN.md` - Uninstall feature design

**When to add here:** Technical specifications, feature designs, architecture decisions

### development/ (Contributor Documentation)

Documentation for contributors and developers working on todo.ai.

**Files:**
- `DEVELOPMENT_GUIDELINES.md` - Development workflow and best practices
- `MIGRATION_GUIDE.md` - Guide for writing migration functions
- `NUMBERING_MODES_TEST_PLAN.md` - Test plan for numbering modes
- `TODO_TOOL_IMPROVEMENTS.md` - Planned improvements and roadmap

**When to add here:** Development guidelines, testing plans, contribution guides

### analysis/ (Research and Analysis)

Research documents, analysis reports, and comparison studies.

**Files:**
- `BASH_VS_ZSH_ANALYSIS.md` - Bash vs zsh comparison and recommendations
- `CODE_SIZE_ANALYSIS.md` - Codebase size analysis and optimization opportunities
- `GITHUB_API_COORDINATION_ANALYSIS.md` - GitHub API coordination analysis
- `IMPLEMENTATION_ALTERNATIVES_ANALYSIS.md` - Alternative implementation approaches
- `MULTI_USER_CONFLICT_ANALYSIS.md` - Multi-user conflict scenarios
- `MULTI_USER_TOOL_RESEARCH.md` - Research on multi-user coordination tools
- `TASK_NUMBERING_SCHEMA_ANALYSIS.md` - Task numbering schema analysis

**When to add here:** Research documents, comparative analysis, feasibility studies

### archive/ (Historical Documentation)

Completed migrations, historical context, and deprecated documentation.

**Files:**
- `COMMIT_FORMAT_MIGRATION.md` - Commit format migration (completed)
- `CURSOR_RULES_MIGRATION.md` - Cursor rules migration (completed)
- `RELEASE_NUMBERING_MAPPING.md` - Release numbering analysis (historical)
- `README_PREVIEW_WITH_SMART_INSTALLER.md` - Smart installer README preview (superseded)

**When to add here:** Completed migration docs, deprecated guides, historical context

## Adding New Documentation

When creating new documentation, follow these guidelines:

1. **Determine the category:**
   - User-facing guide? → `guides/`
   - Technical design? → `design/`
   - Development/contributor doc? → `development/`
   - Research/analysis? → `analysis/`
   - Historical/completed migration? → `archive/`

2. **Use descriptive filenames:**
   - Use UPPERCASE with underscores
   - Be specific: `FEATURE_NAME_DESIGN.md` not `DESIGN.md`
   - Include document type: `_GUIDE.md`, `_DESIGN.md`, `_ANALYSIS.md`

3. **Update docs/README.md:**
   - Add link to new document in appropriate section
   - Keep documentation index current

4. **Cross-reference appropriately:**
   - Link to related docs in other categories
   - Use relative paths: `../design/FEATURE_DESIGN.md`

## Maintenance

- Keep this structure document updated when adding new categories
- Archive completed migration docs when no longer actively referenced
- Consolidate related documents when they become too fragmented
- Review and update docs/README.md quarterly for accuracy
