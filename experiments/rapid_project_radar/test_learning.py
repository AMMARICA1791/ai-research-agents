import tempfile
import unittest
from pathlib import Path
from experiments.rapid_project_radar.learning import record, save

class LearningTests(unittest.TestCase):
    def test_failure_creates_reusable_lesson(self):
        first = record("test", "FAIL", "Assumption contradicted", "Change control group")
        second = record("test", "PASS", "Control group passed", previous=first["iterations"])
        self.assertEqual(len(second["iterations"]), 2)
        self.assertEqual(second["lessons"][0]["try_next"], "Change control group")
        self.assertFalse(second["automatic_code_changes"])

    def test_rejects_unsupported_outcome(self):
        with self.assertRaises(ValueError):
            record("test", "SUCCESSFUL_INVENTION", "unsupported")

    def test_persists_iterations(self):
        with tempfile.TemporaryDirectory() as directory:
            save(directory, "FAIL", "Test failed", "Review assumptions")
            result = save(directory, "INCONCLUSIVE", "Not enough data")
            self.assertEqual(len(result["iterations"]), 2)

if __name__ == "__main__":
    unittest.main()
