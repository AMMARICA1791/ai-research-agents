"""Evaluate mechanically detectable defects on a separately labeled JSON dataset.

This does NOT evaluate semantic entailment; labels must be assigned independently.
Usage: python -m experiments.claim_stress_lab.evaluate_dataset --input labels.json
"""
import argparse
import json
from pathlib import Path
from experiments.claim_stress_lab.lab import evaluate

MECHANICAL_FLAGS = {"QUOTE_NOT_VERBATIM_IN_SOURCE", "CLAIM_NUMBERS_ABSENT_FROM_QUOTE"}


def metrics(tp, fp, fn, tn):
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall": tp / (tp + fn) if tp + fn else None,
        "false_positive_rate": fp / (fp + tn) if fp + tn else None,
    }


def assess(records):
    if not isinstance(records, list) or not records:
        raise ValueError("Expected a nonempty JSON array")
    seen = set()
    counts = {"lab": [0, 0, 0, 0], "exact_quote_only": [0, 0, 0, 0]}
    rows = []
    for record in records:
        if not isinstance(record, dict) or type(record.get("defect_label")) is not bool:
            raise ValueError("Each record requires an independent boolean defect_label")
        ident = record.get("id")
        if not isinstance(ident, str) or not ident.strip() or ident in seen:
            raise ValueError("Each record requires a unique nonempty string id")
        seen.add(ident)
        result = evaluate(record)
        truth = record["defect_label"]
        predictions = {
            "lab": bool(MECHANICAL_FLAGS.intersection(result["flags"])),
            "exact_quote_only": not result["quote_present"],
        }
        for method, predicted in predictions.items():
            # TP, FP, FN, TN
            idx = 0 if predicted and truth else 1 if predicted else 2 if truth else 3
            counts[method][idx] += 1
        rows.append({"id": ident, "defect_label": truth, "predictions": predictions, "flags": result["flags"]})
    return {
        "n": len(rows),
        "label_scope": "independently_labeled_mechanical_citation_defect",
        "lab": metrics(*counts["lab"]),
        "exact_quote_only": metrics(*counts["exact_quote_only"]),
        "semantic_accuracy": None,
        "publication_allowed": False,
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = assess(json.loads(args.input.read_text(encoding="utf-8")))
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
