import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Ready for an Artemis update? Tune in Friday, Oct. 23, at 2 p.m. ET (1800 UTC) to hear our latest progress and accelerated plans for Artemis lunar missions. Watch live: https://www.youtube.com/live/pAKqJxuxDgk'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
