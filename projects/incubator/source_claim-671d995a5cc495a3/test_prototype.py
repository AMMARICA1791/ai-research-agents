import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://twitter.com/rynorhn/status/2113757656498196605 Comments URL: https://news.ycombinator.com/item?id=50224890 Points: 2 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
