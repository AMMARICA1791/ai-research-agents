"""Deterministic evidence-to-next-experiment proposal, with no LLM claims.

This bounded decision policy reads observed robustness results and proposes
a testable next step. It cannot independently discover hypotheses.
"""
import argparse
import json
from pathlib import Path

def propose(result):
    if result.get("study") != "fisher_iris_repeated_stratified_holdout":
        raise ValueError("unsupported evidence type")
    splits = result.get("splits")
    if not isinstance(splits, list) or len(splits) < 5:
        raise ValueError("missing repeated-holdout evidence")
    for split in splits:
        if not all(isinstance(split.get(k), (int, float)) and not isinstance(split.get(k), bool)
                   for k in ("model_accuracy", "baseline_accuracy")):
            raise ValueError("invalid split evidence")
    mean = result.get("mean_accuracy")
    minimum = result.get("min_accuracy")
    if not isinstance(mean, (int, float)) or not isinstance(minimum, (int, float)):
        raise ValueError("missing aggregate evidence")
    recomputed_mean = sum(s["model_accuracy"] for s in splits) / len(splits)
    recomputed_min = min(s["model_accuracy"] for s in splits)
    if abs(mean - recomputed_mean) > 1e-10 or abs(minimum - recomputed_min) > 1e-10:
        raise ValueError("inconsistent aggregate evidence")
    if minimum >= 0.90:
        change = "Replace overlapping holdouts with an independently sourced external dataset; preserve feature schema and fixed model pipeline."
        question = "Does the frozen Iris classifier retain accuracy >= 0.85 on an independently sourced, non-overlapping dataset?"
        reason = "All observed internal holdout accuracies were at least 0.90; the main unresolved risk is external generalization."
        status = "BLOCKED_PENDING_EXTERNAL_DATASET"
    else:
        change = "Use nested cross-validation to select regularization strength using training folds only."
        question = "Does training-only model selection improve the worst-fold accuracy without test leakage?"
        reason = "At least one observed holdout fell below 0.90; internal stability is not established."
        status = "PROPOSED_NOT_EXECUTED"
    return {
        "source_study": result["study"],
        "observed_mean_accuracy": mean,
        "observed_min_accuracy": minimum,
        "decision_rule": "minimum holdout accuracy >= 0.90",
        "reason": reason,
        "research_question": question,
        "changed_design": change,
        "status": status,
        "scientific_validation": "NOT_ESTABLISHED",
        "generation_method": "deterministic_evidence_conditioned_policy_not_autonomous_reasoning",
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    print(json.dumps(propose(json.loads(Path(args.evidence).read_text(encoding="utf-8"))), indent=2, sort_keys=True))
