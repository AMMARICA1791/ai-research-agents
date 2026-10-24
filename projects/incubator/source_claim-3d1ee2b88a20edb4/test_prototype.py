import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://www.construction-physics.com/p/reading-list-102426 Comments URL: https://news.ycombinator.com/item?id=50220547 Points: 1 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
