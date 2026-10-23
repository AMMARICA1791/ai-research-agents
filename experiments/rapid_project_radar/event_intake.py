"""Validate external news events and produce inert project proposals, never execute content."""
import argparse
import hashlib
import json
import re
from urllib.parse import urlsplit

def intake(event):
    if not isinstance(event,dict):
        raise ValueError("event must be an object")
    title=event.get("title")
    url=event.get("url")
    if not isinstance(title,str) or not 8<=len(title.strip())<=250:
        raise ValueError("invalid title")
    if not isinstance(url,str) or len(url)>2048:
        raise ValueError("invalid url")
    parsed=urlsplit(url)
    if parsed.scheme!="https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("HTTPS public source required")
    if not re.fullmatch(r"[A-Za-z0-9.-]+",parsed.hostname):
        raise ValueError("invalid hostname")
    key=hashlib.sha256(url.strip().encode()).hexdigest()[:20]
    return {"id":key,"title":title.strip(),"source_url":url.strip(),
            "status":"proposal_only","requires_prior_art_review":True,
            "novelty_verified":False,"project_created":False,
            "untrusted_input":True}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True);p.add_argument("--output",required=True)
    args=p.parse_args()
    with open(args.input,encoding="utf-8") as f: event=json.load(f)
    result=intake(event)
    with open(args.output,"w",encoding="utf-8") as f: json.dump(result,f,indent=2)
