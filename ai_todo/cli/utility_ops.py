"""Utility commands for todo.ai."""

import os
import shutil
import subprocess
from pathlib import Path

from ai_todo import __version__


def version_command() -> None:
    """Show version information."""
    print(f"ai-todo version {__version__}")
    print("Repository: https://github.com/fxstein/ai-todo")
    print("Update: pip install --upgrade ai-todo")


def uninstall_command(
    remove_data: bool = False,
    remove_rules: bool = False,
    force: bool = False,
) -> None:
    """Uninstall todo.ai (with --remove-data, --remove-rules, --all options)."""
    # For Python package installations, uninstall is handled by pip
    # This command is mainly for shell script installations
    print("")
    print("🗑️  Uninstalling todo.ai")
    print("")
    print("For Python package installations, use:")
    print("  pip uninstall ai-todo")
    print("  # or")
    print("  uv pip uninstall ai-todo")
    print("")
    print("For shell script installations:")
    print("  - Script location: Check your PATH or installation directory")
    print("  - Data directory: .ai-todo/ (in current working directory)")
    print("  - Cursor rules: .cursor/rules/ai-todo-*.mdc")
    print("")

    # Check for .ai-todo directory in current working directory
    # Also check legacy .todo.ai for backward compatibility
    ai_todo_dir = Path.cwd() / ".ai-todo"
    legacy_dir = Path.cwd() / ".todo.ai"
    todo_ai_dir = ai_todo_dir if ai_todo_dir.exists() else legacy_dir
    has_data_dir = todo_ai_dir.exists()

    # Check for Cursor rules
    rules_dir = Path.cwd() / ".cursor" / "rules"
    todo_ai_rules = []
    if rules_dir.exists():
        todo_ai_rules = list(rules_dir.glob("todo.ai-*.mdc"))

    # Build what will be removed list
    print("The following will be removed:")

    will_remove_data = False
    will_remove_rules = False

    if remove_data and has_data_dir:
        print(f"  ✗ Data directory: {todo_ai_dir}")
        will_remove_data = True
        print("     ⚠️  Warning: This will remove your TODO data (.ai-todo/ directory)")
        print("     ⚠️  Your TODO.md file will remain untouched")
    elif has_data_dir:
        print(f"  ✓ Data directory: {todo_ai_dir} (preserved - use --remove-data to remove)")

    if remove_rules and todo_ai_rules:
        print("  ✗ Cursor rules:")
        for rule_file in todo_ai_rules:
            print(f"      - {rule_file.name}")
        will_remove_rules = True
    elif todo_ai_rules:
        print(
            f"  ✓ Cursor rules: {len(todo_ai_rules)} file(s) (preserved - use --remove-rules to remove)"
        )

    # Safety check
    if not will_remove_data and not will_remove_rules:
        print("")
        print("✅ Nothing to remove in current directory.")
        print("   Use --remove-data to remove .ai-todo/ directory")
        print("   Use --remove-rules to remove Cursor rules")
        return

    print("")

    # Confirmation (unless --force)
    if not force:
        reply = input("Proceed with uninstall? (y/N) ").strip()
        if reply.lower() != "y":
            print("Uninstall cancelled")
            return

    # Remove data directory
    if will_remove_data:
        try:
            shutil.rmtree(todo_ai_dir)
            print(f"✅ Removed data directory: {todo_ai_dir}")
        except Exception as e:
            print(f"⚠️  Error: Could not remove data directory: {e}")
            print("   You may need to remove it manually")

    # Remove Cursor rules
    if will_remove_rules:
        rules_removed = 0
        for rule_file in todo_ai_rules:
            try:
                rule_file.unlink()
                rules_removed += 1
            except Exception:
                pass

        if rules_removed > 0:
            print(f"✅ Removed {rules_removed} Cursor rule(s)")
        else:
            print("⚠️  Error: Could not remove Cursor rules")
            print(f"   You may need to remove them manually from {rules_dir}")

    print("")
    print("✅ Uninstall complete!")


