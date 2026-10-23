import unittest
from experiments.claim_stress_lab.adversarial_probes import probe_report


class AdversarialProbeTests(unittest.TestCase):
    def test_semantic_blind_spots_are_not_misreported_as_success(self):
        report = probe_report()
        self.assertEqual(report["dataset"], "synthetic_adversarial_probes_not_validation")
        self.assertEqual(report["n"], 3)
        by_id = {row["id"]: row for row in report["rows"]}
        for ident in ("negation-reversal", "association-to-causation"):
            self.assertTrue(by_id[ident]["expected_semantic_problem"])
            self.assertFalse(by_id[ident]["mechanical_defect_detected"])
            self.assertIsNone(by_id[ident]["semantic_accuracy"])
        self.assertFalse(report["publication_allowed"])


if __name__ == "__main__":
    unittest.main()
