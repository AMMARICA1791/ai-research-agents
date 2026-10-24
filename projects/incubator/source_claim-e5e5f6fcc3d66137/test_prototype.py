import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://www.theatlantic.com/technology/2026/10/the-safe-internet-is-shrinking/689130/ Comments URL: https://news.ycombinator.com/item?id=50224973 Points: 3 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
