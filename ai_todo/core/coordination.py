import subprocess

from ai_todo.core.config import Config
from ai_todo.core.github_client import GitHubClient


class CoordinationManager:
    """Handles multi-user coordination modes and task ID generation."""

    def __init__(self, config: Config, github_client: GitHubClient | None = None):
        self.config = config
        self.github_client = github_client or GitHubClient()

    def get_numbering_mode(self) -> str:
        return self.config.get_numbering_mode()

    def get_coordination_type(self) -> str:
        return self.config.get_coordination_type()

    def generate_next_task_id(self, current_max_serial: int, stored_serial: int = 0) -> str:
        """
        Generate the next task ID based on the current mode.
        """
        mode = self.get_numbering_mode()

        if mode == "single-user":
            return self._generate_single_user_id(current_max_serial, stored_serial)
        elif mode == "multi-user":
            return self._generate_multi_user_id(current_max_serial, stored_serial)
        elif mode == "branch":
            return self._generate_branch_id(current_max_serial, stored_serial)
        elif mode == "enhanced":
            return self._generate_enhanced_id(current_max_serial, stored_serial)
        else:
            # Fallback
            return str(max(stored_serial, current_max_serial) + 1)

    def _generate_single_user_id(self, current_max: int, stored: int) -> str:
        """
        Mode 1: Single-user
        If coordination.type is 'github-issues', fetch next ID from issue comments.
        Otherwise, use max(stored, current_max + 1).
        """
        coord_type = self.get_coordination_type()

        if coord_type == "github-issues":
            issue_num = self.config.get("coordination.issue_number")
            if issue_num:
                return self._coordinate_via_github(current_max, issue_num)

        # Use max of stored (last used) and current_max, then increment
        return str(max(stored, current_max) + 1)

    def _generate_multi_user_id(self, current_max: int, stored: int) -> str:
        """
        Mode 2: Multi-user
        Prefix with GitHub user ID (first 7 chars).
        """
        user_id = self._get_github_user_id()
        next_val = max(stored, current_max) + 1
        return f"{user_id}-{next_val}"

    def _generate_branch_id(self, current_max: int, stored: int) -> str:
        """
        Mode 3: Branch
        Prefix with branch name (first 7 chars).
        """
        branch = self._get_branch_name()
        next_val = max(stored, current_max) + 1
        return f"{branch}-{next_val}"

    def _generate_enhanced_id(self, current_max: int, stored: int) -> str:
        """
        Mode 4: Enhanced
        Same as single-user enhanced (uses coordination service).
        """
        # For now, behaves like single-user with coordination
        return self._generate_single_user_id(current_max, stored)

    def _coordinate_via_github(self, current_max: int, issue_number: int) -> str:
        """
        Fetch latest task ID from GitHub Issue comments and reserve the next one.
        Returns max(local, remote) + 1 and posts the reservation to GitHub.
        """
        import re

        try:
            comments = self.github_client.get_issue_comments(issue_number)
            remote_max = 0

            # Parse comments to find the latest task number
            # Format: "Next task number: 123"
            for comment in reversed(comments):
                body = comment.get("body", "")
                match = re.search(r"Next task number: (\d+)", body)
                if match:
                    remote_max = int(match.group(1))
                    break

            next_val = max(current_max, remote_max) + 1

            # Post the new task number to GitHub for coordination
            self._post_task_number_to_github(next_val, issue_number)

            return str(next_val)

        except Exception as e:
            print(f"Warning: GitHub coordination failed: {e}")
            return str(current_max + 1)

    def _post_task_number_to_github(self, task_number: int, issue_number: int) -> None:
        """Post the reserved task number to the GitHub coordination issue."""
        try:
            body = f"Next task number: {task_number}"
            self.github_client.create_issue_comment(issue_number, body)
        except Exception as e:
            # Don't fail task creation if posting fails - just warn
            print(f"Warning: Failed to post task number to GitHub Issue #{issue_number}: {e}")

    def _get_github_user_id(self) -> str:
        """Get first 7 chars of GitHub username."""
        # Try gh cli via subprocess directly if client doesn't expose it
        # Or use git config user.name
        try:
            # Try git config
            name = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
            # Normalize: lower, alphanumeric, 7 chars
            clean = "".join(c for c in name if c.isalnum()).lower()
            return clean[:7] or "user"
        except subprocess.CalledProcessError:
            return "user"

    def _get_branch_name(self) -> str:
        """Get first 7 chars of current branch."""
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
            ).strip()
            clean = "".join(c for c in branch if c.isalnum() or c == "_").lower()
            return clean[:7] or "main"
        except subprocess.CalledProcessError:
            return "main"

    def get_next_task_id(self, task_manager, file_ops=None) -> str:
        """
        Get next task ID for a new task.
        Wrapper around generate_next_task_id that extracts current_max and stored_serial from TaskManager.
        """  # Get current max task ID from manager
        tasks = task_manager.list_tasks()
        current_max = 0
        for task in tasks:
            # Extract numeric part from task ID
            task_id = task.id
            # Remove prefix if present (e.g., "fxstein-50" -> "50")
            if "-" in task_id:
                task_id = task_id.split("-")[-1]
            # Extract base number (e.g., "50.1" -> "50")
            if "." in task_id:
                task_id = task_id.split(".")[0]
            try:
                num = int(task_id)
                if num > current_max:
                    current_max = num
            except ValueError:
                pass

        # Get stored serial from file
        if file_ops is None:
            # Try to get from task_manager if it has file_ops reference
            # Otherwise default to current_max
            stored_serial = current_max
        else:
            stored_serial = file_ops.get_serial()

        return self.generate_next_task_id(current_max, stored_serial)

    def get_next_subtask_id(self, parent_id: str, task_manager) -> str:
        """
        Get next subtask ID for a parent task.
        """
        # Get all subtasks of this parent
        subtasks = task_manager.get_subtasks(parent_id)
        current_max = 0

        for subtask in subtasks:
            # Extract subtask number (e.g., "50.3" -> 3, "fxstein-50.3" -> 3)
            subtask_id = subtask.id
            # Remove prefix if present
            if "-" in subtask_id:
                subtask_id = subtask_id.split("-", 1)[1]
            # Extract subtask number
            if "." in subtask_id:
                subtask_num_str = subtask_id.split(".")[-1]
                try:
                    num = int(subtask_num_str)
                    if num > current_max:
                        current_max = num
                except ValueError:
                    pass

        # Next subtask number
        next_num = current_max + 1

        # Generate parent's prefix if needed (for multi-user, branch modes)
        mode = self.get_numbering_mode()
        if mode == "multi-user":
            user_id = self._get_github_user_id()
            # Parent ID might already have prefix, extract base number
            base_parent = parent_id.split("-")[-1] if "-" in parent_id else parent_id
            return f"{user_id}-{base_parent}.{next_num}"
        elif mode == "branch":
            branch = self._get_branch_name()
            # Parent ID might already have prefix, extract base number
            base_parent = parent_id.split("-")[-1] if "-" in parent_id else parent_id
            return f"{branch}-{base_parent}.{next_num}"
        else:
            # Single-user or enhanced - just use parent_id.next_num
            # Parent ID might have prefix, extract base number
            base_parent = parent_id.split("-")[-1] if "-" in parent_id else parent_id
            return f"{base_parent}.{next_num}"
