# todo.ai Documentation

Welcome to the todo.ai documentation. This directory contains comprehensive guides, design documents, and technical specifications for todo.ai.

## Quick Example

Get started with todo.ai in three simple steps:

```bash
# 1. Install
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai

# 2. Initialize
./todo.ai init

# 3. Setup (interactive wizard)
./todo.ai setup
```

That's it! You're ready to start managing tasks. Try it:

```bash
./todo.ai add "Implement user authentication" "#feature"
./todo.ai list
./todo.ai complete 1
```

---

## 📖 User Documentation

Essential guides for using todo.ai in your projects.

### Getting Started
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick start guide with installation, setup wizard, and common scenarios

### Core Guides
- **[NUMBERING_MODES_GUIDE.md](NUMBERING_MODES_GUIDE.md)** - Complete guide to all task numbering modes (single-user, multi-user, branch, enhanced)

- **[USAGE_PATTERNS.md](USAGE_PATTERNS.md)** - Real-world usage patterns for individual developers, teams, and collaborative workflows

- **[COORDINATION_SETUP.md](COORDINATION_SETUP.md)** - Step-by-step setup instructions for GitHub Issues and CounterAPI coordination services

### Migration Guides
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - How to migrate between numbering modes and handle configuration changes

---

## 🔧 Developer Documentation

Technical design documents, implementation details, and development guides.

### Architecture & Design
- **[HYBRID_TASK_NUMBERING_DESIGN.md](HYBRID_TASK_NUMBERING_DESIGN.md)** - Technical design of the hybrid task numbering system and coordination architecture

- **[MULTI_USER_DESIGN.md](MULTI_USER_DESIGN.md)** - Complete design document for multi-user and multi-branch support system

- **[TASK_NUMBERING_SCHEMA_ANALYSIS.md](TASK_NUMBERING_SCHEMA_ANALYSIS.md)** - Analysis of task numbering schemas and GitHub issue/PR number conflict prevention

### Feature Design Documents
- **[BUG_REPORTING_DESIGN.md](BUG_REPORTING_DESIGN.md)** - Design for automatic bug reporting to GitHub Issues with duplicate detection

- **[UNINSTALL_DESIGN.md](UNINSTALL_DESIGN.md)** - Design for safe uninstallation with user data preservation options

- **[TODO_TAGGING_SYSTEM_DESIGN.md](TODO_TAGGING_SYSTEM_DESIGN.md)** - Design decisions for the tagging system and task categorization

- **[GIT_HOOKS_DESIGN.md](GIT_HOOKS_DESIGN.md)** - Design for pre-commit hooks with Markdown, YAML, JSON, and TODO.md validation

### System Infrastructure
- **[MIGRATION_SYSTEM_DESIGN.md](MIGRATION_SYSTEM_DESIGN.md)** - Architecture for one-time migrations and cleanup operations

- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Guide for creating and managing migrations

- **[CURSOR_RULES_MIGRATION.md](CURSOR_RULES_MIGRATION.md)** - Migration from `.cursorrules` to `.cursor/rules/` directory structure

### Implementation & Analysis
- **[IMPLEMENTATION_ALTERNATIVES_ANALYSIS.md](IMPLEMENTATION_ALTERNATIVES_ANALYSIS.md)** - Analysis of different approaches for multi-user coordination and conflict resolution

- **[MULTI_USER_TOOL_RESEARCH.md](MULTI_USER_TOOL_RESEARCH.md)** - Research on existing tools and solutions for multi-user task coordination

- **[MULTI_USER_CONFLICT_ANALYSIS.md](MULTI_USER_CONFLICT_ANALYSIS.md)** - Analysis of conflict scenarios and resolution strategies

- **[GITHUB_API_COORDINATION_ANALYSIS.md](GITHUB_API_COORDINATION_ANALYSIS.md)** - Analysis of GitHub Issues API for atomic task number coordination

### Release & Process
- **[RELEASE_NUMBERING_MAPPING.md](RELEASE_NUMBERING_MAPPING.md)** - Mapping of commit prefixes to release types and version bump logic

- **[COMMIT_FORMAT_MIGRATION.md](COMMIT_FORMAT_MIGRATION.md)** - Plan for migrating commit messages from old format to new task number format

### Testing & Quality
- **[NUMBERING_MODES_TEST_PLAN.md](NUMBERING_MODES_TEST_PLAN.md)** - Comprehensive test plan for all numbering modes and coordination scenarios

### Historical Documents
- **[TODO_TOOL_IMPROVEMENTS.md](TODO_TOOL_IMPROVEMENTS.md)** - Historical improvement proposals for the TODO tool system

---

## 🚀 Getting Started

**New to todo.ai?** Start here:
1. Read [GETTING_STARTED.md](GETTING_STARTED.md) for quick setup
2. Explore [USAGE_PATTERNS.md](USAGE_PATTERNS.md) for your workflow
3. Check [NUMBERING_MODES_GUIDE.md](NUMBERING_MODES_GUIDE.md) for mode selection

**Contributing or extending?** Start here:
1. Read [HYBRID_TASK_NUMBERING_DESIGN.md](HYBRID_TASK_NUMBERING_DESIGN.md) for system architecture
2. Review [MIGRATION_SYSTEM_DESIGN.md](MIGRATION_SYSTEM_DESIGN.md) for adding migrations
3. Check [NUMBERING_MODES_TEST_PLAN.md](NUMBERING_MODES_TEST_PLAN.md) for testing patterns

---

## 📝 Document Conventions

- **User Documentation**: Practical guides with examples and step-by-step instructions
- **Developer Documentation**: Technical specifications and implementation details
- **Design Documents**: Architecture decisions and design rationale
- **Analysis Documents**: Research, alternatives, and decision-making processes

