import json
import tempfile
import unittest
from pathlib import Path
from scripts.island_release_gate import assess

class ReleaseGateTests(unittest.TestCase):
    def test_rejects_generic_authorization_code_for_privacy(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "hypothesis.json").write_text(json.dumps({"topic": "privacy"}))
            (p / "prototype.py").write_text("def evaluate(value): return True\n")
            (p / "test_prototype.py").write_text("def test_anything(): pass\n")
            self.assertFalse(assess(p)[0])

    def test_accepts_source_claim_as_unvalidated_experiment(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "hypothesis.json").write_text(json.dumps({"topic": "source_claim"}))
            (p / "prototype.py").write_text("def evidence_matches(value): return True\n")
            (p / "test_prototype.py").write_text("def test_anything(): pass\n")
            self.assertTrue(assess(p)[0])

    def test_accepts_experimental_template_without_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "hypothesis.json").write_text(json.dumps({"topic": "privacy"}))
            (p / "prototype.py").write_text("def redact(value): return value\n")
            (p / "test_prototype.py").write_text("def test_anything(): pass\n")
            self.assertTrue(assess(p)[0])

    def test_accepts_reviewed_evidence_structure_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "hypothesis.json").write_text(json.dumps({"topic": "privacy"}))
            (p / "prototype.py").write_text("def redact(value): return value\n")
            (p / "test_prototype.py").write_text("def test_anything(): pass\n")
            (p / "VALIDATION.json").write_text(json.dumps({"independent_validation": True, "review_status": "approved", "evidence": ["reviewed:test-case-1"]}))
            self.assertTrue(assess(p)[0])

if __name__ == "__main__":
    unittest.main()
