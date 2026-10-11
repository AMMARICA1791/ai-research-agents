"""SciFact dev-set adapter and honest SUPPORT/CONTRADICT class-level scoring.

Does not treat missing annotated evidence as a gold 'insufficient' or 'out_of_scope'.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

LABELS = ("supports", "contradicts")


def load_jsonl(path):
    with Path(path).open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def benchmark_cases(claims_path, corpus_path):
    corpus = {str(doc["doc_id"]): doc for doc in load_jsonl(corpus_path)}
    cases = []
    for claim in load_jsonl(claims_path):
        for doc_id, rationales in claim.get("evidence", {}).items():
            if not rationales:
                continue
            doc = corpus.get(str(doc_id))
            if doc is None:
                raise ValueError("Missing corpus document: " + str(doc_id))
            sentences = doc["abstract"]
            for index, rationale in enumerate(rationales):
                gold = {"SUPPORT": "supports", "CONTRADICT": "contradicts"}[rationale["label"]]
                indices = rationale["sentences"]
                if not indices or any(not isinstance(i, int) or i < 0 or i >= len(sentences) for i in indices):
                    raise ValueError("Invalid rationale indices")
                cases.append({
                    "case_id": f'{claim["id"]}:{doc_id}:{index}',
                    "claim": claim["claim"],
                    "quote": " ".join(sentences[i] for i in indices),
                    "gold": gold,
                    "doc_id": str(doc_id),
                    "sentence_indices": indices,
                })
    return cases


def evaluate(cases, predictions):
    predictions = list(predictions)
    indexed = {}
    for row in predictions:
        case_id = row["case_id"]
        if case_id in indexed:
            raise ValueError("Duplicate prediction")
        label = row.get("relation")
        if label is not None and label not in ("supports", "contradicts", "insufficient", "out_of_scope"):
            raise ValueError("Invalid prediction label")
        indexed[case_id] = label
    ids = {x["case_id"] for x in cases}
    if set(indexed) - ids:
        raise ValueError("Unknown case in predictions")
    matrix = {gold: {pred: 0 for pred in (*LABELS, "insufficient", "out_of_scope", "abstain")}
              for gold in LABELS}
    for case in cases:
        matrix[case["gold"]][indexed.get(case["case_id"]) or "abstain"] += 1
    metrics = {}
    for label in LABELS:
        tp = matrix[label][label]
        actual = sum(matrix[label].values())
        predicted = sum(matrix[gold][label] for gold in LABELS)
        precision = tp / predicted if predicted else None
        recall = tp / actual if actual else None
        f1 = 2 * precision * recall / (precision + recall) if precision is not None and recall is not None and precision + recall else None
        metrics[label] = {"support": actual, "true_positive": tp, "false_positive": predicted - tp,
                          "false_negative": actual - tp, "precision": precision, "recall": recall, "f1": f1}
    return {"benchmark": "SciFact", "gold_classes": list(LABELS), "n": len(cases),
            "per_class": metrics, "confusion_matrix": matrix,
            "coverage": sum(indexed.get(x["case_id"]) is not None for x in cases) / len(cases) if cases else None,
            "accuracy": sum(matrix[label][label] for label in LABELS) / len(cases) if cases else None,
            "other_classes_have_gold_labels": False}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", required=True)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--cases-output", required=True)
    parser.add_argument("--predictions")
    parser.add_argument("--report-output")
    args = parser.parse_args(argv)
    cases = benchmark_cases(args.claims, args.corpus)
    Path(args.cases_output).write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.predictions:
        if not args.report_output:
            parser.error("--report-output required with --predictions")
        report = evaluate(cases, load_jsonl(args.predictions))
        Path(args.report_output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "gold_labels": dict(Counter(x["gold"] for x in cases))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
