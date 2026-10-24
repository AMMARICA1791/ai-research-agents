import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://ricuicui.com/articles/navigateur-porte-entree-agents-ia Comments URL: https://news.ycombinator.com/item?id=50222824 Points: 2 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
