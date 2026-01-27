import os
import shutil
import subprocess
from typing import Any

import requests


class GitHubClient:
    """GitHub API client for issue management and bug reporting."""

    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.api_base = "https://api.github.com"

    def _get_headers(self) -> dict[str, str]:
        if not self.token:
            # Try to get token from gh cli if available
            if shutil.which("gh"):
                try:
                    token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
                    self.token = token
                except subprocess.CalledProcessError:
                    pass

        if not self.token:
            raise ValueError(
                "GitHub token required. Set GITHUB_TOKEN env var or login with 'gh auth login'."
            )

        return {"Authorization": f"token {self.token}", "Accept": "application/vnd.github.v3+json"}

    def _get_repo_info(self) -> tuple[str, str]:
        """Get owner/repo from git config."""
        try:
            url = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], text=True
            ).strip()
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
        except subprocess.CalledProcessError as err:
            raise ValueError("Not a git repository or no remote origin") from err

    def create_issue(
        self, title: str, body: str, labels: list[str] | None = None
    ) -> dict[str, Any]:
        """Create a new issue."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues"

        data = {"title": title, "body": body, "labels": labels or []}

        response = requests.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    def get_issue(self, issue_number: int) -> dict[str, Any]:
        """Get issue details."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues/{issue_number}"

        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    def get_issue_comments(self, issue_number: int) -> list[dict[str, Any]]:
        """Get comments for an issue."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues/{issue_number}/comments"

        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        result: list[dict[str, Any]] = response.json()
        return result

    def list_issues(
        self, labels: list[str] | None = None, state: str = "open"
    ) -> list[dict[str, Any]]:
        """List issues."""
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues"

        params = {"state": state}
        if labels:
            params["labels"] = ",".join(labels)

        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        result: list[dict[str, Any]] = response.json()
        return result

    def create_issue_comment(self, issue_number: int, body: str) -> dict[str, Any]:
        """Create a comment on an issue.

        Used for task number coordination - posts the next task number
        to the coordination issue for atomic multi-user synchronization.
        """
        owner, repo = self._get_repo_info()
        url = f"{self.api_base}/repos/{owner}/{repo}/issues/{issue_number}/comments"

        data = {"body": body}

        response = requests.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result
