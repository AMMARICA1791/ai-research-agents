"""Evaluate all annotated SciFact dev rationale instances with real model inference."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from research.run_scifact_nli import MODEL_ID, DATA_URL, download_scifact, predict
from research.scifact_benchmark import benchmark_cases, evaluate


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    claims, corpus = download_scifact(out)
    cases = benchmark_cases(claims, corpus)
    if not cases:
        raise ValueError("SciFact dev has no annotated rationale cases")
    predictions = predict(cases)
    report = evaluate(cases, predictions)
    report.update({
        "model": MODEL_ID, "dataset": DATA_URL,
        "sample_method": "ALL annotated rationale instances in SciFact dev, no subsampling",
        "task": "gold-rationale conditional NLI, not evidence retrieval",
        "not_scientific_truth_validation": True,
    })
    lookup = {p["case_id"]: p["relation"] for p in predictions}
    errors = [
        {"case_id": c["case_id"], "doc_id": c["doc_id"], "claim": c["claim"],
         "quote": c["quote"], "gold": c["gold"], "predicted": lookup[c["case_id"]]}
        for c in cases if lookup[c["case_id"]] != c["gold"]
    ]
    report["error_breakdown"] = dict(sorted(Counter((e["gold"], e["predicted"]) for e in errors).items()))
    # JSON requires string keys; preserve full error pairs in the separate file.
    report["error_breakdown"] = [
        {"gold": gold, "predicted": predicted, "count": count}
        for (gold, predicted), count in sorted(Counter((e["gold"], e["predicted"]) for e in errors).items())
    ]
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "predictions.json").write_text(json.dumps(predictions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("SCIFACT_FULL_DEV_REPORT=" + json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
