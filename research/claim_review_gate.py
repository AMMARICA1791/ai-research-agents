"""Conservative, review-bound claim gate; NOT a general semantic entailment model.

Exact reviewed statements are approved only as provisional text interpretations.
Any edited, novel, or broadened statement abstains. Human expert review is still required.
"""
import hashlib
import json
from pathlib import Path

def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def assess(report, baseline):
    allowed = {f["id"]: f for f in baseline["findings"]}
    decisions = []
    for finding in report.get("findings", []):
        original = allowed.get(finding.get("id"))
        unchanged = bool(original) and all(
            finding.get(k) == original.get(k)
            for k in ("id", "source", "case_index", "statement", "kind", "confidence")
        )
        decisions.append({
            "id": finding.get("id"),
            "decision": "PROVISIONAL_REVIEW_BOUND" if unchanged else "ABSTAIN_CHANGED_OR_UNREVIEWED_CLAIM",
            "statement_sha256": digest(finding.get("statement", "")),
            "independent_semantic_verification": False,
        })
    ids = [f.get("id") for f in report.get("findings", [])]
    complete = len(ids) == len(allowed) and len(set(ids)) == len(ids) and set(ids) == set(allowed)
    unchanged_boundaries = all(
        report.get(k) == baseline.get(k)
        for k in ("comparison", "earth_iron", "boundaries", "scientific_acceptance", "independent_expert_labels")
    )
    accepted = complete and unchanged_boundaries and all(
        x["decision"] == "PROVISIONAL_REVIEW_BOUND" for x in decisions
    )
    return {
        "decision": "PROVISIONAL_ONLY" if accepted else "ABSTAIN",
        "findings": decisions,
        "independent_semantic_verification": False,
        "scientific_acceptance": "NOT_PASSED",
        "note": "Exact-string review binding detects claim edits, not semantic entailment; no expert labels.",
    }

def enforce(report, baseline):
    result = assess(report, baseline)
    if result["decision"] != "PROVISIONAL_ONLY":
        raise ValueError("Unreviewed or modified scientific claim: ABSTAIN")
    return result

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--baseline", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    result = enforce(json.loads(Path(a.report).read_text()), json.loads(Path(a.baseline).read_text()))
    Path(a.output).write_text(json.dumps(result, indent=2) + "\n")
    print("CLAIM_REVIEW_GATE", result["decision"], flush=True)

if __name__ == "__main__":
    main()
