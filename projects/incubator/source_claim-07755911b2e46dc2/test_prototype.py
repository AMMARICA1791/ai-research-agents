import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches("arXiv:2610.29010v1 Announce Type: new Abstract: Radiation treatment planning requires balancing competing objectives to satisfy clinical criteria while accommodating physicians' preferences. This study aims to develop an evidence-driven, multi-agent compound AI system that integrates DRL-based automated treatment planning with LLM-based conversational plan refinement for proton PBS therapy. A policy network trained using PPO first generates multi"))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
