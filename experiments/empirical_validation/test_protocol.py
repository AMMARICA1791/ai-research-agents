import hashlib
import unittest
from experiments.empirical_validation.protocol import evaluate

DATA = b"fixed-public-dataset-placeholder"
BASE = {
    "claim": "Demonstration only: measured value is near published target",
    "metric": "example_score",
    "expected_value": 0.8,
    "tolerance": 0.05,
    "data_sha256": hashlib.sha256(DATA).hexdigest(),
    "protocol_version": "1",
}

class ProtocolTests(unittest.TestCase):
    def test_within_tolerance_is_not_scientific_proof(self):
        result = evaluate(BASE, [0.79, 0.80, 0.81], DATA)
        self.assertEqual(result["empirical_comparison"], "WITHIN_PREDECLARED_TOLERANCE")
        self.assertEqual(result["scientific_validation"], "NOT_ESTABLISHED_BY_THIS_COMPARISON")

    def test_disagreement_preserved(self):
        result = evaluate(BASE, [0.60, 0.61, 0.62], DATA)
        self.assertEqual(result["empirical_comparison"], "OUTSIDE_PREDECLARED_TOLERANCE")

    def test_changed_data_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(BASE, [0.8] * 3, b"changed")

    def test_insufficient_replicates_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(BASE, [0.8, 0.8], DATA)

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(BASE, [0.8, float("nan"), 0.8], DATA)

if __name__ == "__main__":
    unittest.main()
