# Architecture Design: Python Refactor with MCP and CLI Interfaces

**Created:** 2025-12-12
**Status:** Validated
**Version:** 1.1
**Related Issue:** #39

## Executive Summary

This document outlines the architecture for refactoring `todo.ai` from a shell script (zsh/bash) into a Python-based application with **dual interfaces**: Model Context Protocol (MCP) server and Command-Line Interface (CLI). The core logic will be implemented once and shared by both interfaces, ensuring consistency and maintainability.

**Key Goals:**
- ✅ Maintain existing CLI functionality and command syntax
- ✅ Add MCP server interface for AI agent integration
- ✅ Single implementation of core logic (no duplication)
- ✅ System-wide installation via pipx
- ✅ Cross-platform compatibility
- ✅ Preserve data format compatibility (.todo.ai/, TODO.md)

---

## Current Architecture Analysis

### Current Implementation (Shell Script)

**File Structure:**
```
todo.ai (5,257 lines, 81 functions)
├── Core functionality (all in single file)
│   ├── Task management (add, complete, delete, archive, restore)
│   ├── Subtask management (2-level nesting)
│   ├── Multi-user coordination (4 modes)
│   ├── GitHub API integration
│   ├── Migration system
│   ├── Backup/rollback
│   ├── Bug reporting
│   ├── Cursor rules management
│   ├── Git hooks integration
│   └── Release management
└── Configuration
    └── .todo.ai/
        ├── config.yaml
        ├── .todo.ai.serial
        ├── .todo.ai.log
        └── migrations/
```

**Key Characteristics:**
- **Monolithic:** All functionality in single file
- **Shell-based:** zsh/bash with sed, grep, awk for text processing
- **Dependencies:** zsh, git, yq/python3 (optional for YAML)
- **Platform:** Unix-like systems (macOS, Linux)
- **Installation:** Single file download, manual PATH setup

**Strengths:**
- ✅ Simple deployment (single file)
- ✅ Fast startup (no compilation)
- ✅ No runtime dependencies (beyond shell)
- ✅ Works on any Unix system

