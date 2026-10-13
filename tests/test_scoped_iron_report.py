import json
from pathlib import Path
import pytest
from research.validate_scoped_iron_report import validate

ROOT = Path("research")
REPORT = json.loads((ROOT / "scoped_iron_report.json").read_text())
REVIEW = json.loads((ROOT / "provisional_primary_paper_review.json").read_text())

def test_scoped_report_is_conservative():
    assert len(REPORT["findings"]) == 6
    assert REPORT["scientific_acceptance"] == "NOT_PASSED"
    assert REPORT["independent_expert_labels"] == 0
    assert REPORT["earth_iron"]["conclusion"] == "NOT_ESTABLISHED_BY_THESE_TWO_PAPERS_ALONE"
    assert all(REVIEW["cases"][f["case_index"]]["judgment"] == "DIRECTLY_STATED" for f in REPORT["findings"])

def test_report_rejects_synthetic_excerpt_substitution():
    probe = {"cases": [{"source": r["source"], "pdf_page": r["pdf_page"],
                        "verbatim_text": "fabricated quote", "ground_truth": "UNLABELED"}
                       for r in REVIEW["cases"]]}
    with pytest.raises(AssertionError):
        validate(REPORT, REVIEW, probe)


def test_semantically_false_claim_can_pass_existing_validator():
    """Regression exposure: a correct excerpt fingerprint does not validate a claim."""
    import copy
    report = copy.deepcopy(REPORT)
    report["findings"][0]["statement"] = "The paper proves that all iron on Earth originated exclusively in Type Ia supernovae."
    probe = {"cases": [{"source": r["source"], "pdf_page": r["pdf_page"],
                        "verbatim_text": "", "ground_truth": "UNLABELED"}
                       for r in REVIEW["cases"]]}
    # Populate genuine excerpts only when supplied by real primary-paper extraction.
    # The current validator never examines statement text, so this mutation is
    # undetectable regardless of the verbatim evidence supplied.
    assert report["findings"][0]["statement"] != REPORT["findings"][0]["statement"]
    assert "statement" not in __import__("inspect").getsource(validate)
