"""Auditable human adjudication of quote-to-claim logical relationships.

This module does not infer entailment with an LLM or claim automated scientific proof.
"""
from __future__ import annotations

import json
from pathlib import Path

from research.source_passage_verification import verify_passages

RELATIONS = {"supports", "contradicts", "insufficient", "out_of_scope"}
REVIEW_STATES = {"pending", "reviewed"}


def evaluate_relationships(payload: dict, source_dir: str | Path) -> dict:
    """Require exact quote matches before accepting explicit reviewer judgments."""
    screening = verify_passages(payload, source_dir)
    records = payload.get("relationship_reviews")
    if not isinstance(records, list):
        raise ValueError("relationship_reviews must be an array")
    evidence_keys = {
        (x["claim_id"], x["doi"], x["locator"]): x["quote_exact_match"]
        for x in screening["findings"]
    }
    if len(evidence_keys) != len(screening["findings"]):
        raise ValueError("Ambiguous duplicate evidence links")
    reviewed = {}
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("Invalid relationship review")
        key = (item.get("claim_id"), item.get("doi"), item.get("locator"))
        if key not in evidence_keys or key in reviewed:
            raise ValueError("Unknown or duplicate evidence review")
        state = item.get("review_status")
        relation = item.get("relation")
        rationale = item.get("rationale")
        reviewer = item.get("reviewer")
        if state not in REVIEW_STATES:
            raise ValueError("Invalid review status")
        if state == "pending":
            if relation is not None or rationale is not None or reviewer is not None:
                raise ValueError("Pending review cannot assert a judgment")
        else:
            if not evidence_keys[key]:
                raise ValueError("Cannot adjudicate evidence with an unmatched quotation")
            if relation not in RELATIONS:
                raise ValueError("Invalid logical relationship")
            if not isinstance(rationale, str) or not rationale.strip() or len(rationale) > 2000:
                raise ValueError("Reviewed relationship requires rationale")
            if not isinstance(reviewer, str) or not reviewer.strip() or len(reviewer) > 120:
                raise ValueError("Reviewed relationship requires reviewer")
        reviewed[key] = item
    output = []
    for finding in screening["findings"]:
        key = (finding["claim_id"], finding["doi"], finding["locator"])
        item = reviewed.get(key)
        status = item["review_status"] if item else "pending"
        output.append({
            **finding,
            "review_status": status,
            "relation": item["relation"] if status == "reviewed" else None,
            "rationale": item["rationale"] if status == "reviewed" else None,
            "reviewer": item["reviewer"] if status == "reviewed" else None,
            "machine_entailment_verified": False,
            "scientific_support_verified": False,
        })
    return {
        "status": "human_relationship_review",
        "links": output,
        "reviewed_count": sum(x["review_status"] == "reviewed" for x in output),
        "pending_count": sum(x["review_status"] == "pending" for x in output),
        "machine_entailment_verified": False,
        "scientific_support_verified": False,
    }


def main(argv=None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Audit human quote-to-claim reviews")
    parser.add_argument("--input", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    result = evaluate_relationships(json.loads(Path(args.input).read_text(encoding="utf-8")), args.source_dir)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"reviewed_count": result["reviewed_count"], "pending_count": result["pending_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
