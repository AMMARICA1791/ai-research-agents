"""Two-primary-paper falsification gate; checks provenance and scientific scope.

Passing this gate proves two original texts were processed and compared at the
topic level. It does NOT certify semantic inference or physical truth.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

TOPICS = {
    "nucleosynthesis": r"nucleosynthesis",
    "iron_group": r"iron[ -]group|Fe.group",
    "model_dependence": r"uncertaint|sensitiv|depend|mass cut|electron capture",
}

def evidence(text, pattern):
    for number, page in enumerate(text.split("\f"), 1):
        normalized = re.sub(r"\s+", " ", page)
        match = re.search(pattern, normalized, re.I)
        if match:
            return {"pdf_page":number, "exact_excerpt":normalized[max(0,match.start()-100):match.end()+120]}
    return None

def compare(sources):
    if len(sources) != 2 or len(set(sources)) != 2:
        raise ValueError("two distinct primary sources required")
    output = {}
    for name, text in sources.items():
        if len(text.strip()) < 10000:
            raise ValueError(name+": insufficient original paper text")
        output[name]={"sha256":hashlib.sha256(text.encode()).hexdigest(),
                      "topics":{k:evidence(text,v) for k,v in TOPICS.items()}}
    overlap=[topic for topic in TOPICS if all(v["topics"][topic] for v in output.values())]
    return {"sources":output, "common_topics":overlap,
            "scope":"lexical comparison of two original paper text layers",
            "scientific_entailment":"NOT_TESTED",
            "independent_scientific_reasoning":"NOT_DEMONSTRATED",
            "verdict":"PROVENANCE_AND_TOPIC_COMPARISON_ONLY",
            "claim_all_earth_iron_from_supernovae":"NOT_ESTABLISHED"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--core-collapse",required=True)
    p.add_argument("--type-ia",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    sources={"Woosley_Weaver_1995":Path(a.core_collapse).read_text(errors="replace"),
             "Iwamoto_et_al_1999":Path(a.type_ia).read_text(errors="replace")}
    report=compare(sources)
    Path(a.output).write_text(json.dumps(report,indent=2)+"\n")
    print("TWO_PAPER_GATE",report["verdict"],"COMMON_TOPICS",report["common_topics"],flush=True)
    if not report["common_topics"]:
        raise SystemExit("NO_COMMON_SCIENTIFIC_TOPICS")

if __name__=="__main__":
    main()
