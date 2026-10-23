import unittest
from experiments.claim_stress_lab.averitec_sample import select


class AVeriTeCSampleTests(unittest.TestCase):
    def test_deterministic_and_balanced(self):
        records = ([{"claim": str(i), "label": "Supported"} for i in range(20)] +
                   [{"claim": str(i), "label": "Refuted"} for i in range(20, 40)])
        a = select(records, count=10, seed=42)
        b = select(records, count=10, seed=42)
        self.assertEqual(a, b)
        self.assertEqual(len(set(a["selected_indices"])), 10)
        self.assertEqual(sum(i < 20 for i in a["selected_indices"]), 5)
        self.assertFalse(a["independent_quote_labels"])

    def test_reject_invalid_sample(self):
        with self.assertRaises(ValueError):
            select([{"claim": "x", "label": "Supported"}], count=2)


if __name__ == "__main__":
    unittest.main()
