"""Auditable, conservative cross-paper scientific reasoning engine.

It produces source-backed comparison records, not model-generated scientific
truth. Explicitly abstains from causal/quantitative claims absent expert review.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

AXES = {
 "methods":r"\b(?:methods?|models?|simulations?|calculations?|hydrodynamic|deflagration|detonation)\b",
 "results":r"\b(?:yields?|abundances?|production|results?|synthesi[sz])\b",
 "limitations":r"\b(?:uncertain(?:ty|ties)?|sensitive|sensitivity|depend\w*|assum\w*|limitations?|mass cut)\b",
}
SUBJECT = re.compile(r"\b(?:iron[ -]group|nucleosynthesis|nickel|isotop\w*|\bFe\b|supernova)\b",re.I)

def sentences(text):
    """Keep page references; reject likely two-column row interleaving.

    The source should be extracted with pdftotext -raw, which follows PDF
    content-stream order rather than merging horizontal rows (-layout).
    """
    for page_no,page in enumerate(text.split("\f"),1):
        # Never flatten multiple text columns from the same physical line.
        lines=[line.strip() for line in page.splitlines() if line.strip()]
        paragraph=[]
        for line in lines+[""]:
            # Layout-style gaps indicate multiple columns or tables.
            bad=(bool(re.search(r"\S {5,}\S",line)) or
                 bool(re.search(r"\.{5,}",line)))
            if not line or bad:
                if paragraph:
                    cleaned=re.sub(r"\s+"," "," ".join(paragraph)).strip()
                    for chunk in re.split(r"(?<=[.!?])\s+(?=[A-Z(])",cleaned):
                        if 40<=len(chunk)<=850 and not re.search(r"\.{5,}",chunk):
                            yield page_no,chunk
                paragraph=[]
                continue
            paragraph.append(line)


def analyze(text):
    if len(text.strip())<10000: raise ValueError("original full-text source required")
    items={axis:[] for axis in AXES}
    seen=set()
    for page,chunk in sentences(text):
        fingerprint=re.sub(r"\W+","",chunk).lower()
        if fingerprint in seen: continue
        seen.add(fingerprint)
        if not SUBJECT.search(chunk): continue
        for axis,pattern in AXES.items():
            if re.search(pattern,chunk,re.I) and len(items[axis])<5:
                items[axis].append({"pdf_page":page,"verbatim_text":chunk,
                                    "status":"source_sentence_candidate_not_verified_entailment"})
    return {"sha256":hashlib.sha256(text.encode()).hexdigest(),"axes":items}

def compare(first,second):
    sources={"massive_star_core_collapse":analyze(first),"type_ia":analyze(second)}
    matrix={}
    for axis in AXES:
        a=sources["massive_star_core_collapse"]["axes"][axis]
        b=sources["type_ia"]["axes"][axis]
        matrix[axis]={"first_source_evidence":a,"second_source_evidence":b,
                      "coverage":"BOTH_SOURCES" if a and b else "INSUFFICIENT",
                      "agreement_or_conflict":"NOT_DETERMINED",
                      "reason":"Sentence-level co-occurrence is not scientific entailment."}
    return {"sources":sources,"comparison":matrix,
            "cross_paper_scientific_conclusion":"ABSTAIN_PENDING_SEMANTIC_REVIEW",
            "scientific_truth_verified":False,
            "limitations":["No semantic inference model or expert adjudication",
                           "No numeric yield comparison or normalization",
                           "No physical-origin inference about Earth's iron"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--core-collapse",required=True)
    p.add_argument("--type-ia",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    result=compare(Path(a.core_collapse).read_text(errors="replace"),
                   Path(a.type_ia).read_text(errors="replace"))
    Path(a.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("SCIENTIFIC_COMPARISON", {k:v["coverage"] for k,v in result["comparison"].items()},
          result["cross_paper_scientific_conclusion"],flush=True)

if __name__=="__main__":main()
