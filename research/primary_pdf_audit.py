"""Deterministic, page-aware evidence candidates from a primary PDF text layer.

This does NOT infer scientific truth, and does NOT use a language model.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

PATTERNS = {
    "explosion_models": r"\b78\b.{0,110}\b(?:model|explosion|supernova)",
    "nucleosynthesis": r"\bnucleosynthesis\b",
    "iron_group": r"\biron[- ]group\b|\b(?:iron|nickel)[ -]?(?:isotopes|yields)\b",
    "model_uncertainty": r"\b(?:uncertaint\w*|sensitive|sensitivity|fallback|mass cut)\b",
}

def extract(text):
    if len(text.strip()) < 500:
        raise ValueError("insufficient PDF text layer")
    pages = text.split("\f")
    results = {}
    for key, pattern in PATTERNS.items():
        found = []
        for page_no, page in enumerate(pages, 1):
            normalized = re.sub(r"\s+", " ", page).strip()
            for match in re.finditer(pattern, normalized, re.I):
                start = max(0, match.start() - 95)
                end = min(len(normalized), match.end() + 120)
                found.append({"pdf_page": page_no, "excerpt": normalized[start:end],
                              "matched_text": match.group(0),
                              "status": "text_match_only_not_fact_verified"})
                if len(found) >= 3:
                    break
            if len(found) >= 3:
                break
        results[key] = found
    return {"source_scope": "full_pdf_extracted_text",
            "scientific_truth_verified": False,
            "extraction_method": "deterministic_keyword_context_no_model",
            "pdf_pages_detected": len(pages), "characters": len(text),
            "candidates": results,
            "missing_categories": [k for k,v in results.items() if not v]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    path = Path(args.source)
    data = extract(path.read_text(encoding="utf-8", errors="replace"))
    data["source_text_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print("SOURCE_TEXT_AUDIT", {k:len(v) for k,v in data["candidates"].items()},
          "PAGES", data["pdf_pages_detected"], flush=True)

if __name__ == "__main__":
    main()
