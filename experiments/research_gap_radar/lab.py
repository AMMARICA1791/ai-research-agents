"""Offline research-hypothesis triage, not novelty verification."""
import json
import re

REQUIRED=("hypothesis","falsifiable_prediction","experiment","baseline","prior_art")
def assess(candidate):
    if not isinstance(candidate,dict):
        raise TypeError("candidate must be a JSON object")
    missing=[k for k in REQUIRED if not isinstance(candidate.get(k),str) or not candidate[k].strip()]
    text=" ".join(str(candidate.get(k,"")) for k in REQUIRED)
    has_measure=bool(re.search(r"[0-9%]|accuracy|latency|error rate|precision|recall|seconds|percent|count|rate|time|cost",text,re.I))
    return {"ready_for_human_review":not missing and has_measure,
            "missing_fields":missing,
            "quantified_test_signal":has_measure,
            "novelty_verified":False,
            "prior_art_exhaustive":False,
            "scientific_claim_validated":False,
            "next_step":"independent prior-art and feasibility review"}

def evaluate(candidates):
    if not isinstance(candidates,list):
        raise TypeError("input must be a list")
    return {"dataset":"user_supplied_hypotheses",
            "items":[{"index":i,**assess(c)} for i,c in enumerate(candidates)]}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    a=p.parse_args()
    with open(a.input,encoding="utf-8") as f: data=json.load(f)
    print(json.dumps(evaluate(data),indent=2,ensure_ascii=False))
