import unittest
from experiments.web_action_trust_lab.benchmark import evaluate

class BenchmarkTests(unittest.TestCase):
    def test_synthetic_cases(self):
        report=evaluate()
        self.assertEqual(report["dataset"],"synthetic_policy_smoke_only")
        self.assertEqual(report["n"],12)
        self.assertEqual(report["policy_correct"],12)
        self.assertEqual(report["baseline_correct"],4)
        self.assertIsNone(report["real_world_security_efficacy"])
        self.assertEqual(len(report["fixture_sha256"]),64)

if __name__ == "__main__":
    unittest.main()
