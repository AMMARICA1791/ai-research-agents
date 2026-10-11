"""Independent empirical gates for the bounded self-repair and scanner benchmark."""
import ast
from pathlib import Path

import pytest

from lab.autorepair import FIXTURE, evaluate_repair_demo, propose_fail_closed
from lab.benchmark import CASES, run_scanner_benchmark


def test_scanner_benchmark_reports_actual_confusion_matrix():
    result = run_scanner_benchmark()
    assert result["case_count"] == len(CASES) == 8
    assert result["passed_cases"] == 8
    assert result["true_positive"] == 5
    assert result["false_positive"] == 0
    assert result["false_negative"] == 0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0
    assert "production_generalization" in result["not_measured"]


def test_bounded_repair_produces_a_real_syntax_valid_patch():
    proposal = propose_fail_closed(FIXTURE)
    assert proposal["source_changed"] is False
    assert proposal["approval_required"] is True
    assert proposal["changed_line"] == 5
    assert "-        pass" in proposal["patch"]
    assert "+        raise" in proposal["patch"]
    assert FIXTURE.endswith("        pass\n")
    assert proposal["candidate"].endswith("        raise\n")
    ast.parse(proposal["candidate"])


def test_real_red_to_green_fixture_execution_without_repo_change():
    proof = evaluate_repair_demo()
    assert proof["status"] == "validated_synthetic_only"
    assert proof["baseline"]["passed"] is False
    assert proof["repaired"]["passed"] is True
    assert proof["changes_applied_to_repository"] is False
    assert proof["safety"]["auto_merge"] is False
    assert proof["safety"]["arbitrary_project_code_executed"] is False


@pytest.mark.parametrize("source", [
    "def f():\n    pass\n",
    "try:\n    pass\nexcept Exception:\n    return None\n",
    "try:\n    pass\nexcept:\n    pass\n",
    "try:\n    pass\nexcept KeyError:\n    pass\nexcept ValueError:\n    pass\n",
])
def test_repair_refuses_unsupported_or_ambiguous_cases(source):
    with pytest.raises(ValueError):
        propose_fail_closed(source)


@pytest.mark.parametrize("filename", [
    "../escaped.py", ".hidden.py", "dir/file.py", "config.json",
])
def test_repair_rejects_unsafe_output_names(filename):
    with pytest.raises(ValueError):
        propose_fail_closed(FIXTURE, filename=filename)


def test_proposer_makes_no_changes_to_project_tree(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "unchanged.py").write_text(FIXTURE)
    before = (tmp_path / "unchanged.py").read_bytes()
    proposal = propose_fail_closed(FIXTURE)
    assert proposal["candidate"] != FIXTURE
    assert (tmp_path / "unchanged.py").read_bytes() == before
    assert not (tmp_path / "results").exists()
