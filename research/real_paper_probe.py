"""Adversarial evaluation on verbatim candidate excerpts from two primary papers.

A lexical classifier must not claim semantic verification on real excerpts.
This produces observable predictions for review, with source and page.
"""
import argparse
import json
from pathlib import Path
from research.bounded_entailment import classify

CLAIM_MAP={"results":"iron_group_yields","methods":"nucleosynthesis","limitations":"iron_group_yields"}

def evaluate(report):
    rows=[]
    for source,record in report["sources"].items():
        for axis,items in record["axes"].items():
            for item in items[:5]:
                quote=item["verbatim_text"]
                claim=CLAIM_MAP[axis]
                rows.append({"source":source,"axis":axis,"pdf_page":item["pdf_page"],
                             "verbatim_text":quote,"claim_id":claim,
                             "classifier_output":classify(claim,quote),
                             "ground_truth":"UNLABELED",
                             "semantic_correctness":"NOT_ASSESSED"})
    return {"test":"real_primary_paper_claim_evidence_probe",
            "total_verbatim_cases":len(rows),"cases":rows,
            "scientific_semantic_accuracy":"NOT_MEASURABLE_WITHOUT_EXPERT_LABELS",
            "scientific_acceptance":"NOT_PASSED",
            "disclaimer":"No claim of correctness based on keyword classification."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--comparison",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    result=evaluate(json.loads(Path(a.comparison).read_text()))
    Path(a.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("REAL_PAPER_PROBE",result["total_verbatim_cases"],"UNLABELED; SCIENTIFIC_ACCEPTANCE NOT_PASSED",flush=True)
    if not result["total_verbatim_cases"]:raise SystemExit("NO_REAL_PAPER_EVIDENCE")

if __name__=="__main__":main()
