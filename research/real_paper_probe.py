"""Adversarial evaluation on verbatim candidate excerpts from two primary papers.

A lexical classifier must not claim semantic verification on real excerpts.
This produces observable predictions for review, with source and page.
"""
import argparse
import json
from pathlib import Path
from research.bounded_entailment import classify\nfrom research.scientific_comparison_engine import is_front_matter

def matched_claims(quote):
    from research.bounded_entailment import CLAIMS
    import re
    return [claim for claim,spec in CLAIMS.items()
            if re.search(spec["subject"],quote,re.I)
            and re.search(spec["predicate"],quote,re.I)]

def evaluate(report):
    rows=[]
    for source,record in report["sources"].items():
        for axis,items in record["axes"].items():
            for item in items[:5]:
                quote=item["verbatim_text"]
                excluded=is_front_matter(quote)\n                claims=[] if excluded else matched_claims(quote)
                rows.append({"source":source,"axis":axis,"pdf_page":item["pdf_page"],
                             "verbatim_text":quote,"candidate_claims":claims,
                             "classifications":[{"claim_id":claim,
                                                 "classifier_output":classify(claim,quote)}
                                                for claim in claims],
                             "ground_truth":"UNLABELED",
                             "semantic_correctness":"NOT_ASSESSED",
                             "claim_alignment":"EXCLUDED_FRONT_MATTER" if excluded else ("LEXICAL_CANDIDATE" if claims else "NO_MATCHING_CLAIM"),\n                             "evidence_role":"UNDETERMINED_PENDING_EXPERT_REVIEW"})
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
