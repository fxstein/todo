import subprocess
from typing import Optional
from todo_ai.core.config import Config
from todo_ai.core.github_client import GitHubClient

class CoordinationManager:
    """Handles multi-user coordination modes and task ID generation."""
    
    def __init__(self, config: Config, github_client: Optional[GitHubClient] = None):
        self.config = config
        self.github_client = github_client or GitHubClient()

    def get_numbering_mode(self) -> str:
        return self.config.get_numbering_mode()

    def get_coordination_type(self) -> str:
        return self.config.get_coordination_type()

    def generate_next_task_id(self, current_max_serial: int) -> str:
        """
        Generate the next task ID based on the current mode.
        """
        mode = self.get_numbering_mode()
        
        if mode == "single-user":
            return self._generate_single_user_id(current_max_serial)
        elif mode == "multi-user":
            return self._generate_multi_user_id(current_max_serial)
        elif mode == "branch":
            return self._generate_branch_id(current_max_serial)
        elif mode == "enhanced":
            return self._generate_enhanced_id(current_max_serial)
        else:
            # Fallback
            return str(current_max_serial + 1)

    def _generate_single_user_id(self, current_max: int) -> str:
        """
        Mode 1: Single-user
        If coordination.type is 'github-issues', fetch next ID from issue comments.
        Otherwise, simple increment.
        """
        coord_type = self.get_coordination_type()
        
        if coord_type == "github-issues":
            issue_num = self.config.get("coordination.issue_number")
            if issue_num:
                return self._coordinate_via_github(current_max, issue_num)
                
        return str(current_max + 1)

    def _generate_multi_user_id(self, current_max: int) -> str:
        """
        Mode 2: Multi-user
        Prefix with GitHub user ID (first 7 chars).
        """
        user_id = self._get_github_user_id()
        # In multi-user mode, we typically want a unique serial per user or global?
        # The shell script uses: prefix + serial. 
        # But serial is global in .todo.ai.serial.
        # If multiple users edit same file, they share serial? 
        # Shell script implementation: 
        # assign_task_number_multi_user: gets user_id, increments serial, returns "{user_id}-{serial}"
        
        return f"{user_id}-{current_max + 1}"

    def _generate_branch_id(self, current_max: int) -> str:
        """
        Mode 3: Branch
        Prefix with branch name (first 7 chars).
        """
        branch = self._get_branch_name()
        return f"{branch}-{current_max + 1}"

    def _generate_enhanced_id(self, current_max: int) -> str:
        """
        Mode 4: Enhanced
        Same as single-user enhanced (uses coordination service).
        """
        # For now, behaves like single-user with coordination
        return self._generate_single_user_id(current_max)

    def _coordinate_via_github(self, current_max: int, issue_number: int) -> str:
        """
        Fetch latest task ID from GitHub Issue comments.
        Returns max(local, remote) + 1.
        """
        try:
            comments = self.github_client.get_issue_comments(issue_number)
            remote_max = 0
            
            # Simple parsing: look for digits in comments
            # Shell script looks for "Next task number: 123" or just digits
            for comment in reversed(comments):
                body = comment.get("body", "")
                # Try to find numbers
                # This is a simplified logic compared to shell script's regex
                # Ideally we'd use a regex to find "Next task number: (\d+)"
                import re
                match = re.search(r'Next task number: (\d+)', body)
                if match:
                    remote_max = int(match.group(1))
                    break
                    
            next_val = max(current_max, remote_max) + 1
            return str(next_val)
            
        except Exception as e:
            print(f"Warning: GitHub coordination failed: {e}")
            return str(current_max + 1)

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
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
            clean = "".join(c for c in branch if c.isalnum() or c == '_').lower()
            return clean[:7] or "main"
        except subprocess.CalledProcessError:
            return "main"

