"""Repeated stratified holdout robustness check on corrected Fisher Iris data.

Protocol fixes split seeds and metric before workflow execution. Multiple
holdouts reuse observations and are not independent external replications.
"""
import hashlib
import json
from pathlib import Path
from statistics import mean, stdev
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent

def run():
    p = json.loads((ROOT / "iris_robustness_preregistration.json").read_text(encoding="utf-8"))
    iris = load_iris()
    canonical = ("\n".join(",".join([*(f"{v:.1f}" for v in row), iris.target_names[int(y)]])
                           for row, y in zip(iris.data, iris.target)) + "\n").encode()
    if hashlib.sha256(canonical).hexdigest() != p["data_sha256"]:
        raise ValueError("dataset digest mismatch")
    observations = []
    for seed in p["split_seeds"]:
        X_train, X_test, y_train, y_test = train_test_split(
            iris.data, iris.target, test_size=p["test_fraction"],
            random_state=seed, stratify=iris.target)
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=p["model_seed"]))
        baseline = DummyClassifier(strategy="most_frequent")
        model.fit(X_train, y_train)
        baseline.fit(X_train, y_train)
        observations.append({
            "split_seed": seed,
            "model_accuracy": float(accuracy_score(y_test, model.predict(X_test))),
            "baseline_accuracy": float(accuracy_score(y_test, baseline.predict(X_test))),
            "test_count": len(y_test),
        })
    model_scores = [v["model_accuracy"] for v in observations]
    baseline_scores = [v["baseline_accuracy"] for v in observations]
    avg = mean(model_scores)
    minimum = min(model_scores)
    improvement = mean(model_scores) - mean(baseline_scores)
    passed = avg >= p["minimum_mean_accuracy"] and minimum >= p["minimum_single_split_accuracy"] and improvement > 0
    return {
        "study": "fisher_iris_repeated_stratified_holdout",
        "splits": observations,
        "mean_accuracy": avg,
        "sample_standard_deviation": stdev(model_scores),
        "min_accuracy": minimum,
        "max_accuracy": max(model_scores),
        "mean_baseline_accuracy": mean(baseline_scores),
        "mean_improvement_over_baseline": improvement,
        "status": "PASS" if passed else "FAIL",
        "scientific_scope": "Repeated overlapping holdouts of one small published dataset; not external validation or independent replicates.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
