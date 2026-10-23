"""Small synthetic regression benchmark for review-priority flags.

Labels describe deliberately planted mechanical citation defects, NOT semantic truth.
This is a smoke test, not a scientific evaluation of real-world performance.
"""
import json
from pathlib import Path
from experiments.claim_stress_lab.lab import evaluate

CASES = [
    (True, {"id":"wrong-number","claim":"The trial enrolled 500 patients","quote":"The trial enrolled 50 patients","source_text":"The trial enrolled 50 patients.","source_url":"https://example.org/a"}),
    (True, {"id":"fabricated-quote","claim":"The trial enrolled 50 patients","quote":"The trial enrolled 50 patients","source_text":"A trial was discussed.","source_url":"https://example.org/b"}),
    (False, {"id":"exact-quote","claim":"The trial enrolled 50 patients","quote":"The trial enrolled 50 patients","source_text":"The trial enrolled 50 patients.","source_url":"https://example.org/c"}),
    (False, {"id":"other-evidence","claim":"The trial enrolled 50 patients","quote":"The trial enrolled 50 patients","source_text":"The trial enrolled 50 patients. The trial enrolled 50 patients.","source_url":"https://example.org/d"}),
]

def report():
    rows=[]
    for planted_defect, record in CASES:
        result=evaluate(record)
        # Only high-specificity mechanical defects are counted in this baseline.
        detected=bool(set(result["flags"]) & {"QUOTE_NOT_VERBATIM_IN_SOURCE","CLAIM_NUMBERS_ABSENT_FROM_QUOTE"})
        rows.append({"id":record["id"],"planted_mechanical_defect":planted_defect,"detected":detected,"flags":result["flags"]})
    # Baseline: flag only quotes absent verbatim from the archived source.\n    for row, (_, record) in zip(rows, CASES):\n        row["baseline_detected"] = not (bool(record["quote"].strip()) and record["quote"] in record["source_text"])\n    baseline_tp=sum(r["baseline_detected"] and r["planted_mechanical_defect"] for r in rows)\n    baseline_fp=sum(r["baseline_detected"] and not r["planted_mechanical_defect"] for r in rows)\n    baseline_fn=sum(not r["baseline_detected"] and r["planted_mechanical_defect"] for r in rows)\n    tp=sum(r["detected"] and r["planted_mechanical_defect"] for r in rows)
    fp=sum(r["detected"] and not r["planted_mechanical_defect"] for r in rows)
    fn=sum(not r["detected"] and r["planted_mechanical_defect"] for r in rows)
    return {"dataset":"synthetic_smoke_only","n":len(rows),"true_positive":tp,"false_positive":fp,"false_negative":fn,
            "precision":tp/(tp+fp) if tp+fp else None,"recall":tp/(tp+fn) if tp+fn else None,
            "baseline_exact_quote_only":{"true_positive":baseline_tp,"false_positive":baseline_fp,"false_negative":baseline_fn,\n            "precision":baseline_tp/(baseline_tp+baseline_fp) if baseline_tp+baseline_fp else None,\n            "recall":baseline_tp/(baseline_tp+baseline_fn) if baseline_tp+baseline_fn else None},\n            "semantic_accuracy":None,"publication_allowed":False,"cases":rows}

if __name__=="__main__":
    print(json.dumps(report(),indent=2))
