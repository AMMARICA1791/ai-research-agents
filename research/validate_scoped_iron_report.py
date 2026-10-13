"""Fail-closed source-binding validation for the scoped iron report."""
import argparse
import hashlib
import json
from pathlib import Path
from research.claim_review_gate import enforce

def validate(report, review, probe, baseline=None):
    if baseline is None:
        baseline = json.loads(Path('research/reviewed_iron_claims_baseline.json').read_text())
    claim_gate = enforce(report, baseline)
    assert report["scientific_acceptance"] == "NOT_PASSED"
    assert report["independent_expert_labels"] == 0
    assert report["earth_iron"]["conclusion"] == "NOT_ESTABLISHED_BY_THESE_TWO_PAPERS_ALONE"
    assert report["comparison"]["cross_paper_agreement"] == "NOT_ESTABLISHED"
    cases = review["cases"]
    rows = probe["cases"]
    assert len(cases) == len(rows)
    used = set()
    for finding in report["findings"]:
        idx = finding["case_index"]
        assert idx not in used
        used.add(idx)
        reviewed = cases[idx]
        source = rows[idx]
        assert finding["source"] == reviewed["source"] == source["source"]
        assert reviewed["judgment"] == "DIRECTLY_STATED"
        assert reviewed["canonical_case_index"] == idx
        assert reviewed["review_status"] == "PROVISIONAL"
        assert hashlib.sha256(source["verbatim_text"].encode()).hexdigest() == reviewed["verbatim_sha256"]
        assert source["pdf_page"] == reviewed["pdf_page"]
        assert source["ground_truth"] == "UNLABELED"
        assert finding["confidence"] == "PROVISIONAL_TEXTUAL_SUPPORT"
    assert len(used) >= 2
    assert {x["source"] for x in report["findings"]} == set(report["sources"])
    return {"findings_checked": len(used), "source_count": 2,
            "independent_expert_labels": 0, "scientific_acceptance": "NOT_PASSED", "claim_gate": claim_gate["decision"]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--review", required=True)
    p.add_argument("--probe", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    result = validate(json.loads(Path(a.report).read_text()),
                      json.loads(Path(a.review).read_text()),
                      json.loads(Path(a.probe).read_text()))
    Path(a.output).write_text(json.dumps(result, indent=2) + "\n")
    print("SCOPED_IRON_REPORT", result)

if __name__ == "__main__":
    main()
