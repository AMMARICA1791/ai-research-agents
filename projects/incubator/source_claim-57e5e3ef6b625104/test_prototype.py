import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('NASA’s Inspiration Tour has landed in in the SEC 🚀🏈 Ahead of Alabama vs. Texas A&amp;M, @NASAAdmin met with students and fans outside Bryant-Denny Stadium, joined @SecRollins to sign a new MOU between NASA and @USDA , and will soon take to the skies for today’s flyover!'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
