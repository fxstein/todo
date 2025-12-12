import os
import requests
import subprocess
import shutil
from typing import List, Dict, Optional, Any, Tuple

class GitHubClient:
    """GitHub API client for issue management and bug reporting."""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"
        
    def _get_headers(self) -> Dict[str, str]:
        if not self.token:
             # Try to get token from gh cli if available
            if shutil.which("gh"):
                 try:
                     token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
                     self.token = token
                 except subprocess.CalledProcessError:
                     pass
                     
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN env var or login with 'gh auth login'.")
            
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _get_repo_info(self) -> Tuple[str, str]:
        """Get owner/repo from git config."""
        try:
            url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True).strip()
            # Handle SSH and HTTPS urls
            # git@github.com:owner/repo.git -> owner/repo
            # https://github.com/owner/repo.git -> owner/repo
            
            if "github.com" not in url:
                raise ValueError("Not a GitHub repository")
                
            path = url.split("github.com")[-1].lstrip(":/")
            if path.endswith(".git"):
                path = path[:-4]
                
            parts = path.split("/")
            if len(parts) != 2:
                 raise ValueError(f"Could not parse repo owner/name from URL: {url}")
                 
            return parts[0], parts[1]
        except subprocess.CalledProcessError:
            raise ValueError("Not a git repository or no remote origin")

    def create_issue(self, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        """Create a new issue."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues"
        
        data = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        return response.json()

    def get_issue(self, issue_number: int) -> Dict[str, Any]:
        """Get issue details."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues/{issue_number}"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
        
    def get_issue_comments(self, issue_number: int) -> List[Dict[str, Any]]:
        """Get comments for an issue."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def list_issues(self, labels: List[str] = None, state: str = "open") -> List[Dict[str, Any]]:
        """List issues."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues"
        
        params = {"state": state}
        if labels:
            params["labels"] = ",".join(labels)
            
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

