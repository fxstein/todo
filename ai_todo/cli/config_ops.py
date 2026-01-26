"""Configuration and setup commands for ai-todo."""

import shutil
import subprocess
import urllib.request
from pathlib import Path

from ai_todo.core.config import Config


def _get_config_dir(todo_path: str) -> Path:
    """Get the config directory, preferring new name but falling back to legacy."""
    new_dir = Path(todo_path).parent / ".ai-todo"
    old_dir = Path(todo_path).parent / ".todo.ai"
    return new_dir if new_dir.exists() else (old_dir if old_dir.exists() else new_dir)


def show_config_command(todo_path: str = "TODO.md") -> None:
    """Show current configuration."""
    config_dir = _get_config_dir(todo_path)
    config_path = config_dir / "config.yaml"

    if not config_path.exists():
        print("No configuration file found.")
        print("Using default mode: single-user")
        print("")
        print("To create a config file, use: ai-todo switch-mode <mode>")
        return

    print("Current Configuration:")
    print("======================")
    print(config_path.read_text(encoding="utf-8"))
    print("")
    print(f"Config file location: {config_path}")


def detect_coordination_command(todo_path: str = "TODO.md") -> None:
    """Detect available coordination options based on system."""
    print("🔍 Detecting available coordination options...")
    print("")

    available_options = []
    missing_requirements = []

    # Check for GitHub Issues coordination
    print("Checking GitHub Issues coordination...")
    gh_available = False
    gh_auth = False
    git_repo = False

    if shutil.which("gh"):
        gh_available = True
        print("  ✅ GitHub CLI (gh) installed")

        # Check authentication
        try:
            result = subprocess.run(
                ["gh", "auth", "status"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                gh_auth = True
                print("  ✅ GitHub CLI authenticated")
            else:
                print("  ⚠️  GitHub CLI not authenticated (run: gh auth login)")
                missing_requirements.append("GitHub CLI authentication")
        except Exception:
            print("  ⚠️  GitHub CLI not authenticated (run: gh auth login)")
            missing_requirements.append("GitHub CLI authentication")
    else:
        print("  ❌ GitHub CLI (gh) not installed")
        missing_requirements.append("GitHub CLI (gh)")

    # Check if we're in a git repository
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            # Check for GitHub remote
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            repo_url = result.stdout.strip() if result.returncode == 0 else ""
            if repo_url and "github.com" in repo_url:
                git_repo = True
                print("  ✅ Git repository with GitHub remote detected")
            else:
                print("  ⚠️  Git repository not connected to GitHub")
                missing_requirements.append("GitHub repository connection")
        else:
            print("  ⚠️  Not in a Git repository")
            missing_requirements.append("Git repository")
    except Exception:
        print("  ⚠️  Not in a Git repository")
        missing_requirements.append("Git repository")

    if gh_available and gh_auth and git_repo:
        available_options.append("github-issues")
        print("  ✅ GitHub Issues coordination: AVAILABLE")
    else:
        print("  ❌ GitHub Issues coordination: NOT AVAILABLE")

    print("")

    # Check for CounterAPI coordination
    print("Checking CounterAPI coordination...")
    try:
        # Try to access CounterAPI
        urllib.request.urlopen("https://api.countapi.xyz", timeout=2)
        available_options.append("counterapi")
        print("  ✅ CounterAPI coordination: AVAILABLE")
    except Exception:
        print("  ❌ CounterAPI coordination: NOT AVAILABLE (network issue)")

    print("")

    if available_options:
        print("✅ Available coordination options:")
        for option in available_options:
            print(f"  - {option}")
    else:
        print("❌ No coordination options available")
        if missing_requirements:
            print("")
            print("Missing requirements:")
            for req in missing_requirements:
                print(f"  - {req}")


def setup_coordination_command(
    coord_type: str, interactive: bool = True, todo_path: str = "TODO.md"
) -> None:
    """Set up coordination service (github-issues, counterapi)."""
    if not coord_type:
        print("Error: Please specify coordination type")
        print("Usage: ./todo.ai setup-coordination <type>")
        print("Types: github-issues, counterapi")
        return

    config_dir = _get_config_dir(todo_path)
    config_path = config_dir / "config.yaml"
    config = Config(str(config_path))

    # Ensure config file exists
    current_mode = config.get_numbering_mode()
    if not config_path.exists():
        config.set("mode", current_mode)
        config.set("coordination.type", "none")
        config.set("coordination.fallback", "multi-user")

    if coord_type == "github-issues":
        _setup_github_issues_coordination(config, interactive, todo_path)
    elif coord_type == "counterapi":
        _setup_counterapi_coordination(config, interactive)
    else:
        print(f"Error: Unknown coordination type '{coord_type}'")
        print("Valid types: github-issues, counterapi")
        return


def _setup_github_issues_coordination(config: Config, interactive: bool, todo_path: str) -> None:
    """Set up GitHub Issues coordination."""
    if not shutil.which("gh"):
        print("Error: GitHub CLI (gh) is required for GitHub Issues coordination")
        print("Install: https://cli.github.com/")
        return

    # Check authentication
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("Error: GitHub CLI not authenticated")
            print("Run: gh auth login")
            return
    except Exception:
        print("Error: Cannot check GitHub CLI authentication")
        return

    # Get repository info
    try:
        from ai_todo.core.github_client import GitHubClient

        github_client = GitHubClient()
        owner, repo = github_client._get_repo_info()

        if interactive:
            print(f"Repository: {owner}/{repo}")
            print("")
            print("Enter the issue number to use for coordination:")
            print("(This should be an existing GitHub issue in the repository)")
            issue_num_str = input("Issue number: ").strip()

            try:
                issue_number = int(issue_num_str)
            except ValueError:
                print("Error: Invalid issue number")
                return

            # Verify issue exists
            issue = github_client.get_issue(issue_number)
            if not issue:
                print(f"Error: Issue #{issue_number} not found")
                return

            print(f"✅ Found issue: {issue.get('title', 'Untitled')}")
        else:
            # Non-interactive mode - would need issue number as parameter
            print("Error: Non-interactive mode requires issue number parameter")
            return

        # Save configuration
        config.set("coordination.type", "github-issues")
        config.set("coordination.issue_number", issue_number)
        config.set("coordination.fallback", "multi-user")

        print("")
        print("✅ GitHub Issues coordination configured successfully!")
    except Exception as e:
        print(f"Error: Failed to setup GitHub Issues coordination: {e}")


def _setup_counterapi_coordination(config: Config, interactive: bool) -> None:
    """Set up CounterAPI coordination."""
    if interactive:
        print("CounterAPI coordination uses a public API service.")
        print("No configuration needed - it works automatically.")
        print("")
        print("Continue? (y/N)")
        reply = input().strip()
        if reply.lower() != "y":
            print("Setup cancelled")
            return

    config.set("coordination.type", "counterapi")
    config.set("coordination.fallback", "multi-user")

    print("")
    print("✅ CounterAPI coordination configured successfully!")


def setup_wizard_command(todo_path: str = "TODO.md") -> None:
    """Interactive setup wizard for mode and coordination."""
    print("🚀 todo.ai Setup Wizard")
    print("========================")
    print("")
    print("This wizard will guide you through configuring todo.ai for your needs.")
    print("")

    # Step 1: Detect current system capabilities
    print("Step 1: Detecting system capabilities...")
    print("")
    detect_coordination_command(todo_path)
    print("")

    # Step 2: Select mode
    print("Step 2: Select numbering mode")
    print("")
    print("Available modes:")
    print("  1) single-user  - Simple sequential numbering (#1, #2, #3...)")
    print("  2) multi-user   - Prefix with GitHub user ID (fxstein-50, alice-50...)")
    print("  3) branch       - Prefix with branch name (feature-50, main-50...)")
    print("  4) enhanced     - Multi-user with atomic coordination (requires setup)")
    print("")
    mode_choice = input("Enter mode [1]: ").strip() or "1"

    mode_map = {
        "1": "single-user",
        "2": "multi-user",
        "3": "branch",
        "4": "enhanced",
    }

    selected_mode = mode_map.get(mode_choice)
    if not selected_mode:
        print("❌ Invalid choice")
        return

    print("")
    print(f"✅ Selected mode: {selected_mode}")
    print("")

    # Step 3: Switch to selected mode
    print(f"Step 3: Switching to {selected_mode} mode...")
    switch_mode_command(selected_mode, force=True, todo_path=todo_path)
    print("")

    # Step 4: Setup coordination (if needed)
    if selected_mode in ["multi-user", "enhanced"]:
        print("Step 4: Setup coordination (optional)")
        print("")
        print("Coordination helps prevent task ID conflicts in multi-user environments.")
        print("Skip coordination? (y/N)")
        skip = input().strip().lower() == "y"

        if not skip:
            detect_coordination_command(todo_path)
            print("")
            print("Select coordination type:")
            print("  1) github-issues  - Use GitHub Issues for coordination")
            print("  2) counterapi      - Use CounterAPI service")
            print("  3) none            - Skip coordination setup")
            print("")
            coord_choice = input("Enter choice [3]: ").strip() or "3"

            if coord_choice == "1":
                setup_coordination_command("github-issues", interactive=True, todo_path=todo_path)
            elif coord_choice == "2":
                setup_coordination_command("counterapi", interactive=True, todo_path=todo_path)

    print("")
    print("✅ Setup complete!")


def switch_mode_command(
    new_mode: str,
    force: bool = False,
    renumber: bool = False,
    todo_path: str = "TODO.md",
) -> None:
    """Switch numbering mode (single-user, multi-user, branch, enhanced) with --force and --renumber options."""
    valid_modes = ["single-user", "multi-user", "branch", "enhanced"]
    if new_mode not in valid_modes:
        print(f"Error: Invalid mode '{new_mode}'")
        print(f"Valid modes: {', '.join(valid_modes)}")
        return

    config_dir = _get_config_dir(todo_path)
    config_path = config_dir / "config.yaml"
    config = Config(str(config_path))

    current_mode = config.get_numbering_mode()

    # Check if already in requested mode
    if current_mode == new_mode:
        print(f"Already in {new_mode} mode")
        return

    # Create backup before mode switch
    backup_name = create_mode_backup(todo_path)
    if backup_name:
        print(f"💾 Backup created: {backup_name}")
        print("")

    # Switch mode
    config.set("mode", new_mode)

    print(f"✅ Switched to {new_mode} mode")

    if renumber:
        print("")
        print("⚠️  Renumbering existing tasks is not yet implemented in Python version")
        print("   Tasks will keep their current IDs")


def list_mode_backups_command(todo_path: str = "TODO.md") -> None:
    """List mode switch backups."""
    config_dir = _get_config_dir(todo_path)
    backups_dir = config_dir / "backups"

    if not backups_dir.exists():
        print("No mode switch backups found")
        return

    backups = sorted(
        backups_dir.glob("mode-switch-*.TODO.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not backups:
        print("No mode switch backups found")
        return

    print("Mode switch backups:")
    print("")

    for backup in backups:
        backup_name = backup.name.replace(".TODO.md", "")
        timestamp = backup_name.replace("mode-switch-", "")
        # Format timestamp: YYYYMMDDHHMMSS -> YYYY-MM-DD HH:MM:SS
        if len(timestamp) == 14:
            date_str = f"{timestamp[0:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[8:10]}:{timestamp[10:12]}:{timestamp[12:14]}"
        else:
            date_str = timestamp
        print(f"  {backup_name} ({date_str})")


def rollback_mode_command(backup_name: str, todo_path: str = "TODO.md") -> None:
    """Rollback from mode switch backup."""
    if not backup_name:
        print("Error: Please provide backup name")
        print("Usage: ai-todo rollback-mode <backup-name>")
        print("List backups: ai-todo list-mode-backups")
        return

    config_dir = _get_config_dir(todo_path)
    backups_dir = config_dir / "backups"

    backup_todo = backups_dir / f"{backup_name}.TODO.md"
    backup_config = backups_dir / f"{backup_name}.config.yaml"
    backup_serial = backups_dir / f"{backup_name}.serial"

    if not backup_todo.exists():
        print(f"Error: Backup '{backup_name}' not found")
        return

    # Restore files
    todo_file = Path(todo_path)
    if backup_todo.exists():
        shutil.copy2(backup_todo, todo_file)

    config_path = config_dir / "config.yaml"
    if backup_config.exists():
        shutil.copy2(backup_config, config_path)
    elif config_path.exists():
        # If backup has no config but current has one, remove it
        config_path.unlink()

    serial_path = config_dir / ".ai-todo.serial"
    if not serial_path.exists():
        serial_path = config_dir / ".todo.ai.serial"
    if backup_serial.exists():
        shutil.copy2(backup_serial, serial_path)

    print(f"✅ Rollback complete: restored from backup '{backup_name}'")


def create_mode_backup(todo_path: str = "TODO.md") -> str | None:
    """Create backup before mode switches."""
    from datetime import datetime

    config_dir = _get_config_dir(todo_path)
    backups_dir = config_dir / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_name = f"mode-switch-{timestamp}"

    # Backup TODO.md
    todo_file = Path(todo_path)
    if todo_file.exists():
        backup_todo = backups_dir / f"{backup_name}.TODO.md"
        shutil.copy2(todo_file, backup_todo)

    # Backup config.yaml
    config_path = config_dir / "config.yaml"
    if config_path.exists():
        backup_config = backups_dir / f"{backup_name}.config.yaml"
        shutil.copy2(config_path, backup_config)

    # Backup serial file
    serial_path = config_dir / ".ai-todo.serial"
    if not serial_path.exists():
        serial_path = config_dir / ".todo.ai.serial"
    if serial_path.exists():
        backup_serial = backups_dir / f"{backup_name}.serial"
        shutil.copy2(serial_path, backup_serial)

    return backup_name
