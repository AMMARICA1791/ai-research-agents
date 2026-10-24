import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://www.technologyreview.com/2026/10/22/1146103/the-foundations-of-scalable-ai/ Comments URL: https://news.ycombinator.com/item?id=50220098 Points: 2 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
