"""Adversarial probes: expose semantic errors that lexical checks cannot establish.

These cases are synthetic diagnostic counterexamples, NOT independently reviewed
real-world validation. A flag is only a review cue; absence of flags is not proof.
"""
import json
from experiments.claim_stress_lab.lab import evaluate

PROBES = [
    {
        "id": "negation-reversal",
        "claim": "The treatment increased mortality",
        "quote": "The treatment did not increase mortality",
        "source_text": "The treatment did not increase mortality",
        "source_url": "https://example.org/synthetic-negation",
        "expected_semantic_problem": True,
    },
    {
        "id": "association-to-causation",
        "claim": "Coffee consumption caused lower risk",
        "quote": "Coffee consumption was associated with lower risk",
        "source_text": "Coffee consumption was associated with lower risk",
        "source_url": "https://example.org/synthetic-causality",
        "expected_semantic_problem": True,
    },
    {
        "id": "supported-verbatim",
        "claim": "The trial included 120 participants",
        "quote": "The trial included 120 participants",
        "source_text": "The trial included 120 participants",
        "source_url": "https://example.org/synthetic-control",
        "expected_semantic_problem": False,
    },
]


def probe_report():
    rows = []
    for record in PROBES:
        result = evaluate(record)
        rows.append({
            "id": record["id"],
            "expected_semantic_problem": record["expected_semantic_problem"],
            "mechanical_flags": result["flags"],
            "mechanical_defect_detected": bool(set(result["flags"]) & {
                "QUOTE_NOT_VERBATIM_IN_SOURCE", "CLAIM_NUMBERS_ABSENT_FROM_QUOTE"
            }),
            "semantic_accuracy": result["semantic_accuracy"],
        })
    return {
        "dataset": "synthetic_adversarial_probes_not_validation",
        "n": len(rows),
        "publication_allowed": False,
        "rows": rows,
    }


if __name__ == "__main__":
    print(json.dumps(probe_report(), indent=2))
