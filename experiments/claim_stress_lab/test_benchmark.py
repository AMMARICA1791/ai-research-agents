import unittest
from experiments.claim_stress_lab.benchmark import report


class BenchmarkTests(unittest.TestCase):
    def test_synthetic_baseline_is_explicitly_bounded(self):
        result = report()
        self.assertEqual(result["dataset"], "synthetic_smoke_only")
        self.assertEqual(result["n"], 4)
        self.assertEqual(result["true_positive"], 2)
        self.assertEqual(result["false_positive"], 0)
        self.assertEqual(result["false_negative"], 0)
        self.assertEqual(result["precision"], 1.0)
        self.assertEqual(result["recall"], 1.0)
        baseline = result["baseline_exact_quote_only"]\n        self.assertEqual(baseline["true_positive"], 1)\n        self.assertEqual(baseline["false_negative"], 1)\n        self.assertEqual(baseline["false_positive"], 0)\n        self.assertIsNone(result["semantic_accuracy"])
        self.assertFalse(result["publication_allowed"])


if __name__ == "__main__":
    unittest.main()
