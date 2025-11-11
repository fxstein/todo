# Migration and Cleanup System Design Document

**Created:** 2025-11-01  
**Status:** Design Phase  
**Version:** 1.0

## Executive Summary

This document outlines the design for a migration and cleanup system for `todo.ai` that enables one-time migrations and cleanups to be automatically executed when users update to new versions. The system allows collecting migration tasks, packaging them for releases, and ensuring they run exactly once per installation.

## Problem Statement

Currently, `todo.ai` has no mechanism to:
- Automatically fix section ordering issues on existing installations (e.g., moving "Deleted Tasks" below "Recently Completed")
- Perform one-time data migrations when file formats change
- Clean up obsolete files or configurations from previous versions
- Apply structural fixes that existing code doesn't handle automatically

**Real Example:** The implementation of task #19 moves "Deleted Tasks" section below "Recently Completed" when creating a new section, but existing installations with incorrect section order remain broken until manually fixed.

## Goals

1. **Simple Collection:** Easy way to collect cleanup/migration tasks during development
2. **Versioned Execution:** Migrations run exactly once per installation, tracked by version
3. **Safe Execution:** Migrations must be idempotent and reversible where possible
4. **Release Integration:** Seamlessly package migrations with releases
5. **Minimal Overhead:** Lightweight system that doesn't add complexity to the update process

## Design Approach

### Core Concepts

1. **Migration Registry:** A simple list of migrations with version targets
2. **Execution Tracking:** Record completed migrations in `.todo.ai/migrations/`
3. **Idempotent Functions:** Each migration checks its own state before running
4. **Version Alignment:** Migrations are tied to release versions

### Architecture

```
todo.ai
├── Migration System
│   ├── Migration registry (in script)
│   ├── Migration functions (in script)
│   └── Execution tracker (.todo.ai/migrations/)
│
.todo.ai/
├── migrations/
│   ├── v1.3.5_migrate_section_order.migrated
│   ├── v1.4.0_cleanup_old_files.migrated
│   └── .migrations_lock (prevents concurrent runs)
```

## Implementation Details

### 1. Migration Registry Structure

Migrations are registered as an array in the `todo.ai` script:

```zsh
# Migration registry
declare -a MIGRATIONS=(
    # Format: "VERSION|MIGRATION_ID|DESCRIPTION|FUNCTION_NAME"
    "1.3.5|section_order_fix|Fix TODO.md section order|migrate_section_order"
    "1.4.0|cleanup_old_backups|Remove old .bak files|cleanup_old_backup_files"
)
```

### 2. Migration Function Pattern

Each migration follows a standard pattern:

```zsh
migrate_section_order() {
    local migration_id="section_order_fix"
    local migration_file=".todo.ai/migrations/v1.3.5_${migration_id}.migrated"
    
    # Check if already migrated
    if [[ -f "$migration_file" ]]; then
        return 0  # Already done
    fi
    
    # Check prerequisites (e.g., TODO.md exists)
    if [[ ! -f "$TODO_FILE" ]]; then
        return 1
    fi
    
    # Perform migration
    # ... migration logic ...
    
    # Mark as complete
    mkdir -p "$(dirname "$migration_file")"
    touch "$migration_file"
    
    return 0
}
```

### 3. Migration Execution

Migrations run automatically on script startup (after version check, before main logic):

```zsh
run_migrations() {
    local current_version="$VERSION"
    
    # Lock to prevent concurrent execution
    local lock_file=".todo.ai/migrations/.migrations_lock"
    if [[ -f "$lock_file" ]]; then
        # Another instance is running migrations
        return 0
    fi
    touch "$lock_file"
    
    # Process each migration
    for migration in "${MIGRATIONS[@]}"; do
        IFS='|' read -r target_version migration_id description function_name <<< "$migration"
        
        # Check if this migration applies to current or earlier version
        if version_compare "$current_version" "$target_version" ">="; then
            # Check if already executed
            local migration_file=".todo.ai/migrations/v${target_version}_${migration_id}.migrated"
            if [[ ! -f "$migration_file" ]]; then
                # Run migration
                if "$function_name"; then
                    echo "✓ Migration: $description" >&2
                else
                    echo "✗ Migration failed: $description" >&2
                fi
            fi
        fi
    done
    
    rm -f "$lock_file"
}
```

### 4. Version Comparison Function

Simple semantic version comparison:

```zsh
version_compare() {
    local version1="$1"
    local version2="$2"
    local operator="$3"
    
    # Convert versions to comparable format (1.3.5 -> 1003005)
    local v1_num=$(echo "$version1" | awk -F. '{printf "%d%03d%03d", $1, $2, $3}')
    local v2_num=$(echo "$version2" | awk -F. '{printf "%d%03d%03d", $1, $2, $3}')
    
    case "$operator" in
        ">=") [[ $v1_num -ge $v2_num ]] ;;
        ">")  [[ $v1_num -gt $v2_num ]] ;;
        "<=") [[ $v1_num -le $v2_num ]] ;;
        "<")  [[ $v1_num -lt $v2_num ]] ;;
        "==") [[ $v1_num -eq $v2_num ]] ;;
        *) return 1 ;;
    esac
}
```

## Example Migrations

### Migration 1: Fix Section Order

**Problem:** Task #19 implementation fixes section order when creating sections, but existing installations may have incorrect order.

