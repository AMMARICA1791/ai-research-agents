"""Run a genuine public NLI model on SciFact dev rationales (CPU, no API key).

This evaluates relation classification with gold evidence provided (not retrieval).
"""
from __future__ import annotations

import argparse
import json
import tarfile
import urllib.request
from pathlib import Path

from research.scifact_benchmark import benchmark_cases, evaluate

DATA_URL = "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz"
MODEL_ID = "cross-encoder/nli-MiniLM2-L6-H768"


def download_scifact(destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / "scifact-data.tar.gz"
    urllib.request.urlretrieve(DATA_URL, archive)
    with tarfile.open(archive, "r:gz") as tf:
        wanted = {"data/corpus.jsonl", "data/claims_dev.jsonl"}
        members = [m for m in tf.getmembers() if m.name.lstrip("./") in wanted]
        if len(members) != 2 or any(not m.isfile() for m in members):
            raise ValueError("Expected SciFact corpus and dev claims not present")
        for member in members:
            target = destination / Path(member.name).name
            with tf.extractfile(member) as src, target.open("wb") as dst:
                import shutil
                shutil.copyfileobj(src, dst)
    return destination / "claims_dev.jsonl", destination / "corpus.jsonl"


def predict(cases, model_id=MODEL_ID):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    torch.set_num_threads(2)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id).eval()
    labels = {int(k): str(v).lower() for k, v in model.config.id2label.items()}
    expected = {"contradiction", "entailment", "neutral"}
    if set(labels.values()) != expected:
        raise ValueError(f"Unknown model label semantics: {labels}; refusing to guess")
    result = []
    for case in cases:
        tokens = tokenizer(case["quote"], case["claim"], return_tensors="pt",
                           truncation=True, max_length=512)
        with torch.inference_mode():
            predicted = int(model(**tokens).logits.argmax(-1).item())
        semantic = labels[predicted]
        relation = {"entailment": "supports", "contradiction": "contradicts",
                    "neutral": "insufficient"}[semantic]
        result.append({"case_id": case["case_id"], "relation": relation})
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= 500:
        parser.error("--limit must be between 1 and 500")
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    claims, corpus = download_scifact(out)
    all_cases = benchmark_cases(claims, corpus)
    # Deterministic, class-balanced sampling using only published gold labels.
    positives = [c for c in all_cases if c["gold"] == "supports"]
    negatives = [c for c in all_cases if c["gold"] == "contradicts"]
    half = args.limit // 2
    selected = positives[:half] + negatives[:args.limit - half]
    if len(selected) != args.limit:
        raise ValueError("Insufficient gold examples for requested sample")
    preds = predict(selected)
    report = evaluate(selected, preds)
    report["model"] = MODEL_ID
    report["dataset"] = DATA_URL
    report["sample_method"] = "first N rationale records per gold class, nonrandom, dev only"
    report["task"] = "gold-rationale conditional relation classification (not end-to-end retrieval)"
    report["sample_size"] = len(selected)
    report["not_scientific_truth_validation"] = True
    (out / "predictions.json").write_text(json.dumps(preds, indent=2) + "\n", encoding="utf-8")
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("SCIFACT_REAL_NLI_REPORT=" + json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
