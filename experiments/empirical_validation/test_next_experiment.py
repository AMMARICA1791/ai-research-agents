import unittest
from experiments.empirical_validation.next_experiment import propose

def evidence(scores):
    return {
        "study": "fisher_iris_repeated_stratified_holdout",
        "splits": [{"model_accuracy": s, "baseline_accuracy": 1/3} for s in scores],
        "mean_accuracy": sum(scores) / len(scores),
        "min_accuracy": min(scores),
    }

class SuccessorPolicyTests(unittest.TestCase):
    def test_strong_internal_evidence_requests_external_validation(self):
        p = propose(evidence([.93, .97, 1., .97, 1.]))
        self.assertEqual(p["status"], "BLOCKED_PENDING_EXTERNAL_DATASET")
        self.assertIn("external", p["changed_design"])

    def test_weak_internal_evidence_requests_training_only_selection(self):
        p = propose(evidence([.7, .9, .9, .95, .96]))
        self.assertEqual(p["status"], "PROPOSED_NOT_EXECUTED")

    def test_inconsistent_evidence_rejected(self):
        e = evidence([.9] * 5)
        e["mean_accuracy"] = 1.
        with self.assertRaises(ValueError):
            propose(e)

    def test_missing_evidence_rejected(self):
        with self.assertRaises(ValueError):
            propose({"study": "fisher_iris_repeated_stratified_holdout"})

if __name__ == "__main__":
    unittest.main()
