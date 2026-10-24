import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://medium.com/@ivan_43200/i-built-a-saas-with-ai-two-months-later-i-have-zero-active-users-1e93436a5b39 Comments URL: https://news.ycombinator.com/item?id=50223278 Points: 2 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
