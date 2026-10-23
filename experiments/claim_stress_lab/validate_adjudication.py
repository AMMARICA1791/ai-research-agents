"""Validate independent quote adjudications; never infer labels from verdicts."""
import argparse
import json
from collections import Counter
from pathlib import Path

REQUIRED = ("case_id", "source_url", "source_snapshot_sha256", "claim_text",
            "quoted_text", "source_contains_quote", "quote_supports_claim",
            "defect_label", "defect_type", "annotator_id", "annotated_at_utc",
            "independent_of_model_output", "notes")
TYPES = {"none", "missing_quote", "number", "negation", "causality",
         "unsupported", "other", "unreviewable"}


def validate(rows, minimum=30):
    if not isinstance(rows, list):
        raise ValueError("Expected a JSON array")
    errors, cases = [], {}
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row {i}: not an object")
            continue
        missing = set(REQUIRED) - row.keys()
        if missing:
            errors.append(f"row {i}: missing {sorted(missing)}")
            continue
        case = row["case_id"]
        if not isinstance(case, str) or not case.strip():
            errors.append(f"row {i}: invalid case_id")
            continue
        cases.setdefault(case, []).append(row)
        for key in ("source_contains_quote", "independent_of_model_output"):
            if type(row[key]) is not bool:
                errors.append(f"row {i}: {key} must be boolean")
        for key in ("quote_supports_claim", "defect_label"):
            if row[key] is not None and type(row[key]) is not bool:
                errors.append(f"row {i}: {key} must be boolean or null")
        if row["defect_type"] not in TYPES:
            errors.append(f"row {i}: unknown defect_type")
        if row["independent_of_model_output"] is not True:
            errors.append(f"row {i}: reviewer was not blinded")
        if not isinstance(row["source_snapshot_sha256"], str) or len(row["source_snapshot_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in row["source_snapshot_sha256"]):
            errors.append(f"row {i}: invalid source hash")
        for key in ("source_url", "claim_text", "annotator_id", "annotated_at_utc", "notes"):
            if not isinstance(row[key], str) or not row[key].strip():
                errors.append(f"row {i}: empty {key}")
        if row["defect_label"] is None and row["defect_type"] != "unreviewable":
            errors.append(f"row {i}: null label requires unreviewable type")
        if row["defect_label"] is False and row["defect_type"] != "none":
            errors.append(f"row {i}: negative defect label requires none type")
        if row["defect_label"] is True and row["defect_type"] in ("none", "unreviewable"):
            errors.append(f"row {i}: positive defect label requires defect type")
    for case, reviews in cases.items():
        reviewers = [r["annotator_id"] for r in reviews]
        if len(reviewers) != len(set(reviewers)):
            errors.append(f"case {case}: repeated reviewer")
        if len(reviews) < 2:
            errors.append(f"case {case}: fewer than two independent reviews")
        if len({(r["claim_text"], r["quoted_text"], r["source_snapshot_sha256"]) for r in reviews}) != 1:
            errors.append(f"case {case}: reviewer inputs disagree")
        labels = {r["defect_label"] for r in reviews}
        if len(labels) > 1:
            errors.append(f"case {case}: unresolved disagreement; adjudication required")
    if len(cases) < minimum:
        errors.append(f"only {len(cases)} cases; need at least {minimum}")
    return {"ready": not errors, "cases": len(cases), "reviews": len(rows),
            "reviewed_label_counts": dict(Counter(str(r["defect_label"]) for r in rows if isinstance(r, dict) and "defect_label" in r)),
            "errors": errors}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--minimum", type=int, default=30)
    a = p.parse_args()
    report = validate(json.loads(a.input.read_text(encoding="utf-8")), a.minimum)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["ready"] else 1)


if __name__ == "__main__":
    main()
