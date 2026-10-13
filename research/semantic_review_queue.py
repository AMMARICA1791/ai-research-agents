"""Generic claim-review queue, separate from domain-specific science.

This is an audit queue, not an automated entailment classifier. Every new or
edited statement is held for human adjudication with its source reference.
"""
import hashlib
import json
from pathlib import Path

def make_queue(report, baseline, review):
    originals = {f["id"]: f for f in baseline["findings"]}
    cases = {r["case_index"]: r for r in review["cases"]}
    queue = []
    for finding in report["findings"]:
        old = originals.get(finding["id"])
        same = old is not None and all(finding.get(k) == old.get(k) for k in
                                      ("source", "case_index", "statement", "kind", "confidence"))
        case = cases.get(finding.get("case_index"))
        queue.append({
            "claim_id": finding["id"],
            "statement": finding["statement"],
            "source": finding.get("source"),
            "pdf_page": case["pdf_page"] if case else None,
            "verbatim_sha256": case["verbatim_sha256"] if case else None,
            "review_state": "PROVISIONAL_UNCHANGED" if same else "NEEDS_SEMANTIC_REVIEW",
            "questions": [
                "Does the full source paragraph directly support the exact claim?",
                "Are model assumptions, isotope identities, and numerical qualifiers preserved?",
                "Is the statement broader than the source or dependent on missing context?",
                "Has an independent qualified reviewer adjudicated this claim?"
            ] if not same else [],
            "independently_verified": False,
        })
    removed = sorted(set(originals) - {f["id"] for f in report["findings"]})
    return {"schema_version": 1, "claims": queue, "removed_claim_ids": removed,
            "pending": sum(x["review_state"] == "NEEDS_SEMANTIC_REVIEW" for x in queue),
            "scientific_acceptance": "NOT_PASSED"}

def main():
    import argparse
    p = argparse.ArgumentParser()
    for name in ("report", "baseline", "review", "output"):
        p.add_argument("--" + name, required=True)
    a = p.parse_args()
    result = make_queue(*[json.loads(Path(getattr(a, k)).read_text()) for k in
                          ("report", "baseline", "review")])
    Path(a.output).write_text(json.dumps(result, indent=2) + "\n")
    print("SEMANTIC_REVIEW_QUEUE", result["pending"], "pending")

if __name__ == "__main__":
    main()