**Limitations:**
- ⚠️ Hard to maintain (5,257 lines in one file)
- ⚠️ Limited cross-platform support (no Windows)
- ⚠️ Complex text processing (sed/grep patterns)
- ⚠️ Difficult to test (shell testing frameworks limited)
- ⚠️ No MCP integration (can't be used by MCP-compatible tools)
- ⚠️ Manual PATH management for installation

---

## Proposed Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                  Core Logic (Python)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Task Management Module                           │  │
│  │  - Task CRUD operations                           │  │
│  │  - Subtask management                             │  │
│  │  - Archive/restore                                │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  File Operations Module                           │  │
│  │  - TODO.md parsing/generation                     │  │
│  │  - Serial file management                         │  │
│  │  - Log file operations                            │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Coordination Module                              │  │
│  │  - Multi-user coordination (4 modes)              │  │
│  │  - Git integration                                │  │
│  │  - Conflict resolution                            │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  GitHub Integration Module                        │  │
│  │  - Issue management                               │  │
│  │  - Bug reporting                                  │  │
│  │  - API client                                     │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Migration System Module                          │  │
│  │  - Migration registry                             │  │
│  │  - Execution tracking                             │  │
│  │  - Version management                             │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Configuration Module                             │  │
│  │  - YAML config parsing                            │  │
│  │  - Environment variables                          │  │
│  │  - Default values                                 │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         │                              │
         │                              │
    ┌────▼────┐                    ┌────▼────┐
    │   MCP   │                    │   CLI   │
    │  Server │                    │Interface│
    └─────────┘                    └─────────┘
```

### Core Principles

1. **Single Source of Truth:** All business logic in core Python modules
2. **Interface Abstraction:** MCP and CLI are thin wrappers around core logic
3. **Data Compatibility:** Preserve existing file formats and directory structure
4. **Backward Compatibility:** CLI maintains existing command syntax
5. **Testability:** Core logic is unit-testable without interface dependencies
6. **Environment Isolation:** ALL dependencies must be managed in a virtual environment (`venv`). No system-wide package pollution.

---

## Core Logic Design

### Module Structure

```
todo_ai/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── task.py              # Task data models and operations
│   ├── file_ops.py          # File I/O operations
│   ├── coordination.py       # Multi-user coordination
│   ├── github_client.py     # GitHub API integration
│   ├── migrations.py        # Migration system
│   ├── rules.py             # Cursor rules management
│   ├── hooks.py             # Git hooks integration
│   └── config.py           # Configuration management
├── parsers/
│   ├── __init__.py
│   ├── markdown.py          # TODO.md parsing/generation
│   └── yaml.py             # Config file parsing
└── utils/
    ├── __init__.py
    ├── git.py              # Git operations
    └── logging.py          # Logging utilities
```

### Core Module: `task.py`

**Purpose:** Task data models and business logic

**Key Classes:**
```python
class Task:
    """Represents a single task with metadata"""
    id: str                    # e.g., "42" or "42.1"
    description: str
    status: TaskStatus        # PENDING, COMPLETED, ARCHIVED, DELETED
    tags: List[str]
    notes: List[str]
    relationships: List[str]  # Related task IDs
    created_at: datetime
    updated_at: datetime

class TaskManager:
    """Core task management operations"""
    def add_task(self, description: str, tags: List[str]) -> Task
    def complete_task(self, task_id: str) -> Task
    def delete_task(self, task_id: str) -> Task
    def archive_task(self, task_id: str) -> Task
    def restore_task(self, task_id: str) -> Task
    def modify_task(self, task_id: str, **kwargs) -> Task
    def add_subtask(self, parent_id: str, description: str, tags: List[str]) -> Task
    def get_task(self, task_id: str) -> Task
    def list_tasks(self, filters: Dict) -> List[Task]
```

### Core Module: `file_ops.py`

**Purpose:** File I/O operations for TODO.md and .todo.ai/ files

**Key Functions:**
```python
class FileManager:
    """Manages file operations for todo.ai data"""
    def read_todo_file(self, path: str) -> List[Task]
    def write_todo_file(self, path: str, tasks: List[Task]) -> None
    def read_serial_file(self, path: str) -> int
    def write_serial_file(self, path: str, serial: int) -> None
    def read_log_file(self, path: str) -> List[LogEntry]
    def append_log_entry(self, path: str, entry: LogEntry) -> None
    def backup_file(self, path: str) -> str
    def restore_backup(self, backup_path: str, target_path: str) -> None
```

### Core Module: `coordination.py`

**Purpose:** Multi-user coordination logic

**Key Classes:**
```python
class CoordinationManager:
    """Handles multi-user coordination modes"""
    def __init__(self, mode: str, config: Config)

    def get_next_task_id(self, current_max: int) -> int
    def sync_with_remote(self) -> Dict[str, Any]
    def resolve_conflicts(self, local_tasks: List[Task], remote_tasks: List[Task]) -> List[Task]

    # Modes: single-user, multi-user, branch, enhanced
```

### Core Module: `github_client.py`

**Purpose:** GitHub API integration

**Key Classes:**
```python
class GitHubClient:
    """GitHub API client for issue management and bug reporting"""
    def __init__(self, token: Optional[str] = None)

    def create_issue(self, title: str, body: str, labels: List[str]) -> Dict
    def close_issue(self, issue_number: int, comment: Optional[str] = None) -> Dict
    def get_issue(self, issue_number: int) -> Dict
    def list_issues(self, labels: Optional[List[str]] = None) -> List[Dict]
    def report_bug(self, description: str, context: str, command: str) -> Dict
```

### Core Module: `migrations.py`

**Purpose:** Migration system for version upgrades

**Key Classes:**
```python
class MigrationRegistry:
    """Manages migration execution"""
    def __init__(self, migrations_dir: str)

    def register_migration(self, version: str, migration_id: str, func: Callable) -> None
    def run_pending_migrations(self, current_version: str) -> List[str]
    def is_migration_complete(self, version: str, migration_id: str) -> bool
```

### Core Module: `rules.py`

**Purpose:** Management of Cursor AI rules (.cursor/rules/)

**Key Classes:**
```python
class RulesManager:
    """Manages Cursor AI rules installation and updates"""
    def __init__(self, rules_dir: str)

    def init_rules(self) -> None
    def update_rules(self) -> None
    def get_rule_content(self, rule_name: str) -> str
    def detect_project_root(self) -> str
```

### Core Module: `hooks.py`

**Purpose:** Management of Git hooks

**Key Functions:**
```python
def install_git_hooks(hooks_dir: str) -> None
def uninstall_git_hooks(hooks_dir: str) -> None
def check_git_hooks_status() -> Dict[str, bool]
```

### Core Module: `config.py`

**Purpose:** Configuration management

**Key Classes:**
```python
class Config:
    """Manages todo.ai configuration"""
    def __init__(self, config_path: str)

    def get(self, key: str, default: Any = None) -> Any
    def set(self, key: str, value: Any) -> None
    def get_numbering_mode(self) -> str
    def get_coordination_type(self) -> str
```

---

## MCP Server Interface Design

### MCP Protocol Overview

Model Context Protocol (MCP) enables AI tools to interact with external services through standardized tools and resources.

**Key Concepts:**
- **Tools:** Functions that AI agents can call (e.g., `add_task`, `complete_task`)
- **Resources:** Data that AI agents can read (e.g., `TODO.md` content)
- **Prompts:** Template prompts for common operations

### MCP Server Structure

```
todo_ai/
└── mcp/
    ├── __init__.py
    ├── server.py           # MCP server implementation
    ├── tools.py            # MCP tool definitions
    ├── resources.py        # MCP resource definitions
    └── prompts.py          # MCP prompt templates
```

### MCP Tools

**Tool Definitions:**
```python
MCP_TOOLS = [
    {
        "name": "add_task",
        "description": "Add a new task to TODO.md",
        "inputSchema": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["description"]
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as complete",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string"}
            },
            "required": ["task_id"]
        }
    },
    # ... all other commands as MCP tools
]
```

**Tool Implementation:**
```python
class MCPServer:
    """MCP server implementation"""
    def __init__(self, core_manager: TaskManager):
        self.core = core_manager

    async def handle_tool_call(self, tool_name: str, arguments: Dict) -> Dict:
        """Route MCP tool calls to core logic"""
        if tool_name == "add_task":
            task = self.core.add_task(
                description=arguments["description"],
                tags=arguments.get("tags", [])
            )
            return {"task_id": task.id, "status": "success"}

        # ... route all tools to core logic
