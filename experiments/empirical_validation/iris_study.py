"""Reproduce a published Iris dataset property using the corrected scikit-learn copy.

Source: Fisher (1936), UCI DOI 10.24432/C56C76.
UCI warns its historical rows 35/38 differ from the corrected Fisher/R copy.
This study verifies dataset structure and setosa separability, NOT Fisher's
original discriminant-analysis performance or a newly discovered effect.
"""
import hashlib
import json
from pathlib import Path
from sklearn.datasets import load_iris

ROOT = Path(__file__).resolve().parent

def run():
    protocol = json.loads((ROOT / "iris_preregistration.json").read_text(encoding="utf-8"))
    iris = load_iris()
    labels = iris.target_names
    lines = [",".join([*(f"{v:.1f}" for v in row), labels[int(target)]])
             for row, target in zip(iris.data, iris.target)]
    canonical = ("\n".join(lines) + "\n").encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    if digest != protocol["data_sha256"]:
        raise ValueError("dataset version differs from frozen corrected-Iris snapshot")
    if protocol["dataset_variant"] != "sklearn_corrected_fisher":
        raise ValueError("wrong dataset variant")
    counts = {str(name): sum(int(t == i) for t in iris.target) for i, name in enumerate(labels)}
    # A transparent one-dimensional separator: Setosa has petal length < 2.0cm
    # while both other classes have petal length > 2.0cm in this fixed dataset.
    petal_lengths = iris.data[:, 2]
    predicted_setosa = petal_lengths < protocol["petal_length_threshold_cm"]
    actual_setosa = iris.target == 0
    accuracy = float((predicted_setosa == actual_setosa).mean())
    checks = {
        "rows_equal_150": len(lines) == 150,
        "four_features": iris.data.shape[1] == 4,
        "three_balanced_classes": counts == {"setosa": 50, "versicolor": 50, "virginica": 50},
        "setosa_separation": accuracy == protocol["expected_setosa_binary_accuracy"],
    }
    return {
        "study": "corrected_fisher_iris_dataset_property",
        "source_doi": "10.24432/C56C76",
        "data_sha256": digest,
        "rows": len(lines),
        "class_counts": counts,
        "petal_length_threshold_cm": protocol["petal_length_threshold_cm"],
        "observed_setosa_binary_accuracy": accuracy,
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scientific_scope": "In-sample property verification of corrected dataset, not out-of-sample prediction or original Fisher model reproduction.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
