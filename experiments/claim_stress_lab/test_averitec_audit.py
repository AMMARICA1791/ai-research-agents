import unittest
from experiments.claim_stress_lab.averitec_audit import audit


class AVeriTeCAuditTests(unittest.TestCase):
    def test_source_urls_do_not_become_verified_quotes(self):
        rows = [{"claim": "An example", "label": "Refuted", "questions": [
            {"question": "Is it true?", "answers": [
                {"answer": "No", "source_url": "https://example.org/evidence"}]}]}]
        result = audit(rows)
        self.assertEqual(result["claims"], 1)
        self.assertEqual(result["answers_with_source_url"], 1)
        self.assertFalse(result["quote_text_verified"])
        self.assertFalse(result["independent_quote_defect_labels"])
        self.assertFalse(result["ready_for_claim_stress_evaluation"])

    def test_reject_invalid_dataset(self):
        with self.assertRaises(ValueError):
            audit({"claim": "wrong container"})


if __name__ == "__main__":
    unittest.main()
