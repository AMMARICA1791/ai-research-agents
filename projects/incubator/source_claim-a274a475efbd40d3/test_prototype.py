import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://torrentfreak.com/ai-assisted-paper-on-z-library-cites-a-torrentfreak-article-that-doesnt-exist/ Comments URL: https://news.ycombinator.com/item?id=50220204 Points: 56 # Comments: 17'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
