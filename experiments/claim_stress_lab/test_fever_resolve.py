import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from experiments.claim_stress_lab.fever_resolve import resolve


class FeverResolveTests(unittest.TestCase):
    def test_resolves_only_referenced_sentences(self):
        with tempfile.TemporaryDirectory() as folder:
            claims = Path(folder) / "claims.jsonl"
            wiki = Path(folder) / "wiki.zip"
            claim = {"id": 1, "claim": "A claim", "label": "SUPPORTS",
                     "evidence": [[[0, 0, "Test_Page", 1]]]}
            claims.write_text(json.dumps(claim) + "\n", encoding="utf-8")
            page = {"id": "Test_Page", "lines": "0\tOther text\n1\tVerified source sentence"}
            with zipfile.ZipFile(wiki, "w") as archive:
                archive.writestr("wiki-pages/wiki-001.jsonl", json.dumps(page) + "\n")
            result = resolve(claims, wiki, 1)
        self.assertEqual(result["requested_references"], 1)
        self.assertEqual(result["resolved_references"], 1)
        self.assertEqual(result["references"][0]["source_text"], "Verified source sentence")
        self.assertFalse(result["quote_defect_labels_available"])
        self.assertFalse(result["ready_for_independent_evaluation"])


if __name__ == "__main__":
    unittest.main()
