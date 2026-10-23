"""Compare immutable evidence snapshots without network access."""
import hashlib
import json
import re

def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def normalize(text):
    return " ".join(text.split())

def inspect(previous, current, required_quotes):
    """Return evidence changes; quote presence is not semantic truth."""
    if not isinstance(previous,str) or not isinstance(current,str):
        raise TypeError("snapshots must be strings")
    if not isinstance(required_quotes,list) or any(not isinstance(q,str) or not q.strip() for q in required_quotes):
        raise ValueError("required_quotes must be a list of nonempty strings")
    old,new=normalize(previous),normalize(current)
    return {"previous_sha256":digest(previous),"current_sha256":digest(current),
            "changed":digest(previous)!=digest(current),
            "normalized_changed":old!=new,
            "quote_checks":[{"quote":q,"previous_present":normalize(q) in old,
                             "current_present":normalize(q) in new,
                             "lost":normalize(q) in old and normalize(q) not in new}
                            for q in required_quotes],
            "semantic_validity":None,"publication_allowed":False}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--before",required=True);p.add_argument("--after",required=True)
    p.add_argument("--quote",action="append",default=[])
    a=p.parse_args()
    with open(a.before,encoding="utf-8") as f: old=f.read()
    with open(a.after,encoding="utf-8") as f: new=f.read()
    print(json.dumps(inspect(old,new,a.quote),ensure_ascii=False,indent=2))
