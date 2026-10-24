"""Evidence-linked successor: does increasing group size from 23 to 30 raise collisions?

The predecessor's measured result is explicitly recorded as the reason to test
sensitivity to group size. This is a controlled numerical study, not autonomous
scientific reasoning or a new discovery.
"""
import hashlib
import json
import random
from pathlib import Path
from experiments.empirical_validation.protocol import evaluate

ROOT = Path(__file__).resolve().parent
SEEDS = (11, 29, 47)
TRIALS = 20000
DAYS = 365
BASE_GROUP = 23
NEW_GROUP = 30
DATA = b"birthday-sensitivity|days=365|baseline=23|intervention=30|trials=20000|seeds=11,29,47|v1"

def exact(group):
    remaining = 1.0
    for i in range(group):
        remaining *= (DAYS - i) / DAYS
    return 1 - remaining

def paired_measure(seed):
    rng = random.Random(seed)
    base_count = 0
    new_count = 0
    for _ in range(TRIALS):
        birthdays = [rng.randrange(DAYS) for _ in range(NEW_GROUP)]
        base_count += len(set(birthdays[:BASE_GROUP])) < BASE_GROUP
        new_count += len(set(birthdays)) < NEW_GROUP
    return base_count / TRIALS, new_count / TRIALS

def run():
    frozen = json.loads((ROOT / "successor_preregistration.json").read_text(encoding="utf-8"))
    if frozen["data_sha256"] != hashlib.sha256(DATA).hexdigest():
        raise ValueError("successor configuration digest mismatch")
    if abs(frozen["expected_value"] - (exact(NEW_GROUP) - exact(BASE_GROUP))) > 1e-12:
        raise ValueError("theoretical contrast differs from frozen protocol")
    pairs = [paired_measure(seed) for seed in SEEDS]
    differences = [new - base for base, new in pairs]
    result = evaluate(frozen, differences, DATA)
    result.update({
        "study": "birthday_group_size_successor",
        "predecessor_run": "https://github.com/AMMARICA1791/ai-research-agents/actions/runs/40051552147",
        "predecessor_observed_mean": 0.5052333333333333,
        "rationale": "The predecessor agreed with the exact probability within preregistered tolerance; next test sensitivity to group size with paired draws.",
        "baseline_group_size": BASE_GROUP,
        "new_group_size": NEW_GROUP,
        "seeds": list(SEEDS),
        "trials_per_seed": TRIALS,
        "paired_rates": [{"baseline": b, "intervention": n} for b, n in pairs],
        "observed_differences": differences,
        "theoretical_difference": exact(NEW_GROUP) - exact(BASE_GROUP),
        "scientific_scope": "Idealized mathematical model only; independent reproduction and literature replication not established.",
    })
    return result

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
