import subprocess
from typing import Optional, List

def get_git_root() -> Optional[str]:
    """Get the root directory of the git repository."""
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
        return root
    except subprocess.CalledProcessError:
        return None

def get_current_branch() -> str:
    """Get current git branch name."""
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        return branch
    except subprocess.CalledProcessError:
        return "main"

def get_user_name() -> str:
    """Get git user name."""
    try:
        name = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
        return name
    except subprocess.CalledProcessError:
        return "user"

def get_user_email() -> str:
    """Get git user email."""
    try:
        email = subprocess.check_output(["git", "config", "user.email"], text=True).strip()
        return email
    except subprocess.CalledProcessError:
        return ""

def is_git_repo() -> bool:
    """Check if current directory is inside a git repository."""
    return get_git_root() is not None