```

### MCP Resources

**Resource Definitions:**
```python
MCP_RESOURCES = [
    {
        "uri": "todo://todo.md",
        "name": "TODO.md",
        "description": "Main task list file",
        "mimeType": "text/markdown"
    },
    {
        "uri": "todo://config.yaml",
        "name": "Configuration",
        "description": "todo.ai configuration file",
        "mimeType": "application/yaml"
    }
]
```

**Resource Implementation:**
```python
async def handle_resource_read(self, uri: str) -> str:
    """Read MCP resources"""
    if uri == "todo://todo.md":
        return self.core.file_manager.read_todo_file(self.core.todo_path)
    elif uri == "todo://config.yaml":
        return self.core.config.read_config_file()
```

### MCP Server Entry Point

```python
# todo_ai/mcp/__main__.py
async def main():
    """MCP server entry point"""
    core_manager = TaskManager(...)
    server = MCPServer(core_manager)

    # Start MCP server (stdin/stdout for MCP protocol)
    await server.run()
```

---

## CLI Interface Design

### CLI Structure

```
todo_ai/
└── cli/
    ├── __init__.py
    ├── main.py            # CLI entry point
    ├── commands/          # Command implementations
    │   ├── __init__.py
    │   ├── add.py
    │   ├── complete.py
    │   ├── delete.py
    │   ├── archive.py
    │   └── ... (all commands)
    └── parser.py          # Argument parsing (click/argparse)
```

### CLI Command Pattern

**Example: Add Command**
```python
# todo_ai/cli/commands/add.py
from todo_ai.core.task import TaskManager

def add_command(description: str, tags: List[str] = None):
    """CLI implementation of add command"""
    # Initialize core manager
    manager = TaskManager.from_config()

    # Call core logic (same as MCP would call)
    task = manager.add_task(description=description, tags=tags or [])

    # Format output for CLI
    print(f"Added: #{task.id} {task.description}")
    return task
```

### CLI Entry Point

```python
# todo_ai/cli/main.py
import click
from todo_ai.cli.commands import add_command, complete_command, ...

@click.group()
def cli():
    """todo.ai - AI-Agent First TODO List Tracker"""
    pass

