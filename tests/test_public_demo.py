"""Keep the public one-click demonstration honest, repeatable, and read-only."""
from pathlib import Path

import pytest

from lab.public_demo import (
    HISTORICAL_LINE, SAFE_LINE, collect_evidence,
    main, markdown_summary,
)
from lab.real_repo_repair import TARGET

ROOT = Path(__file__).resolve().parents[1]


def test_public_demo_proves_known_three_bounded_checks_without_mutating_source():
    target = ROOT / TARGET
    old = target.read_bytes()
    proof = collect_evidence(ROOT)
    assert target.read_bytes() == old
    assert proof["status"] == "verified_bounded_experiments"
    assert proof["no_paid_model_api_required"] is True
    assert proof["model_inference_this_run"] is False
    assert proof["external_user_code_executed"] is False
    assert proof["repository_files_changed"] is False
    scanner = proof["experiments"]["static_scanner"]
    assert (scanner["tested_cases"], scanner["cases_passed"]) == (8, 8)
    assert proof["experiments"]["synthetic_repair"]["model_authored"] is False
    real = proof["experiments"]["real_repository_regression"]
    assert real["test_before"] == "FAIL"
    assert real["test_after"] == "PASS"
    assert real["model_run_replayed"] is False
    assert real["historical_pull_request"].endswith("/17")


def test_public_demo_refuses_unrecognized_source(tmp_path):
    target = tmp_path / TARGET
    target.parent.mkdir()
    target.write_text("def unrelated(): return 42\n", encoding="utf-8")
    with pytest.raises(ValueError, match="previously-reviewed URL repair"):
        collect_evidence(tmp_path)


def test_public_demo_renders_report_without_overclaiming(tmp_path):
    out = tmp_path / "public-report"
    assert main(["--repo", str(ROOT), "--out", str(out)]) == 0
    summary = (out / "SUMMARY.md").read_text(encoding="utf-8")
    assert "synthetic" in summary
    assert "does not rerun Qwen" in summary
    assert "One-click evidence tour" in summary
    import json
    report = json.loads((out / "evidence.json").read_text(encoding="utf-8"))
    assert summary == markdown_summary(report)
    assert report["model_inference_this_run"] is False


def test_fixture_line_patterns_remain_exact():
    source = (ROOT / TARGET).read_text(encoding="utf-8")
    assert source.count(SAFE_LINE) == 1
    assert HISTORICAL_LINE not in source


def test_public_instructions_distinguish_viewers_from_workflow_operators():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    guide = (ROOT / "docs/PUBLIC_DEMO.md").read_text(encoding="utf-8")
    quick = (ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    for text in (readme, guide, quick):
        assert "successful run" in text
        assert "write access" in text
    assert "Sign in to GitHub" in guide
