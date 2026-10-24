import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://mantid.dev Comments URL: https://news.ycombinator.com/item?id=50220773 Points: 1 # Comments: 1'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
