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


def test_semantically_false_claim_is_rejected_by_review_gate():
    """Regression exposure: a correct excerpt fingerprint does not validate a claim."""
    import copy
    report = copy.deepcopy(REPORT)
    report["findings"][0]["statement"] = "The paper proves that all iron on Earth originated exclusively in Type Ia supernovae."
    from research.claim_review_gate import assess, enforce
    assert assess(report, REPORT)["decision"] == "ABSTAIN"
    with pytest.raises(ValueError):
        enforce(report, REPORT)

def test_new_claim_and_removed_finding_abstain():
    import copy
    from research.claim_review_gate import assess
    missing = copy.deepcopy(REPORT)
    missing["findings"].pop()
    assert assess(missing, REPORT)["decision"] == "ABSTAIN"
    added = copy.deepcopy(REPORT)
    added["findings"].append({"id":"F7","statement":"Earth's iron is exclusively Type Ia.","source":"type_ia","case_index":16})
    assert assess(added, REPORT)["decision"] == "ABSTAIN"

def test_original_report_is_only_provisionally_review_bound():
    from research.claim_review_gate import enforce
    result = enforce(REPORT, REPORT)
    assert result["decision"] == "PROVISIONAL_ONLY"
    assert result["independent_semantic_verification"] is False
    assert result["scientific_acceptance"] == "NOT_PASSED"
