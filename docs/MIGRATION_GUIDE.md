# Migration Creation Guide

**Created:** 2025-11-01  
**Version:** 1.0

## Overview

This guide explains how to create new migrations for `todo.ai`. Migrations are one-time operations that automatically fix issues in existing installations when users update to new versions.

## When to Create a Migration

Create a migration when:
- A change affects existing installations (e.g., file format changes)
- Structural fixes are needed (e.g., section reordering)
- Cleanup tasks need to run once per installation
- Data format changes require conversion

**Example:** Task #19 fixed section order when creating new sections, but existing installations with incorrect order needed automatic fixing.

## Migration Function Pattern

All migrations follow this standard pattern:

```zsh
migrate_example_name() {
    local migration_id="example_name"
    local migrations_dir="$(pwd)/.todo.ai/migrations"
    local migration_file="${migrations_dir}/v1.4.0_${migration_id}.migrated"
    
    # Check if already migrated
    if [[ -f "$migration_file" ]]; then
        return 0  # Already done
    fi
    
    # Check prerequisites (e.g., TODO.md exists)
    if [[ ! -f "$TODO_FILE" ]]; then
        return 1
    fi
    
    # Perform migration
    # ... your migration logic here ...
    
    # Mark as complete
    mkdir -p "$migrations_dir" 2>/dev/null || return 1
    touch "$migration_file" 2>/dev/null || return 1
    
    return 0
}
```

## Step-by-Step: Creating a New Migration

### Step 1: Write the Migration Function

Create a function following the pattern above. Key requirements:

1. **Idempotent:** Safe to run multiple times (checks `.migrated` file first)
2. **Prerequisites:** Check required files/conditions exist
3. **Error Handling:** Return appropriate exit codes
4. **User Feedback:** Use `echo "✓ Migration: ..." >&2` for success messages

### Step 2: Add to Migration Registry

Add your migration to the `MIGRATIONS` array in `todo.ai`:

```zsh
declare -a MIGRATIONS=(
    "1.3.5|section_order_fix|Fix TODO.md section order|migrate_section_order"
    "1.4.0|your_migration_id|Your migration description|your_migration_function"
)
```

**Format:** `"VERSION|MIGRATION_ID|DESCRIPTION|FUNCTION_NAME"`

- **VERSION:** Target version for this migration (usually the version where the fix is needed)
- **MIGRATION_ID:** Unique identifier (snake_case)
- **DESCRIPTION:** Human-readable description
- **FUNCTION_NAME:** Name of the migration function

### Step 3: Test the Migration

1. **Test Idempotency:**
   ```bash
   # Run migration
   ./todo.ai list
   
   # Run again - should skip (idempotent)
   ./todo.ai list
   ```

2. **Test with Wrong State:**
   - Create a TODO.md file with the problem state
   - Run the migration
   - Verify it fixes the issue

3. **Test Version Check:**
   - Verify migration runs when version >= target version
   - Verify migration doesn't run when version < target version

### Step 4: Update Version (If Needed)

If this migration should run in a future release, ensure the target version matches the release version where the fix is needed.

## Examples

### Example 1: Section Order Fix

```zsh
migrate_section_order() {
    local migration_id="section_order_fix"
    local migrations_dir="$(pwd)/.todo.ai/migrations"
    local migration_file="${migrations_dir}/v1.3.5_${migration_id}.migrated"
    
    if [[ -f "$migration_file" ]]; then
        return 0
    fi
    
    if [[ ! -f "$TODO_FILE" ]]; then
        return 1
    fi
    
    # Check if sections are in wrong order
    local deleted_line=$(grep -n "^## Deleted Tasks" "$TODO_FILE" | cut -d: -f1 | head -1)
    local recently_completed_line=$(grep -n "^## Recently Completed" "$TODO_FILE" | cut -d: -f1 | head -1)
    
    # Fix if needed
    if [[ -n "$deleted_line" ]] && [[ -n "$recently_completed_line" ]] && [[ $deleted_line -lt $recently_completed_line ]]; then
        # ... reorder sections ...
        echo "✓ Migration: Fixed TODO.md section order" >&2
    fi
    
    mkdir -p "$migrations_dir" 2>/dev/null || return 1
    touch "$migration_file" 2>/dev/null || return 1
    return 0
}
```

