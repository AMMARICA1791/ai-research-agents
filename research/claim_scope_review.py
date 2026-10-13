"""Conservative claim-level assessment against primary-paper text.

This evaluates whether the *paper states* a narrow claim, not whether nature
agrees. Unknown and broad claims abstain; no language model or fabricated quote.
"""
import argparse
import json
import re
from pathlib import Path

CLAIMS = {
    "paper_models_explosive_nucleosynthesis": {
        "require": (r"nucleosynthesis", r"(?:explosion|supernova|explosive)"),
        "claim": "The paper discusses nucleosynthesis in the context of stellar explosions.",
    },
    "paper_discusses_iron_group_yields": {
        "require": (r"iron[ -]group", r"(?:yield|production|synthesi)"),
        "claim": "The paper discusses production or yields of iron-group nuclei.",
    },
}
UNSUPPORTED = {
    "all_earth_iron_came_from_supernovae": "Requires multiple sources and solar-system geochemistry; cannot infer from a single supernova model paper.",
    "every_iron_atom_came_from_one_supernova": "Cannot trace individual atoms from this paper.",
    "quran_57_25_is_scientifically_proven": "Religious interpretation is outside the scientific-paper evidence domain.",
}

def judge(text):
    pages = text.split("\f")
    output = {}
    for key, spec in CLAIMS.items():
        found = []
        for page_number, page in enumerate(pages, 1):
            normalized = re.sub(r"\s+", " ", page).strip()
            # Search bounded windows; do not combine unrelated matches from far apart.
            for m in re.finditer(spec["require"][0], normalized, re.I):
                window = normalized[max(0,m.start()-170):min(len(normalized),m.end()+170)]
                if re.search(spec["require"][1], window, re.I):
                    found.append({"pdf_page": page_number, "exact_source_excerpt": window,
                                  "assessment": "topic_cooccurrence_not_semantic_entailment"})
                    break
            if len(found) >= 2:
                break
        output[key] = {"claim": spec["claim"], "verdict": "EVIDENCE_CANDIDATE_REQUIRES_SEMANTIC_REVIEW" if found else "INSUFFICIENT_EVIDENCE",
                       "evidence": found, "scientific_truth_verified": False}
    for key,reason in UNSUPPORTED.items():
        output[key] = {"verdict": "INSUFFICIENT_EVIDENCE", "reason": reason,
                       "evidence": [], "scientific_truth_verified": False}
    return {"assessment_type": "claim_scope_and_primary_source_evidence",
            "automatic_scientific_verification": False, "claims": output}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    text=Path(a.source).read_text(encoding="utf-8",errors="replace")
    report=judge(text)
    Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print("CLAIM_SCOPE_REVIEW", {k:v["verdict"] for k,v in report["claims"].items()},flush=True)

if __name__=="__main__":
    main()
