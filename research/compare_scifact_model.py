"""Compare a second evidence-oriented NLI model on exactly SciFact dev gold rationales."""
import json
from collections import Counter
from pathlib import Path

from research.run_scifact_nli import download_scifact, predict
from research.scifact_benchmark import benchmark_cases, evaluate

MODEL = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
BASELINE = {
    "model": "cross-encoder/nli-MiniLM2-L6-H768",
    "n": 338,
    "accuracy": 104 / 338,
    "confusion_matrix": {
        "supports": {"supports": 46, "contradicts": 18, "insufficient": 152},
        "contradicts": {"supports": 3, "contradicts": 58, "insufficient": 61},
    },
}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    claims, corpus = download_scifact(out)
    cases = benchmark_cases(claims, corpus)
    if len(cases) != BASELINE["n"]:
        raise ValueError(f"Benchmark drift: expected {BASELINE['n']}, got {len(cases)}")
    predictions = predict(cases, model_id=MODEL)
    report = evaluate(cases, predictions)
    report["model"] = MODEL
    report["baseline"] = BASELINE
    report["accuracy_delta_percentage_points"] = 100 * (report["accuracy"] - BASELINE["accuracy"])
    report["scope"] = "SciFact dev all gold rationale instances, NOT end-to-end retrieval"
    indexed = {p["case_id"]: p["relation"] for p in predictions}
    errors = [
        {"case_id": c["case_id"], "claim": c["claim"], "quote": c["quote"],
         "gold": c["gold"], "predicted": indexed[c["case_id"]]}
        for c in cases if indexed[c["case_id"]] != c["gold"]
    ]
    report["error_breakdown"] = [
        {"gold": gold, "predicted": pred, "count": count}
        for (gold, pred), count in sorted(Counter((e["gold"], e["predicted"]) for e in errors).items())
    ]
    for name, data in (("report.json", report), ("errors.json", errors),
                       ("predictions.json", predictions)):
        (out / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("SCIFACT_MODEL_COMPARISON=" + json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
