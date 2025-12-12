import pytest
import yaml
from todo_ai.core.migrations import MigrationRegistry

@pytest.fixture
def migration_registry(tmp_path):
    config_dir = tmp_path / ".todo.ai"
    return MigrationRegistry(str(config_dir))

def test_registry_init(tmp_path):
    config_dir = tmp_path / ".todo.ai"
    registry = MigrationRegistry(str(config_dir))
    
    assert (config_dir / "migrations").exists()
    assert (config_dir / "migrations").is_dir()

def test_register_and_run(migration_registry):
    state = {"count": 0}
    
    def migration_001():
        state["count"] += 1
        
    migration_registry.register_migration("001_test", migration_001)
    
    executed = migration_registry.run_pending_migrations()
    
    assert "001_test" in executed
    assert state["count"] == 1
    assert "001_test" in migration_registry.get_applied_migrations()

def test_skip_applied(migration_registry):
    state = {"count": 0}
    def migration_001():
        state["count"] += 1
        
    migration_registry.register_migration("001_test", migration_001)
    
    # Run once
    migration_registry.run_pending_migrations()
    assert state["count"] == 1
    
    # Run again - should skip
    executed = migration_registry.run_pending_migrations()
    assert len(executed) == 0
    assert state["count"] == 1

def test_migration_error(migration_registry):
    def migration_fail():
        raise ValueError("Failed")
        
    migration_registry.register_migration("001_fail", migration_fail)
    
    with pytest.raises(ValueError):
        migration_registry.run_pending_migrations()
        
    # Should not be marked as applied
    assert "001_fail" not in migration_registry.get_applied_migrations()

