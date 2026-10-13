"""Bounded scientific claim/evidence entailment benchmark.

Deterministic inference for explicit assertions and negations only. Not a
general-purpose language model or a validation of astrophysical truth.
"""
import argparse
import json
import re
from pathlib import Path

CLAIMS = {
 "iron_group_yields": {"subject":r"iron[ -]group", "predicate":r"yields?|production"},
 "nucleosynthesis": {"subject":r"nucleosynthesis", "predicate":r"explosions?|supernovae?|explosive"},
}
NEGATION = re.compile(r"\b(?:no|not|never|without|neither|cannot|does not|do not)\b",re.I)

def classify(claim_id, quote):
    if claim_id not in CLAIMS: return "INSUFFICIENT_EVIDENCE"
    if not isinstance(quote,str) or len(quote)>1200: return "INSUFFICIENT_EVIDENCE"
    s=re.sub(r"\s+"," ",quote).strip()
    spec=CLAIMS[claim_id]
    subject=re.search(spec["subject"],s,re.I)
    predicate=re.search(spec["predicate"],s,re.I)
    if not subject or not predicate: return "INSUFFICIENT_EVIDENCE"
    # Prevent distant unrelated assertions from counting as entailment.
    if abs(subject.start()-predicate.start())>130: return "INSUFFICIENT_EVIDENCE"
    span=s[max(0,min(subject.start(),predicate.start())-30):max(subject.end(),predicate.end())+30]
    return "CONTRADICTED_EXPLICITLY" if NEGATION.search(span) else "SUPPORTED_EXPLICITLY"

def evaluate(cases):
    output=[]
    for case in cases:
        actual=classify(case["claim_id"],case["quote"])
        output.append({"id":case["id"],"expected":case["expected"],"actual":actual,
                       "correct":actual==case["expected"]})
    return {"benchmark":"bounded_entailment_v1","cases":output,
            "correct":sum(x["correct"] for x in output),"total":len(output),
            "passed":bool(output) and all(x["correct"] for x in output),
            "scope":"Explicit short-sentence co-occurrence and negation only",
            "independent_scientific_truth_verified":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cases",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    report=evaluate(json.loads(Path(a.cases).read_text())["cases"])
    Path(a.output).write_text(json.dumps(report,indent=2)+"\n")
    print("BOUNDED_ENTAILMENT",report["correct"],"/",report["total"],"PASS" if report["passed"] else "FAIL",flush=True)
    if not report["passed"]: raise SystemExit(1)

if __name__=="__main__":main()
