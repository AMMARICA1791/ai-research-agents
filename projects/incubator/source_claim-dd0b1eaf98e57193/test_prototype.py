import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://rentry.co/themis-docket-e61b189e37 Comments URL: https://news.ycombinator.com/item?id=50222576 Points: 4 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
