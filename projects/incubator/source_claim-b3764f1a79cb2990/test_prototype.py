import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://homepage.farm/ai.html Comments URL: https://news.ycombinator.com/item?id=50220640 Points: 5 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
