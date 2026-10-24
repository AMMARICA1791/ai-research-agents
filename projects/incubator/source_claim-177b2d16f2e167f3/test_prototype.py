import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://stevekrouse.com/10x Comments URL: https://news.ycombinator.com/item?id=50221446 Points: 3 # Comments: 2'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