@cli.command()
@click.argument('description')
@click.option('--tags', multiple=True)
def add(description, tags):
    """Add a new task"""
    add_command(description, list(tags))

@cli.command()
@click.argument('task_id')
def complete(task_id):
    """Mark a task as complete"""
    complete_command(task_id)

# ... all other commands

if __name__ == '__main__':
    cli()
```

### CLI Compatibility

**Maintain Existing Syntax:**
- `todo.ai add "description"` → `todo-ai add "description"`
- `todo.ai complete 42` → `todo-ai complete 42`
- `todo.ai list` → `todo-ai list`
- All existing commands work identically

**Entry Point:**
- After pipx installation: `todo-ai` command available system-wide
- Maintains backward compatibility with existing workflows

---

## Installation and Distribution

### Package Structure

```
todo-ai/
├── pyproject.toml          # Python package configuration
├── setup.py               # Setup script (if needed)
├── README.md
├── LICENSE
├── todo_ai/               # Main package
│   ├── __init__.py
│   ├── core/             # Core logic
│   ├── mcp/              # MCP server
│   ├── cli/              # CLI interface
│   └── ...
└── tests/                # Test suite
```

### pyproject.toml

```toml
[project]
name = "todo-ai"
version = "3.0.0"
description = "AI-Agent First TODO List Tracker with MCP and CLI interfaces"
requires-python = ">=3.8"
dependencies = [
    "mcp>=0.1.0",
    "click>=8.0.0",
    "pyyaml>=6.0",
    "requests>=2.28.0",
    "pygithub>=1.59.0",
]

[project.scripts]
todo-ai = "todo_ai.cli.main:cli"
todo-ai-mcp = "todo_ai.mcp.__main__:main"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### Installation via pipx

**User Installation:**
```bash
pipx install todo-ai
```

**After Installation:**
- `todo-ai` command available system-wide (CLI)
- `todo-ai-mcp` command available (MCP server)
- Both use same core logic

**Update:**
```bash
pipx upgrade todo-ai
```

### Distribution

**Release Process:**
1. Build Python package: `python -m build`
2. Upload to PyPI: `twine upload dist/*`
3. Users install via: `pipx install todo-ai`

**Platform Support:**
- ✅ macOS (Intel and Apple Silicon)
- ✅ Linux (all distributions)
- ✅ Windows (via pipx)

---

## Migration Strategy

### Phase 1: Parallel Development

**Goal:** Develop Python version alongside shell version

**Approach:**
- Keep shell version functional during development
- Use shell version to track progress (meta-tracking)
- Test Python version with isolated test data (separate TODO.md)
- No disruption to existing users

**Test Data Isolation:**
- Create dedicated test directory: `tests/integration/test_data/`
- Copy TODO.md structure for testing
- Never modify live project TODO.md during development

### Phase 2: Feature Parity

**Goal:** Achieve 100% feature parity with shell version

**Checklist:**
- [ ] All CLI commands implemented
- [ ] All core functionality ported
- [ ] Data format compatibility verified
- [ ] Migration system working
- [ ] GitHub integration working
- [ ] Multi-user coordination working

### Phase 3: MCP Implementation

**Goal:** Add MCP server interface

**Checklist:**
- [ ] MCP server implementation
- [ ] All tools exposed via MCP
- [ ] Resources exposed via MCP
- [ ] MCP server tested with Cursor/Claude Desktop

### Phase 4: Testing and Validation

**Goal:** Comprehensive testing with isolated test data

**Approach:**
- Unit tests for core logic
- Integration tests for CLI
- Integration tests for MCP
- End-to-end tests with test TODO.md
- Performance testing
- Cross-platform testing

### Phase 5: Migration Path for Users

**Goal:** Smooth transition for existing users

**Migration Script:**
```python
# todo_ai/migrate.py
def migrate_from_shell():
    """Migrate from shell version to Python version"""
    # 1. Detect shell version installation
    # 2. Verify data compatibility
    # 3. Install Python version via pipx
    # 4. Verify Python version works
    # 5. Optionally remove shell version
```

**User Instructions:**
1. Install Python version: `pipx install todo-ai`
2. Test with existing data: `todo-ai list`
3. Verify all commands work
4. Optionally remove shell version

### Phase 6: Release

**Goal:** Release Python version as primary