### Example 2: Cleanup Old Files

```zsh
cleanup_old_backup_files() {
    local migration_id="cleanup_old_backups"
    local migrations_dir="$(pwd)/.todo.ai/migrations"
    local migration_file="${migrations_dir}/v1.4.0_${migration_id}.migrated"
    
    if [[ -f "$migration_file" ]]; then
        return 0
    fi
    
    # Remove old .bak files if backups/ directory exists
    local bak_files=$(find .todo.ai -name "*.bak" -type f 2>/dev/null)
    if [[ -n "$bak_files" ]] && [[ -d ".todo.ai/backups" ]]; then
        echo "$bak_files" | xargs rm -f 2>/dev/null || true
        echo "✓ Migration: Removed old .bak files" >&2
    fi
    
    mkdir -p "$migrations_dir" 2>/dev/null || return 1
    touch "$migration_file" 2>/dev/null || return 1
    return 0
}
```

## Best Practices

### 1. Idempotency

Always check for the `.migrated` file first:

```zsh
if [[ -f "$migration_file" ]]; then
    return 0  # Already done
fi
```

### 2. Prerequisites Checking

Verify required files/conditions exist:

```zsh
if [[ ! -f "$TODO_FILE" ]]; then
    return 1
fi
```

### 3. Error Handling

Return appropriate exit codes:
- `0` = Success (or already completed)
- `1` = Failure (e.g., missing prerequisites)

### 4. User Feedback

Provide clear feedback:

```zsh
echo "✓ Migration: Fixed TODO.md section order" >&2
```

Or for warnings:

```zsh
echo "⚠️  Migration: Some files could not be cleaned" >&2
```

### 5. Safe Operations

- Use `sed_inplace` for file modifications
- Create backups if needed (though migrations should be safe)
- Use `|| true` for operations that might fail but shouldn't block

## Testing Checklist

Before committing a migration:

- [ ] Migration function is idempotent
- [ ] Prerequisites are checked
- [ ] Error handling is appropriate
- [ ] User feedback is clear
- [ ] Migration is added to registry
- [ ] Version in registry matches target version
- [ ] Tested with wrong state (problem exists)
- [ ] Tested with correct state (problem doesn't exist)
- [ ] Tested idempotency (runs twice without issues)
- [ ] Tested version comparison (runs at correct version)

## Common Pitfalls

### 1. Forgetting Idempotency Check

**Bad:**
```zsh
migrate_example() {
    # No check for .migrated file
    # ... migration logic ...
}
```

**Good:**
```zsh
migrate_example() {
    local migration_file="${migrations_dir}/v1.4.0_example.migrated"
    if [[ -f "$migration_file" ]]; then
        return 0
    fi
    # ... migration logic ...
}
```

### 2. Wrong Version in Registry

**Bad:**
```zsh
"1.3.4|example|Description|migrate_example"  # Current version - will run immediately
```

**Good:**
```zsh
"1.3.5|example|Description|migrate_example"  # Future version - runs when released
```

### 3. Not Checking Prerequisites

**Bad:**
```zsh
migrate_example() {
    # Directly modifies file without checking it exists
    sed_inplace "s/old/new/" "$TODO_FILE"
}
```

**Good:**
```zsh
migrate_example() {
    if [[ ! -f "$TODO_FILE" ]]; then
        return 1
    fi
    sed_inplace "s/old/new/" "$TODO_FILE"
}
```

## Integration with Release Process

When adding a migration for a release:

1. Create the migration function
2. Add to migration registry with the **release version**
3. Test thoroughly
4. Document in release notes if migration is user-visible

Example release notes:

```markdown
## Migration Notes

This release includes automatic migrations:

- **Section Order Fix (v1.3.5):** Automatically reorders TODO.md sections to correct order
```

## References

- **Design Document:** `docs/MIGRATION_SYSTEM_DESIGN.md`
- **Release Process:** `release/RELEASE_PROCESS.md`
- **Task #37:** Build release migration and cleanup system

