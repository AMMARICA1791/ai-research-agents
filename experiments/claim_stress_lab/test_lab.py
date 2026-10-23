import unittest
from experiments.claim_stress_lab.lab import evaluate


class ClaimStressTests(unittest.TestCase):
    def sample(self, **overrides):
        record = dict(id="a", claim="Revenue was 500", quote="Revenue was 50",
                      source_text="Revenue was 50 in the excerpt.",
                      source_url="https://example.org/a")
        record.update(overrides)
        return record

    def test_mismatched_number_is_flagged(self):
        result = evaluate(self.sample())
        self.assertIn("CLAIM_NUMBERS_ABSENT_FROM_QUOTE", result["flags"])
        self.assertFalse(result["publication_allowed"])
        self.assertIsNone(result["semantic_accuracy"])

    def test_missing_quote_is_flagged(self):
        result = evaluate(self.sample(quote="Revenue was 99"))
        self.assertIn("QUOTE_NOT_VERBATIM_IN_SOURCE", result["flags"])

    def test_ablation_removes_one_quote(self):
        result = evaluate(self.sample(claim="Revenue was 50"))
        self.assertTrue(result["quote_present"])
        self.assertLess(result["ablated_source_overlap"], result["claim_quote_overlap"])

    def test_no_claim_is_automatically_approved(self):
        result = evaluate(self.sample(claim="Revenue was 50"))
        self.assertTrue(result["review_required"])
        self.assertFalse(result["publication_allowed"])


if __name__ == "__main__":
    unittest.main()
