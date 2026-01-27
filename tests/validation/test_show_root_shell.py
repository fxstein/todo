from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

# Skip all tests in this module
# After v3.1 API terminology standardization (#253), Python and shell are intentionally divergent
# These tests will be removed as part of task #254
pytestmark = pytest.mark.skip(reason="Shell tests obsolete after API standardization (#253)")

_IS_WINDOWS = os.name == "nt"


def _run_show_root(
    script_root: Path,
    cwd: Path,
    args: list[str],
    env: dict[str, str] | None = None,
) -> str:
    script = script_root / "legacy" / "todo.ai"
    result = subprocess.run(
        [str(script), "show-root", *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    return (result.stdout or "") + (result.stderr or "")


@pytest.mark.skipif(_IS_WINDOWS, reason="todo.ai shell script is not runnable on Windows")
def test_show_root_uses_git_root():
    repo_root = Path(__file__).parent.parent.parent
    output = _run_show_root(repo_root, repo_root, [])
    assert "Resolved root:" in output
    assert "source: git" in output


@pytest.mark.skipif(_IS_WINDOWS, reason="todo.ai shell script is not runnable on Windows")
def test_show_root_overrides(tmp_path: Path):
    repo_root = Path(__file__).parent.parent.parent
    override_root = tmp_path / "override-root"
    override_root.mkdir(parents=True, exist_ok=True)

    output = _run_show_root(repo_root, repo_root, ["--root", str(override_root)])
    assert "Resolved root:" in output
    assert "source: --root" in output

    env = os.environ.copy()
    env["TODO_AI_ROOT"] = str(override_root)
    output = _run_show_root(repo_root, repo_root, [], env=env)
    assert "Resolved root:" in output
    assert "source: env" in output


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


@pytest.mark.skipif(_IS_WINDOWS, reason="todo.ai shell script is not runnable on Windows")
def test_show_root_from_submodule(tmp_path: Path):
    repo_root = Path(__file__).parent.parent.parent
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

    output = _run_show_root(repo_root, superrepo / "submodule", [])
    assert f"Resolved root: {superrepo}" in output
    assert "source: git" in output
