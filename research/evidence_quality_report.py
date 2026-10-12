"""Report evidence quality without treating repeated rows as independent support."""
import argparse
import json
from collections import Counter
from pathlib import Path

def summarize(review):
    cases = review["cases"]
    unique = [row for row in cases if row["case_index"] == row["canonical_case_index"]]
    counts = Counter(row["judgment"] for row in unique)
    return {
        "extracted_rows": len(cases),
        "unique_excerpts": len(unique),
        "duplicate_rows": len(cases)-len(unique),
        "provisional_directly_stated": counts["DIRECTLY_STATED"],
        "provisional_context_required": counts["CONTEXT_REQUIRED"],
        "provisional_not_evidence": counts["NOT_EVIDENCE"],
        "excluded_case_indices": [x["case_index"] for x in unique if x["judgment"] == "NOT_EVIDENCE"],
        "context_required_case_indices": [x["case_index"] for x in unique if x["judgment"] == "CONTEXT_REQUIRED"],
        "independent_expert_labels": 0,
        "scientific_acceptance": "NOT_PASSED",
        "caution": "DIRECTLY_STATED is a provisional textual judgment, not validated entailment."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--review",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    report=summarize(json.loads(Path(a.review).read_text()))
    Path(a.output).write_text(json.dumps(report,indent=2)+"\n")
    print("EVIDENCE_QUALITY",report)

if __name__=="__main__":
    main()