**Approach:**
- Release Python version as v3.0.0
- Keep shell version available as legacy option
- Update documentation
- Provide migration guide
- **Requirement:** Release must advise `pipx` installation to ensure environment isolation

---

## Data Format Compatibility

### Preserved Formats

**TODO.md Format:**
- Markdown structure unchanged
- Task ID format: `#42` or `**#42**`
- Subtask format: `#42.1`, `#42.2`
- Section structure: Tasks, Recently Completed, Deleted Tasks, Archived Tasks
- Tag format: `` `#tag` ``
- Notes format: `> Note text`

**.todo.ai/ Directory:**
- `config.yaml` - Same YAML structure
- `.todo.ai.serial` - Same integer format
- `.todo.ai.log` - Same log format
- `migrations/` - Same migration tracking

**No Breaking Changes:**
- Python version reads/writes same formats
- Shell version and Python version can coexist
- Data migration not required

---

## Testing Strategy

### Test Structure

```
tests/
├── unit/
│   ├── test_task.py
│   ├── test_file_ops.py
│   ├── test_coordination.py
│   └── ...
├── integration/
│   ├── test_cli.py
│   ├── test_mcp.py
│   └── test_data/          # Isolated test TODO.md
│       ├── TODO.md
│       └── .todo.ai/
└── e2e/
    └── test_workflows.py
```

### Test Data Isolation

**Critical Requirement:**
- **NEVER** use live project TODO.md for testing
- Always use `tests/integration/test_data/TODO.md`
- Create fresh test data for each test run
- Clean up test data after tests

**Test Data Setup:**
```python
@pytest.fixture
def test_todo_file(tmp_path):
    """Create isolated test TODO.md"""
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text("# Tasks\n\n- [ ] **#1** Test task\n")
    return todo_file
```

### Test Coverage Goals

- **Unit Tests:** 90%+ coverage of core logic
- **Integration Tests:** All CLI commands
- **Integration Tests:** All MCP tools
- **E2E Tests:** Complete workflows

---

## Implementation Phases

### Phase 1: Design and Setup (Task #163.1-163.6)

1. **163.1:** Create architecture design document ✅ (this document)
2. **163.2:** Design core module structure and interfaces
3. **163.3:** Design MCP server interface specification
4. **163.4:** Design CLI interface specification
5. **163.5:** Design data format compatibility layer
6. **163.6:** Create project structure and setup development environment

### Phase 2: Core Implementation (Task #163.7-163.13)

1. **163.7:** Implement task data models and TaskManager
2. **163.8:** Implement file operations module (TODO.md parsing/generation)
3. **163.9:** Implement configuration module
4. **163.10:** Implement coordination module
5. **163.11:** Implement GitHub client module
6. **163.12:** Implement migration system module
7. **163.13:** Implement utility modules (git, logging)

### Phase 3: CLI Implementation (Task #163.14-163.16)

1. **163.14:** Implement CLI argument parser and command routing
2. **163.15:** Implement all CLI commands (add, complete, delete, etc.)
3. **163.16:** Implement CLI output formatting and error handling

### Phase 4: MCP Implementation (Task #163.17-163.19)

1. **163.17:** Implement MCP server framework
2. **163.18:** Implement MCP tools (expose all commands as tools)
3. **163.19:** Implement MCP resources (TODO.md, config as resources)

### Phase 5: Testing (Task #163.20-163.28)

1. **163.20:** Set up test framework and test data isolation
2. **163.21:** Write unit tests for core modules
3. **163.22:** Write integration tests for CLI commands
4. **163.23:** Write integration tests for MCP tools
5. **163.24:** Write end-to-end workflow tests
6. **163.25:** Test data format compatibility with shell version
7. **163.26:** Test cross-platform compatibility (macOS, Linux, Windows)
8. **163.27:** Performance testing and optimization
9. **163.28:** Test migration system with version upgrades

### Phase 6: Validation (Task #163.29-163.30)

1. **163.29:** Feature parity validation against shell version
2. **163.30:** User acceptance testing with real workflows

### Phase 7: Documentation and Release (Task #163.31-163.35)

1. **163.31:** Write user documentation for Python version
2. **163.32:** Write migration guide from shell to Python version
3. **163.33:** Write developer documentation
4. **163.34:** Prepare release package (pyproject.toml, setup)
5. **163.35:** Create release plan and execute v3.0.0 release

