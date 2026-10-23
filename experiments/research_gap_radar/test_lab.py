import unittest
from experiments.research_gap_radar.lab import assess,evaluate

class RadarTests(unittest.TestCase):
    def test_complete_measurable(self):
        x=dict(hypothesis="X",falsifiable_prediction="error rate falls 10%",
               experiment="run blinded test",baseline="simple control",prior_art="paper A")
        r=assess(x)
        self.assertTrue(r["ready_for_human_review"])
        self.assertFalse(r["novelty_verified"])
    def test_missing_baseline(self):
        r=assess({"hypothesis":"X"})
        self.assertIn("baseline",r["missing_fields"])
        self.assertFalse(r["ready_for_human_review"])
    def test_unquantified(self):
        r=assess(dict(hypothesis="X",falsifiable_prediction="improves",
                      experiment="try",baseline="other",prior_art="paper"))
        self.assertFalse(r["ready_for_human_review"])
    def test_empty(self):
        self.assertEqual(evaluate([])["items"],[])
