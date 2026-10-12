import json
from pathlib import Path
import pytest
from research.validate_provisional_review import validate

REVIEW = json.loads(Path("research/provisional_primary_paper_review.json").read_text())

def synthetic_probe():
    cases = [{"source": "other", "pdf_page": 0, "ground_truth": "UNLABELED"} for _ in range(30)]
    for item in REVIEW["cases"]:
        cases[item["case_index"]] = {"source": item["source"],
                                      "pdf_page": item["pdf_page"],
                                      "ground_truth": "UNLABELED"}
    return {"cases": cases}

def test_review_is_provisional_and_traceable():
    result = validate(REVIEW, synthetic_probe())
    assert result["reviewed"] == 8
    assert result["independent_expert_labels"] == 0
    assert result["scientific_acceptance"] == "NOT_PASSED"

def test_mismatched_source_page_rejected():
    probe = synthetic_probe()
    probe["cases"][20]["pdf_page"] = 99
    with pytest.raises(AssertionError):
        validate(REVIEW, probe)