---

## Critical Requirements

### Must-Have Features

1. **Dual Interfaces:**
   - ✅ MCP server interface (for AI agent integration)
   - ✅ CLI interface (for direct usage)

2. **Shared Core Logic:**
   - ✅ Single implementation of all functionality
   - ✅ No code duplication between interfaces

3. **Backward Compatibility:**
   - ✅ CLI commands maintain existing syntax
   - ✅ Data formats unchanged (.todo.ai/, TODO.md)

4. **Installation:**
   - ✅ System-wide installation via pipx
   - ✅ Both CLI and MCP available after installation

5. **Testing:**
   - ✅ Isolated test data (never use live TODO.md)
   - ✅ Comprehensive test coverage

6. **Environment Isolation:**
   - ✅ STRICT REQUIREMENT: No system-wide library installation
   - ✅ Development: Use `python -m venv .venv`
   - ✅ Production: Use `pipx` (creates isolated venv per tool)

### Constraints

1. **Shell Version Continuity:**
   - Shell version must continue working during development
   - Use shell version to track progress (meta-tracking)
   - No disruption to existing users

2. **Test Data Isolation:**
   - **NEVER** modify live project TODO.md during development
   - Always use separate test data directory
   - Create fresh test data for each test run

3. **Data Compatibility:**
   - Python version must read/write same formats as shell version
   - No breaking changes to data structures
   - Migration not required for existing data

---

## Technology Stack

### Core Dependencies

- **Python 3.8+:** Minimum Python version
- **mcp:** MCP protocol library
- **click:** CLI framework
- **pyyaml:** YAML parsing
- **requests:** HTTP client for GitHub API
- **pygithub:** GitHub API client

### Development Dependencies

- **pytest:** Testing framework
- **pytest-cov:** Coverage reporting
- **black:** Code formatting
- **mypy:** Type checking
- **ruff:** Linting

### Build and Distribution

- **setuptools:** Package building
- **wheel:** Binary distribution
- **twine:** PyPI upload
- **pipx:** User installation

---

## Success Criteria

### Functional Requirements

- ✅ All CLI commands work identically to shell version
- ✅ MCP server exposes all functionality as tools
- ✅ Data format compatibility maintained
- ✅ Cross-platform support (macOS, Linux, Windows)
- ✅ System-wide installation via pipx

### Quality Requirements

- ✅ 90%+ test coverage for core logic
- ✅ All integration tests passing
- ✅ Performance comparable to shell version
- ✅ No data loss during migration

### User Experience

- ✅ Smooth migration from shell version
- ✅ CLI commands feel identical to shell version
- ✅ MCP integration works with Cursor/Claude Desktop
- ✅ Clear documentation and migration guide

---

## Design Decisions

1. **MCP Library:**
   - **Decision:** Use official `mcp` Python SDK
   - **Rationale:** Standard implementation, likely to have best support

2. **CLI Framework:**
   - **Decision:** `click`
   - **Rationale:** Robust, composable, excellent documentation, widely used in Python ecosystem

3. **Version Numbering:**
   - **Decision:** `v3.0.0`
   - **Rationale:** Complete rewrite warrants major version bump

4. **Shell Version Strategy:**
   - **Decision:** Freeze and Deprecate
   - **Rationale:** Shell version enters maintenance mode. New features only in Python version.

5. **Migration Strategy:**
   - **Decision:** Manual installation via `pipx`
   - **Rationale:** Data format is compatible. No data migration needed. `pipx` handles the binary replacement.

---

## Next Steps

1. **Setup:** Create Python project structure
2. **Implementation:** Start with `core/task.py` and `core/file_ops.py`
3. **CLI:** Implement basic `list` and `add` commands
4. **MCP:** Implement basic server with `list` and `add` tools
5. **Iterate:** Port remaining functionality incrementally

---

## References

- **Issue #39:** Feature Request: Refactor todo.ai into Python-based MCP server
- **Current Implementation:** `todo.ai` (shell script, 5,257 lines)
- **MCP Protocol:** https://modelcontextprotocol.io/
- **pipx Documentation:** https://pipx.pypa.io/

---

**Document Status:** Validated
**Last Updated:** 2025-12-12
**Next Review:** Implementation Phase
