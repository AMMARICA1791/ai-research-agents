"""Transparent per-class model evaluation from independently reviewed labels.

No synthetic cases are presented as real-world benchmark results.
"""
from __future__ import annotations

from research.ai_entailment_triage import score_against_human
from research.relationship_review import RELATIONS


def per_class_report(payload: dict, source_dir, predictions: dict) -> dict:
    scored = score_against_human(payload, source_dir, predictions)
    rows = scored["evaluations"]
    labels = sorted(RELATIONS)
    matrix = {gold: {pred: 0 for pred in labels + ["abstain"]} for gold in labels}
    for row in rows:
        matrix[row["human_label"]][row["model_label"] or "abstain"] += 1
    per_class = {}
    for label in labels:
        tp = matrix[label][label]
        support = sum(matrix[label].values())
        predicted = sum(matrix[g][label] for g in labels)
        precision = tp / predicted if predicted else None
        recall = tp / support if support else None
        f1 = (2 * precision * recall / (precision + recall)
              if precision is not None and recall is not None and precision + recall else None)
        per_class[label] = {
            "support": support, "predicted": predicted, "true_positive": tp,
            "false_positive": predicted - tp, "false_negative": support - tp,
            "precision": precision, "recall": recall, "f1": f1,
        }
    eligible = [x["f1"] for x in per_class.values() if x["f1"] is not None]
    return {
        "status": "per_class_human_annotation_comparison",
        "reviewed_count": scored["reviewed_count"],
        "accuracy": scored["accuracy"],
        "coverage": scored["coverage"],
        "confusion_matrix": matrix,
        "per_class": per_class,
        "macro_f1_observed_classes": sum(eligible) / len(eligible) if eligible else None,
        "macro_f1_note": "Mean over classes with defined F1 only; absent classes excluded",
        "scientific_validity_established": False,
        "human_labels_independently_verified": False,
    }


def main(argv=None):
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Per-class evidence relation metrics")
    parser.add_argument("--input", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    predictions = json.loads(Path(args.predictions).read_text(encoding="utf-8"))
    report = per_class_report(payload, args.source_dir, predictions)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, sort_keys=True, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"reviewed_count": report["reviewed_count"],
                      "per_class": report["per_class"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
