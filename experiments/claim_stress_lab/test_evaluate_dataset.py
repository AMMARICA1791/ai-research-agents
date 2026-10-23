import unittest
from experiments.claim_stress_lab.evaluate_dataset import assess


def record(ident, claim, quote, source, defect):
    return {"id": ident, "claim": claim, "quote": quote,
            "source_text": source, "source_url": "https://example.org/source",
            "defect_label": defect}


class IndependentDatasetTests(unittest.TestCase):
    def test_comparison_and_denominators(self):
        rows = [
            record("a", "The count is 500", "The count is 50", "The count is 50", True),
            record("b", "The count is 50", "The count is 50", "The count is 50", False),
            record("c", "The count is 50", "The count is 50", "Other text", True),
            record("d", "The count is 50", "The count is 50", "The count is 50", False),
        ]
        result = assess(rows)
        self.assertEqual(result["n"], 4)
        self.assertEqual(result["lab"]["tp"], 2)
        self.assertEqual(result["lab"]["tn"], 2)
        self.assertEqual(result["exact_quote_only"]["tp"], 1)
        self.assertEqual(result["exact_quote_only"]["fn"], 1)
        self.assertIsNone(result["semantic_accuracy"])
        self.assertFalse(result["publication_allowed"])

    def test_rejects_unlabeled_and_duplicate_records(self):
        a = record("a", "Count 2", "Count 2", "Count 2", False)
        with self.assertRaises(ValueError):
            assess([{k: v for k, v in a.items() if k != "defect_label"}])
        with self.assertRaises(ValueError):
            assess([a, a])
        with self.assertRaises(ValueError):
            assess([])


if __name__ == "__main__":
    unittest.main()
