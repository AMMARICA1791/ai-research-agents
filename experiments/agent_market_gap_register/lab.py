"""Evidence-gated market opportunity triage. No novelty or demand prediction."""
import json
from urllib.parse import urlparse

REQUIRED=("problem","buyer","current_workaround","falsifiable_test","success_metric","competitors")
def inspect(item):
    if not isinstance(item,dict):
        raise TypeError("opportunity must be an object")
    missing=[k for k in REQUIRED if not isinstance(item.get(k),str) or not item[k].strip()]
    evidence=item.get("evidence",[])
    if not isinstance(evidence,list):
        raise TypeError("evidence must be a list")
    valid=[]
    for e in evidence:
        if not isinstance(e,dict):
            continue
        u=e.get("url","")
        parsed=urlparse(u) if isinstance(u,str) else None
        if parsed and parsed.scheme=="https" and parsed.hostname and isinstance(e.get("observation"),str) and e["observation"].strip():
            valid.append({"url":u,"observation":e["observation"]})
    return {"ready_for_customer_discovery":not missing and bool(valid),
            "missing_fields":missing,"evidence_count":len(valid),
            "buyer_demand_verified":False,"novelty_verified":False,
            "recommended_next_step":"interview buyers and benchmark nearest existing solutions"}

def evaluate(items):
    if not isinstance(items,list):
        raise TypeError("input must be a list")
    return {"status":"hypothesis_triage_only","items":[{"index":i,**inspect(x)} for i,x in enumerate(items)]}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    a=p.parse_args()
    with open(a.input,encoding="utf-8") as f: items=json.load(f)
    print(json.dumps(evaluate(items),ensure_ascii=False,indent=2))
