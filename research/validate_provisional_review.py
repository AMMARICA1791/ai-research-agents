"""Validate provisional review against a real-paper-probe artifact, without claiming scientific acceptance."""
import argparse
import json
from pathlib import Path

def validate(review, probe):
    assert review["status"] == "PROVISIONAL_NOT_INDEPENDENTLY_ADJUDICATED"
    assert review["scientific_acceptance"] == "NOT_PASSED"
    cases = probe["cases"]
    seen = set()
    for item in review["cases"]:
        idx = item["case_index"]
        assert isinstance(idx, int) and 0 <= idx < len(cases)
        assert idx not in seen
        seen.add(idx)
        row = cases[idx]
        assert (row["source"], row["pdf_page"]) == (item["source"], item["pdf_page"])
        assert row["ground_truth"] == "UNLABELED"
        assert item["review_status"] == "PROVISIONAL"
        assert item["judgment"] in {"DIRECTLY_STATED", "NOT_EVIDENCE", "CONTEXT_REQUIRED"}
    return {"reviewed": len(seen), "total": len(cases),
            "independent_expert_labels": 0, "scientific_acceptance": "NOT_PASSED"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--review", required=True)
    p.add_argument("--probe", required=True)
    a = p.parse_args()
    print(json.dumps(validate(json.loads(Path(a.review).read_text()),
                              json.loads(Path(a.probe).read_text()))))

if __name__ == "__main__":
    main()
