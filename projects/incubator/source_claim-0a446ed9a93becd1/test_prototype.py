import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://www.uxness.in/2026/08/top-ux-conferences-to-attend-in-2027.html Comments URL: https://news.ycombinator.com/item?id=50225094 Points: 3 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
