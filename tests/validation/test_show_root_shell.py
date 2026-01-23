from __future__ import annotations

import os
import subprocess
from pathlib import Path


def _run_show_root(repo_root: Path, args: list[str], env: dict[str, str] | None = None) -> str:
    script = repo_root / "todo.ai"
    result = subprocess.run(
        [str(script), "show-root", *args],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    return (result.stdout or "") + (result.stderr or "")


def test_show_root_uses_git_root():
    repo_root = Path(__file__).parent.parent.parent
    output = _run_show_root(repo_root, [])
    assert "Resolved root:" in output
    assert "source: git" in output


def test_show_root_overrides(tmp_path: Path):
    repo_root = Path(__file__).parent.parent.parent
    override_root = tmp_path / "override-root"
    override_root.mkdir(parents=True, exist_ok=True)

    output = _run_show_root(repo_root, ["--root", str(override_root)])
    assert "Resolved root:" in output
    assert "source: --root" in output

    env = os.environ.copy()
    env["TODO_AI_ROOT"] = str(override_root)
    output = _run_show_root(repo_root, [], env=env)
    assert "Resolved root:" in output
    assert "source: env" in output