def report_bug_command(
    error_description: str,
    error_context: str | None = None,
    command: str | None = None,
) -> None:
    """Report bugs to GitHub Issues (with duplicate detection)."""
    if not error_description:
        print("Error: Please provide an error description")
        print('Usage: todo.ai report-bug "Error description" [error context] [command]')
        return

    # Check if GitHub CLI is available
    if not shutil.which("gh"):
        print("Error: GitHub CLI (gh) is required for bug reporting")
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
        repo_url = f"{owner}/{repo}"
    except Exception as e:
        print(f"Error: Cannot determine GitHub repository: {e}")
        return

    # Generate bug report
    bug_report = _generate_bug_report(error_description, error_context, command)

    # Categorize error and get suggested labels
    labels = _categorize_error(error_description, error_context)

    # Extract title from error message
    title = f"[Bug]: {error_description[:90]}"

    # Detect if running in AI agent context
    is_ai_agent = bool(
        os.environ.get("CURSOR_AI")
        or os.environ.get("AI_AGENT")
        or os.environ.get("GITHUB_ACTIONS")
    )

    # Show error and preview
    print("")
    print(f"⚠️  An error occurred: {error_description}")
    print("")

    if is_ai_agent:
        print("🤖 AI Agent detected - Bug report will be submitted automatically")
        print("")
        print("Preview of bug report:")
        print("---")
        # Show condensed preview for agents
        preview_lines = bug_report.split("\n")[:30]
        print("\n".join(preview_lines))
        print("...")
        print("---")
        print("")
        print(f"📋 Suggested labels: {labels}")
        print("")
        print("⏳ Auto-submitting in 2 seconds...")
        import time

        time.sleep(2)
        print("✓ Proceeding with bug report submission")

        # Proceed automatically
        _handle_duplicate_detection(title, bug_report, repo_url, labels)
    else:
        # Human user - show full preview and ask for confirmation
        print("Would you like to report this bug to GitHub Issues?")
        print("")
        print("Preview of bug report:")
        print("---")
        # Show header sections
        preview_lines = bug_report.split("\n")[:40]
        print("\n".join(preview_lines))
        print("")
        print("... (additional context sections collapsed) ...")
        print("")
        print("---")
        print("")
        print(f"📋 Suggested labels: {labels}")
        print("")

        # Always require confirmation for humans
        reply = input("Report this bug? (y/N) ").strip()
        if reply.lower() != "y":
            print("Bug report cancelled by user")
            return

        # User confirmed - proceed with duplicate check and reporting
        _handle_duplicate_detection(title, bug_report, repo_url, labels)


