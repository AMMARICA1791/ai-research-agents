import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://deallocatedobjects.com/posts/making-my-blog-readable-by-ai-agents Comments URL: https://news.ycombinator.com/item?id=50225443 Points: 1 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
