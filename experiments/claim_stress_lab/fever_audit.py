"""Safely inspect FEVER JSONL annotations without inventing quote-level labels.

FEVER contains claim-level SUPPORTS/REFUTES/NOT ENOUGH INFO judgments and
Wikipedia sentence identifiers, NOT verified quote strings in this file.
This script audits eligibility; it intentionally never feeds FEVER labels into
the mechanical-defect evaluator.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

LABELS = {"SUPPORTS", "REFUTES", "NOT ENOUGH INFO"}


def audit(path, limit=None):
    counts = Counter()
    examples = []
    with Path(path).open(encoding="utf-8") as stream:
        for lineno, line in enumerate(stream, 1):
            if not line.strip():
                continue
            obj = json.loads(line)
            if not isinstance(obj, dict) or obj.get("label") not in LABELS or not isinstance(obj.get("claim"), str):
                raise ValueError(f"Invalid FEVER record at line {lineno}")
            counts[obj["label"]] += 1
            evidence = obj.get("evidence")
            references = []
            if isinstance(evidence, list):
                for group in evidence:
                    if isinstance(group, list):
                        for entry in group:
                            if isinstance(entry, list) and len(entry) >= 4 and entry[2] is not None and entry[3] is not None:
                                references.append({"page": entry[2], "sentence_id": entry[3]})
            if len(examples) < 5:
                examples.append({"id": obj.get("id"), "label": obj["label"], "evidence_references": references[:5]})
            if limit is not None and sum(counts.values()) >= limit:
                break
    return {"dataset": "FEVER", "claims_read": sum(counts.values()), "claim_labels": dict(counts),
            "sample_references": examples, "quote_text_resolved": False,
            "independent_quote_defect_labels": False, "ready_for_claim_stress_evaluation": False,
            "publication_allowed": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--limit", type=int)
    args = p.parse_args()
    if args.limit is not None and args.limit < 1:
        p.error("--limit must be positive")
    print(json.dumps(audit(args.input, args.limit), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