def _generate_bug_report(error_message: str, error_context: str | None, command: str | None) -> str:
    """Generate bug report with context."""
    import platform
    from datetime import datetime

    # Collect environment info
    os_info = f"{platform.system()} {platform.release()}"
    shell_info = os.environ.get("SHELL", "unknown")
    version_info = f"todo.ai {__version__}"

    # Get shell version
    shell_version = "unknown"
    try:
        if "zsh" in shell_info:
            result = subprocess.run(["zsh", "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                shell_version = result.stdout.strip().split()[-1]
        elif "bash" in shell_info:
            result = subprocess.run(
                ["bash", "--version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                shell_version = (
                    result.stdout.strip().split()[3]
                    if len(result.stdout.strip().split()) > 3
                    else "unknown"
                )
    except Exception:
        pass

    # Collect git info
    git_info = "Not in a git repository"
    repo_info = ""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            branch = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()
            git_info = f"Branch: {branch}"

            # Get git status
            status = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()
            if status:
                git_info += f"\nStatus:\n{status}"

            # Get repo URL
            repo_url = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()
            if repo_url:
                # Convert SSH to HTTPS if needed
                if repo_url.startswith("git@"):
                    repo_url = repo_url.replace("git@github.com:", "https://github.com/")
                if repo_url.endswith(".git"):
                    repo_url = repo_url[:-4]
                repo_info = f"Git Repository: {repo_url}"
    except Exception:
        pass

    # Collect TODO.md state
    todo_info = "TODO.md not found"
    todo_path = Path("TODO.md")
    if todo_path.exists():
        try:
            content = todo_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            task_count = sum(1 for line in lines if "**#" in line and "[ ]" in line)
            completed_count = sum(1 for line in lines if "**#" in line and "[x]" in line)
            todo_info = f"Tasks: {task_count} pending, {completed_count} completed"
        except Exception:
            todo_info = "Could not read TODO.md"

    # Collect environment variables (filtered)
    env_vars = []
    for key in ["PATH", "SHELL", "HOME", "USER", "EDITOR"]:
        if key in os.environ:
            env_vars.append(f"{key}={os.environ[key]}")
    env_info = "\n".join(env_vars) if env_vars else "No relevant environment variables"

    # Collect recent logs
    log_info = ""
    # Check new location first, then legacy
    log_path = Path(".ai-todo") / ".ai-todo.log"
    if not log_path.exists():
        log_path = Path(".todo.ai") / ".todo.ai.log"
    if log_path.exists():
        try:
            content = log_path.read_text(encoding="utf-8")
            log_lines = [
                line for line in content.splitlines() if line.strip() and not line.startswith("#")
            ]
            log_info = "\n".join(log_lines[:50])  # Last 50 lines
        except Exception:
            log_info = "Could not read log file"

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build bug report with GitHub callout blocks
    report = f"""## 🐛 Bug Report

> [!WARNING]
> **Error Occurred**: {current_date}

---

### Error Description

```text
{error_message}
```

### Command Executed

```bash
todo.ai {command or "unknown"}
```

### Error Context

```text
{error_context or "No additional context provided"}
```

---

### System Information

> [!NOTE]
> Environment details collected automatically

| Component | Details |
|-----------|---------|
| **OS** | {os_info} |
| **Shell** | {shell_version} |
| **Version** | {version_info} |"""

    if repo_info:
        report += f"\n| **Repository** | {repo_info} |"

    report += f"""

---

<details>
<summary><strong>📊 Additional Context</strong></summary>

#### Git Status
```
{git_info}
```

#### TODO.md State
```
{todo_info}
```

#### Environment Variables
```
{env_info}
```

</details>

---

<details>
<summary><strong>📋 Recent Logs</strong> (last 50 lines)</summary>

```
{log_info or "No logs available"}
```

</details>

---

### Additional Information

*Add any other relevant details here*

---

<sub>🤖 Reported automatically by todo.ai v{__version__}</sub>
"""

    return report


def _categorize_error(error_message: str, error_context: str | None) -> str:
    """Categorize error and suggest labels."""
    import platform

    error_lower = (error_message + " " + (error_context or "")).lower()
    labels = ["bug"]

    # Error type labels
    if any(
        word in error_lower for word in ["segfault", "segmentation fault", "core dump", "signal 11"]
    ):
        labels.append("crash")
    elif any(
        word in error_lower for word in ["timeout", "too slow", "performance", "taking too long"]
    ):
        labels.append("performance")
    elif any(
        word in error_lower
        for word in ["data loss", "file corrupt", "lost", "missing data", "cannot find"]
    ):
        labels.append("data-loss")
    elif any(
        word in error_lower
        for word in ["github", "api", "coordination", "gh cli", "issue.*not found"]
    ):
        labels.append("coordination")

    # OS-specific labels
    system = platform.system()
    if system == "Darwin":
        labels.append("macos")
    elif system == "Linux":
        # Check for WSL
        if os.path.exists("/proc/version"):
            try:
                with open("/proc/version") as f:
                    if "microsoft" in f.read().lower():
                        labels.append("wsl")
                    else:
                        labels.append("linux")
            except Exception:
                labels.append("linux")
        else:
            labels.append("linux")

    # Shell-specific labels
    shell = os.environ.get("SHELL", "").lower()
    if "zsh" in shell:
        labels.append("zsh")
    elif "bash" in shell:
        labels.append("bash")

    return ",".join(labels)


def _handle_duplicate_detection(title: str, body: str, repo_url: str, labels: str) -> None:
    """Handle duplicate detection and create issue or comment."""
    # Check for duplicates
    duplicates = _check_for_duplicate_issues(title, body, repo_url)

    if duplicates:
        print("")
        print("Similar issues found:")
        print("")

        # Display duplicates
        for idx, (issue_num, issue_title, similarity) in enumerate(duplicates, 1):
            print(f"{idx}) Issue #{issue_num}: {issue_title} (similarity: {similarity}%)")

        print("")
        reply = input(
            "Would you like to add a 'me too' comment to an existing issue? (y/N) "
        ).strip()

        if reply.lower() == "y":
            selected_num = input("Enter issue number to reply to: ").strip()
            if selected_num.isdigit():
                _reply_to_existing_issue(int(selected_num), body, repo_url)
                return
            else:
                print("Invalid issue number")
                return
        else:
            reply = input("Create a new issue instead? (y/N) ").strip()
            if reply.lower() != "y":
                print("Bug report cancelled")
                return

    # No duplicates or user wants new issue - create it
    _create_new_issue(title, body, repo_url, labels)


def _check_for_duplicate_issues(
    title: str, body: str, repo_url: str
) -> list[tuple[int, str, float]]:
    """Check for duplicate issues with similarity calculation."""
    BUG_REPORT_THRESHOLD = 50  # 50% similarity threshold

    try:
        # Use GitHub CLI to search for issues
        import re

        # Extract keywords from title
        keywords = re.findall(r"[a-z]+", title.lower())[:5]
        if not keywords:
            return []

        # Search for issues using gh CLI
        search_query = " ".join(keywords)
        result = subprocess.run(
            [
                "gh",
                "issue",
                "list",
                "--repo",
                repo_url,
                "--search",
                f"in:title {search_query}",
                "--limit",
                "10",
                "--json",
                "number,title",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return []

        import json

        issues = json.loads(result.stdout)
        duplicates = []

        for issue in issues:
            issue_num = issue.get("number", 0)
            issue_title = issue.get("title", "")

            # Normalize titles (strip "Bug: " prefix)
            normalized_issue_title = re.sub(r"^Bug:\s*", "", issue_title, flags=re.IGNORECASE)
            normalized_title = re.sub(r"^\[Bug\]:\s*", "", title, flags=re.IGNORECASE)

            # Calculate similarity
            similarity = _calculate_similarity(normalized_title, normalized_issue_title)

            if similarity >= BUG_REPORT_THRESHOLD:
                duplicates.append((issue_num, issue_title, round(similarity, 1)))

        # Sort by similarity (highest first)
        duplicates.sort(key=lambda x: x[2], reverse=True)
        return duplicates[:5]  # Return top 5 matches
    except Exception:
        return []


def _calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two strings (word-based Jaccard)."""
    import re

    # Extract words (lowercase, alphanumeric)
    words1 = set(re.findall(r"[a-z0-9]+", text1.lower()))
    words2 = set(re.findall(r"[a-z0-9]+", text2.lower()))

    if not words1 and not words2:
        return 0.0
    if not words1 or not words2:
        return 0.0

    # Calculate Jaccard similarity
    intersection = len(words1 & words2)
    union = len(words1 | words2)

    if union == 0:
        return 0.0

    return (intersection / union) * 100


def _create_new_issue(title: str, body: str, repo_url: str, labels: str) -> None:
    """Create new GitHub issue."""
    try:
        from ai_todo.core.github_client import GitHubClient

        github_client = GitHubClient()
        label_list = [label.strip() for label in labels.split(",") if label.strip()]
        if "auto-reported" not in label_list:
            label_list.append("auto-reported")

        issue = github_client.create_issue(title, body, label_list)
        print(f"✅ Bug report created successfully: {issue.get('html_url', '')}")
    except Exception as e:
        print(f"Error: Failed to create issue: {e}")


def _reply_to_existing_issue(issue_number: int, body: str, repo_url: str) -> None:
    """Add comment to existing issue."""
    try:
        # Use GitHub CLI to add comment
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
            f.write(body)
            temp_file = f.name

        try:
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "comment",
                    str(issue_number),
                    "--body-file",
                    temp_file,
                    "--repo",
                    repo_url,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                print(f"✅ Comment added to issue #{issue_number}")
            else:
                print(f"Error: Failed to add comment: {result.stderr}")
        finally:
            os.unlink(temp_file)
    except Exception as e:
        print(f"Error: Failed to add comment: {e}")
