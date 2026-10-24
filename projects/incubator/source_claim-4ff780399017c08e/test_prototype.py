import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Live From SF! We’re teaching these folk how to train their own open weight agents. Sorry, but we won’t live stream. Full recording coming tomorrow! Join us tomorrow on the training agents livestream, and here from experts about how they&apos;re scaling RL and evals to train frontier agents. \u200bWe will look beyond single-turn RL to multi-step, environment-driven training: reward design, rollouts, benchmarks, and the practical gap be…'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
