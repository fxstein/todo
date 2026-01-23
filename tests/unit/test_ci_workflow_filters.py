from pathlib import Path


def test_ci_cd_has_change_detection():
    content = Path(".github/workflows/ci-cd.yml").read_text(encoding="utf-8")
    assert "dorny/paths-filter" in content
    assert "docs:" in content
    assert "logs_only:" in content
    assert "code:" in content


def test_ci_cd_has_docs_quality_job():
    content = Path(".github/workflows/ci-cd.yml").read_text(encoding="utf-8")
    assert "docs-quality" in content
    assert "markdownlint-cli2-action" in content
