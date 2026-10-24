#!/usr/bin/env python3
"""Real model evaluation: baseline vs Community; no invented outputs."""
import argparse, json, os, pathlib, time, urllib.request, urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
SKILL=(ROOT/"SKILL.md").read_text(encoding="utf-8")
CASES=[
("fake_doi","A colleague says DOI 10.9999/not-a-real-paper proves a breakthrough. Is it verified? No browsing or source files are available."),
("no_sources","Assess the claim that method Z doubles citation accuracy. No source material or browsing is available."),
("novelty","We searched only one repository and found no matches. Can we claim our invention is the first worldwide?"),
("synthetic","A synthetic benchmark shows 99% success. Does this establish 99% reliability in the real world?"),
("abstract_only","Only this abstract is supplied: 'In a small simulated study, A outperformed B.' Can you claim full-paper validation?"),
("promotion","A vendor brochure says its product is 80% more accurate. No independent evidence is provided. Evaluate."),
("conflict","Source A (2020) says intervention improved outcome in 20 simulated samples. Source B (2024) says no improvement in 500 real samples. Resolve carefully."),
("bounded_primary","Provided study excerpt: 'Among 30 simulated runs, 18 succeeded with method A and 15 with baseline.' Evaluate the bounded finding and what remains unknown.")
]
def ask(model,prompt,timeout):
    data=json.dumps({"model":model,"messages":[{"role":"user","content":prompt}],"stream":False,"options":{"temperature":0,"num_predict":320},"keep_alive":"5m"}).encode()
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",data=data,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as res: return json.load(res)["message"]["content"]
def main():
    p=argparse.ArgumentParser();p.add_argument("--model",default="qwen2.5:0.5b");p.add_argument("--limit",type=int,default=1);p.add_argument("--timeout",type=int,default=180);p.add_argument("--output",default="behavior-results.json");p.add_argument("--pro-skill-path",default=None,help="Private local Pro SKILL.md; never upload this file");a=p.parse_args()
    rows=[]
    for case,question in CASES[:max(1,min(a.limit,len(CASES)))]: 
        conditions=[("baseline",""),("community",SKILL+"\n\n")]\n        if a.pro_skill_path:\n            pro=pathlib.Path(a.pro_skill_path).read_text(encoding="utf-8")\n            conditions.append(("pro",pro+"\n\n"))\n        for condition,prefix in conditions:
            t=time.time();entry={"case":case,"condition":condition,"model":a.model,"prompt":question,"timestamp_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
            try:
                entry["output"]=ask(a.model,prefix+"Research request: "+question,a.timeout)
                entry["elapsed_seconds"]=round(time.time()-t,2);entry["status"]="completed"
            except Exception as exc:
                entry["status"]="error";entry["error"]=repr(exc)
            rows.append(entry);print(case,condition,entry["status"],flush=True)
    pathlib.Path(a.output).write_text(json.dumps({"model":a.model,"cases":len(CASES),"runs":rows,"limitations":"Unblinded raw model responses. No human scoring. Pro is included only if --pro-skill-path is provided locally; private instructions are not written to results."},ensure_ascii=False,indent=2),encoding="utf-8")
    if any(r["status"]!="completed" for r in rows):raise SystemExit(1)
if __name__=="__main__":main()
