import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://github.com/tensemem/tensemem Comments URL: https://news.ycombinator.com/item?id=50221670 Points: 1 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
