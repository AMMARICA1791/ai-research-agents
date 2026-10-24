"""Holdout prediction experiment on the corrected Fisher Iris dataset.

Pre-registered stratified train/test split, dummy baseline and a linear
classifier. No test-set tuning or scientific novelty claim.
"""
import hashlib
import json
from pathlib import Path
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent

def run():
    p = json.loads((ROOT / "iris_holdout_preregistration.json").read_text(encoding="utf-8"))
    iris = load_iris()
    labels = iris.target_names
    canonical = ("\n".join(",".join([*(f"{v:.1f}" for v in row), labels[int(y)]])
                           for row, y in zip(iris.data, iris.target)) + "\n").encode()
    digest = hashlib.sha256(canonical).hexdigest()
    if digest != p["data_sha256"]:
        raise ValueError("dataset digest mismatch")
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=p["test_fraction"], random_state=p["split_seed"],
        stratify=iris.target)
    baseline = DummyClassifier(strategy="most_frequent")
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=p["model_seed"]))
    baseline.fit(X_train, y_train)
    model.fit(X_train, y_train)
    baseline_pred = baseline.predict(X_test)
    pred = model.predict(X_test)
    baseline_accuracy = float(accuracy_score(y_test, baseline_pred))
    accuracy = float(accuracy_score(y_test, pred))
    passed = accuracy >= p["minimum_holdout_accuracy"] and accuracy > baseline_accuracy
    return {
        "study": "fisher_iris_stratified_holdout",
        "data_sha256": digest,
        "train_count": len(y_train),
        "test_count": len(y_test),
        "baseline_accuracy": baseline_accuracy,
        "holdout_accuracy": accuracy,
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "split_seed": p["split_seed"],
        "model_seed": p["model_seed"],
        "status": "PASS" if passed else "FAIL",
        "scientific_scope": "Single fixed holdout; no confidence interval, external cohort, or original Fisher model replication.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
