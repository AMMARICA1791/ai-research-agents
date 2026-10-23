import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2602.06232v2 Announce Type: replace-cross Abstract: Game balancing is a longstanding challenge requiring repeated playtesting, expert intuition, and extensive manual tuning. We introduce RuleSmith, a framework that couples multi-agent LLM self-play with surrogate-based optimization over a parameterized rule space. As a proof of concept, we build CivMini, a simplified civilization-style game with two asymmetric factions governed by 12 tunabl'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
