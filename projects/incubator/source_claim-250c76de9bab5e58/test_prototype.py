import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://kouh.me/ai-text-detector Comments URL: https://news.ycombinator.com/item?id=50220254 Points: 5 # Comments: 7'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
