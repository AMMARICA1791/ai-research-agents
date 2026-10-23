import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches("arXiv:2604.04978v3 Announce Type: replace-cross Abstract: Claude Code's auto mode is the first deployed permission system for AI coding agents, using a two-stage transcript classifier to gate dangerous tool calls. Anthropic reports a 0.4% false positive rate and 17% false negative rate on production traffic. We present the first independent evaluation of this system on deliberately ambiguous authorization scenarios, i.e., tasks where the user's i"))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
