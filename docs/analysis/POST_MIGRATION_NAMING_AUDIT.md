# Post-Migration Naming Audit

**Date:** 2026-01-26
**Task:** #219 (Naming Unification)
**Audit Type:** Post-migration verification

## Summary

After migrating from `todo.ai` to `ai-todo`, this audit identifies remaining references to old naming conventions that need cleanup.

## Source Code Issues (Priority: High)

These are functional code references that should be updated:

### Python Package (`ai_todo/`)

| File | Line | Current | Should Be |
|------|------|---------|-----------|
| `cli/utility_ops.py` | 15 | `pip install --upgrade todo-ai` | `pip install --upgrade ai-todo` |
| `cli/utility_ops.py` | 30-32 | `pip uninstall todo-ai` | `pip uninstall ai-todo` |
| `cli/system_ops.py` | 52-54 | `pip install --upgrade todo-ai` | `pip install --upgrade ai-todo` |
| `cli/system_ops.py` | 200-202 | `pip install todo-ai==<version>` | `pip install ai-todo==<version>` |
| `cli/main.py` | 69-70 | `todo-ai tamper diff/accept` | `ai-todo tamper diff/accept` |
| `core/file_ops.py` | 899 | `todo-ai (CLI/MCP)` | `ai-todo (CLI/MCP)` |
| `core/file_ops.py` | 1063 | `todo-ai (mcp)` | `ai-todo` |
| `mcp/__main__.py` | 7 | `todo-ai-mcp` comment | `ai-todo` |
| `mcp/server.py` | 43 | `FastMCP("todo-ai")` | `FastMCP("ai-todo")` |

### Test Files

| File | Issue | Count |
|------|-------|-------|
| `tests/integration/test_mcp_cli_parity.py` | `fxstein/todo.ai` URLs in fixtures | 7 |
| `tests/integration/test_compatibility.py` | `fxstein/todo.ai` URLs + `todo.ai script` | 3 |

## Documentation Issues (Priority: Medium)

### Design Documents (`docs/design/`)

| File | Issues |
|------|--------|
| `README_REDESIGN_V3.md` | `todo-ai serve`, `todo-ai [command]` references |
| `TAMPER_DETECTION_DESIGN.md` | Multiple `todo-ai tamper` command references |
| `UNIFIED_EXECUTABLE_ARCHITECTURE.md` | `todo-ai serve` references |
| `PYTHON_REFACTOR_ARCHITECTURE.md` | `todo-ai` CLI examples |

### Guides (`docs/guides/`)

| File | Issues |
|------|--------|
| `TAMPER_DETECTION.md` | `todo-ai tamper diff/accept` examples |
| `BETA_TESTING_GUIDE.md` | `todo-ai add`, `todo-ai list` examples |

### Analysis Documents (`docs/analysis/`)

| File | Issues | Notes |
|------|--------|-------|
| `NAMING_UNIFICATION_ANALYSIS.md` | Shows old naming | **Keep as-is** (historical analysis) |
| `MCP_SERVER_PARAMETERS_ANALYSIS.md` | `todo-ai serve` | Update |

### Packaging (`docs/packaging/`)

| File | Issues |
|------|--------|
| `PUBLISH.md` | `pip install todo-ai` |

### Other

| File | Issues | Notes |
|------|--------|-------|
| `BETA_PRERELEASE_RECOMMENDATIONS.md` | `pip install todo-ai` | Update |
| `release/RELEASE_NOTES.md` | Historical `todo-ai` mentions | **Keep as-is** (release history) |

## Intentional Legacy References (Do Not Change)

These references exist for backward compatibility or historical accuracy:

### Migration Code (Backward Compatibility)

- `ai_todo/core/file_ops.py`: `OLD_DATA_DIR = ".todo.ai"` - needed for migration
- `ai_todo/core/file_ops.py`: `.todo.ai.serial` → `.ai-todo.serial` mapping
- `ai_todo/core/config.py`: `OLD_DATA_DIR = ".todo.ai"` - needed for migration
- `ai_todo/cli/*_ops.py`: Fallback paths checking `.todo.ai/` then `.ai-todo/`

### Historical Documents

- `docs/analysis/NAMING_UNIFICATION_ANALYSIS.md` - documents the confusion that led to rename
- `release/RELEASE_NOTES.md` - historical release notes
- `CHANGELOG.md` - historical changelog entries

### Legacy Shell Script

- `legacy/todo.ai` - intentionally kept as legacy, uses `.todo.ai/` directory
- `legacy/todo.bash` - bash conversion of legacy script

## GitHub URL References

All `fxstein/todo.ai` should be `fxstein/ai-todo`:

```
Found in:
- tests/integration/test_mcp_cli_parity.py (7 instances)
- tests/integration/test_compatibility.py (2 instances)
- Multiple docs/*.md files (~300+ instances across 39 files)
```

## Cleanup Checklist

### Phase 1: Source Code (Critical)
- [ ] Update `ai_todo/cli/utility_ops.py` pip commands
- [ ] Update `ai_todo/cli/system_ops.py` pip commands
- [ ] Update `ai_todo/cli/main.py` tamper command hints
- [ ] Update `ai_todo/core/file_ops.py` footer and warning
- [ ] Update `ai_todo/mcp/__main__.py` docstring
- [ ] Update `ai_todo/mcp/server.py` FastMCP name
- [ ] Update test fixtures with new GitHub URLs

### Phase 2: Documentation (Important)
- [ ] Update `docs/design/` files with `ai-todo` commands
- [ ] Update `docs/guides/` files with `ai-todo` commands
- [ ] Update `docs/packaging/PUBLISH.md`
- [ ] Skip historical/analysis documents (intentional)

### Phase 3: Verification
- [ ] Run full test suite
- [ ] Re-run this audit to confirm no regressions
- [ ] Verify `ai-todo --help` shows correct branding
