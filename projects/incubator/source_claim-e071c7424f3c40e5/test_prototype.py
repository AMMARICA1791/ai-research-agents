import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://substack.norabble.com/p/ai-safety-is-all-hands-on-deck Comments URL: https://news.ycombinator.com/item?id=50220831 Points: 2 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
