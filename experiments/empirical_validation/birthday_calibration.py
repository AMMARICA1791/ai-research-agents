"""Empirical calibration: birthday-collision probability under uniform 365-day sampling.

Independent Monte Carlo measurements compared with an exact combinatorial result.
This validates the experiment pipeline, not a novel scientific discovery.
"""
import hashlib
import json
import random
from pathlib import Path
from experiments.empirical_validation.protocol import evaluate

ROOT = Path(__file__).resolve().parent
DATA = b"uniform-independent-birthdays|days=365|group=23|trials=20000|seeds=11,29,47|v1"
SEEDS = (11, 29, 47)
TRIALS = 20000
DAYS = 365
GROUP = 23

def exact_probability():
    no_collision = 1.0
    for i in range(GROUP):
        no_collision *= (DAYS - i) / DAYS
    return 1.0 - no_collision

def measure(seed):
    rng = random.Random(seed)
    collisions = 0
    for _ in range(TRIALS):
        birthdays = [rng.randrange(DAYS) for _ in range(GROUP)]
        collisions += len(set(birthdays)) < GROUP
    return collisions / TRIALS

def run():
    frozen = json.loads((ROOT / "preregistration.json").read_text(encoding="utf-8"))
    if frozen["data_sha256"] != hashlib.sha256(DATA).hexdigest():
        raise ValueError("frozen configuration digest mismatch")
    if frozen["expected_value"] != exact_probability():
        raise ValueError("theoretical target differs from frozen preregistration")
    results = [measure(seed) for seed in SEEDS]
    comparison = evaluate(frozen, results, DATA)
    comparison.update({
        "study": "birthday_paradox_calibration",
        "seeds": list(SEEDS),
        "trials_per_seed": TRIALS,
        "observed_rates": results,
        "theoretical_probability": exact_probability(),
        "interpretation": "Computational replication of an exact probability under explicitly idealized assumptions; not a real-world birth-date study.",
    })
    return comparison

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