**Migration:** Reorder sections in existing TODO.md files.

```zsh
migrate_section_order() {
    local migration_id="section_order_fix"
    local migration_file=".todo.ai/migrations/v1.3.5_${migration_id}.migrated"
    
    if [[ -f "$migration_file" ]]; then
        return 0
    fi
    
    if [[ ! -f "$TODO_FILE" ]]; then
        return 1
    fi
    
    # Check if sections are in wrong order (Deleted Tasks before Recently Completed)
    local deleted_line=$(grep -n "^## Deleted Tasks" "$TODO_FILE" | cut -d: -f1)
    local recently_completed_line=$(grep -n "^## Recently Completed" "$TODO_FILE" | cut -d: -f1)
    
    # If both exist and Deleted is before Recently Completed, fix it
    if [[ -n "$deleted_line" ]] && [[ -n "$recently_completed_line" ]] && [[ $deleted_line -lt $recently_completed_line ]]; then
        # Extract and reorder sections
        # ... implementation to move Deleted Tasks section after Recently Completed ...
        echo "Reordered TODO.md sections" >&2
    fi
    
    mkdir -p "$(dirname "$migration_file")"
    touch "$migration_file"
    return 0
}
```

### Migration 2: Cleanup Old Backup Files

**Problem:** Old backup files (`.bak`) from previous versions clutter the `.todo.ai/` directory.

**Migration:** Remove obsolete backup files.

```zsh
cleanup_old_backup_files() {
    local migration_id="cleanup_old_backups"
    local migration_file=".todo.ai/migrations/v1.4.0_${migration_id}.migrated"
    
    if [[ -f "$migration_file" ]]; then
        return 0
    fi
    
    # Remove old .bak files if backups/ directory exists (new system uses backups/)
    local bak_files=$(find .todo.ai -name "*.bak" -type f 2>/dev/null)
    if [[ -n "$bak_files" ]] && [[ -d ".todo.ai/backups" ]]; then
        echo "$bak_files" | xargs rm -f 2>/dev/null || true
        echo "Removed old .bak files" >&2
    fi
    
    mkdir -p "$(dirname "$migration_file")"
    touch "$migration_file"
    return 0
}
```

## Integration with Release Process

### Adding Migrations to a Release

1. **During Development:**
   - Identify migration needs
   - Write migration function
   - Add to migration registry with target version
   - Test locally

2. **Before Release:**
   - Review migrations for release
   - Ensure migrations are idempotent
   - Update release notes with migration info

3. **During Release:**
   - Migrations are included automatically in the new version
   - No additional release steps needed

### Release Notes Example

```markdown
## Migration Notes

This release includes automatic migrations that will run once on update:

- **Section Order Fix (v1.3.5):** Automatically reorders TODO.md sections to correct order
- **Backup Cleanup (v1.4.0):** Removes obsolete .bak files from previous versions
```

## Safety Features

### 1. Idempotency

All migrations must be idempotent - running them multiple times has no effect beyond the first execution.

### 2. Locking

File-based lock prevents concurrent migration execution.

### 3. Prerequisites Checking

Migrations check for prerequisites (file existence, etc.) before running.

### 4. Error Handling

Failed migrations don't block script execution but are logged.

### 5. Rollback Support (Future)

Future enhancement: store migration state for potential rollback.

## Testing Strategy

### Unit Tests

- Test each migration function in isolation
- Verify idempotency (running twice produces same result)
- Test version comparison logic

### Integration Tests

- Test migration execution during update
- Verify migration tracking files are created
- Test concurrent execution prevention

### Migration Tests

- Create test TODO.md with wrong section order
- Run migration
- Verify sections are reordered correctly
- Verify migration file is created
- Run again to verify idempotency

## File Structure

```
.todo.ai/
├── migrations/
│   ├── .migrations_lock          # Lock file (temporary)
│   ├── v1.3.5_section_order_fix.migrated
│   └── v1.4.0_cleanup_old_backups.migrated
```

## Benefits

1. **Automatic Fixes:** Existing installations are automatically fixed
2. **Developer-Friendly:** Simple to add new migrations
3. **User-Transparent:** Migrations run silently during normal operation
4. **Version-Tracked:** Each migration is tied to a specific version
5. **Safe:** Idempotent execution prevents issues

## Future Enhancements

1. **Rollback Capability:** Store state to allow migration rollback
2. **Migration Status Command:** `./todo.ai migrations list` to show migration status
3. **Dry-Run Mode:** Test migrations without executing
4. **Migration Validation:** Verify migration requirements before release

## Implementation Checklist

- [ ] Create migration registry structure
- [ ] Implement version comparison function
- [ ] Implement migration execution system
- [ ] Create migration lock mechanism
- [ ] Implement first migration (section order fix)
- [ ] Add migration execution to script startup
- [ ] Create tests for migration system
- [ ] Document migration creation process
- [ ] Update release process documentation

## Open Questions

1. Should migrations run on every script execution or only on update?
   - **Decision:** Run on every execution (fast check via file existence)
   
2. Should we support migration dependencies?
   - **Decision:** Not initially - migrations should be independent
   
3. How to handle failed migrations?
   - **Decision:** Log error but don't block script - user can manually fix

## References

- Task #19: Move Deleted Tasks section below Recently Completed section
- Task #37: Build release migration and cleanup system

