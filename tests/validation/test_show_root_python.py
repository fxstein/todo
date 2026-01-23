from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from todo_ai.cli.main import cli

_IS_WINDOWS = os.name == "nt"


def _git(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(
        ["git", *cmd],
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


def _init_repo(repo_path: Path) -> None:
    repo_path.mkdir(parents=True, exist_ok=True)
    _git(["init"], repo_path)
    (repo_path / "README.md").write_text("test repo\n", encoding="utf-8")
    _git(["add", "README.md"], repo_path)
    _git(
        ["-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "init"],
        repo_path,
    )


@pytest.mark.skipif(_IS_WINDOWS, reason="Test relies on local git submodules")
def test_show_root_from_submodule(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    subrepo = tmp_path / "subrepo"
    superrepo = tmp_path / "superrepo"
    _init_repo(subrepo)
    _init_repo(superrepo)

    env = os.environ.copy()
    env["GIT_ALLOW_PROTOCOL"] = "file"
    _git(
        ["-c", "protocol.file.allow=always", "submodule", "add", str(subrepo), "submodule"],
        superrepo,
        env=env,
    )
    _git(["add", ".gitmodules", "submodule"], superrepo)
    _git(
        [
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-m",
            "add submodule",
        ],
        superrepo,
    )

    monkeypatch.chdir(superrepo / "submodule")
    result = CliRunner().invoke(cli, ["show-root"])
    assert result.exit_code == 0
    assert f"Resolved root: {superrepo}" in result.output
    assert "source: git" in result.output
