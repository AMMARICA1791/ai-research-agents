"""Select a reproducible, verdict-stratified AVeriTeC audit sample.

This outputs metadata only; verdict labels are NOT quote-defect labels.
"""
import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path


def select(records, count=30, seed=20261022):
    if not isinstance(records, list) or not records or not 0 < count <= len(records):
        raise ValueError("Expected a nonempty dataset and valid sample size")
    groups = defaultdict(list)
    for index, row in enumerate(records):
        if not isinstance(row, dict) or not isinstance(row.get("claim"), str):
            raise ValueError(f"Invalid claim at index {index}")
        groups[str(row.get("label", "MISSING"))].append(index)
    rng = random.Random(seed)
    selected = []
    keys = sorted(groups)
    for key in keys:
        rng.shuffle(groups[key])
    while len(selected) < count:
        progressed = False
        for key in keys:
            if groups[key] and len(selected) < count:
                selected.append(groups[key].pop())
                progressed = True
        if not progressed:
            break
    selected_counts = {key: sum(records[i].get("label", "MISSING") == key for i in selected) for key in keys}
    population_counts = {key: sum(records[i].get("label", "MISSING") == key for i in range(len(records))) for key in keys}
    return {"selection_method": "seeded_round_robin_by_claim_verdict",
            "population_size": len(records), "population_verdict_counts": population_counts,
            "sample_verdict_counts": selected_counts,
            "sample_is_population_representative": False,
            "seed": seed, "sample_size": len(selected),
            "selected_indices": selected,
            "claim_verdicts_not_quote_defect_labels": True,
            "independent_quote_labels": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    result = select(json.loads(raw), args.count, args.seed)
    result["source_sha256"] = hashlib.sha256(raw).hexdigest()
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
