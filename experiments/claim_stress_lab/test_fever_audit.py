import json
import tempfile
import unittest
from pathlib import Path
from experiments.claim_stress_lab.fever_audit import audit


class FeverAuditTests(unittest.TestCase):
    def test_claim_labels_are_not_misused_as_quote_labels(self):
        sample = {"id": 1, "label": "REFUTES", "claim": "An invented claim",
                  "evidence": [[[0, 0, "Example_Page", 3]]]}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.jsonl"
            path.write_text(json.dumps(sample) + "\n", encoding="utf-8")
            result = audit(path)
        self.assertEqual(result["claims_read"], 1)
        self.assertEqual(result["claim_labels"], {"REFUTES": 1})
        self.assertEqual(result["sample_references"][0]["evidence_references"][0]["sentence_id"], 3)
        self.assertFalse(result["quote_text_resolved"])
        self.assertFalse(result["independent_quote_defect_labels"])
        self.assertFalse(result["ready_for_claim_stress_evaluation"])


if __name__ == "__main__":
    unittest.main()
