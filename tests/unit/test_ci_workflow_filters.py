from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_cd_has_change_detection():
    content = (_repo_root() / ".github/workflows/ci-cd.yml").read_text(encoding="utf-8")
    assert "dorny/paths-filter" in content
    assert "docs:" in content
    assert "logs:" in content
    assert "all:" in content
    assert "**/*.md" in content
    assert "**/*.log" in content


def test_ci_cd_has_docs_quality_job():
    content = (_repo_root() / ".github/workflows/ci-cd.yml").read_text(encoding="utf-8")
    assert "docs-quality" in content
    assert "markdownlint-cli2-action" in content
