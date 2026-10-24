import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://medicalxpress.com/news/2026-10-ai-generalist-doctors-medical.html Comments URL: https://news.ycombinator.com/item?id=50220694 Points: 6 # Comments: 0'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
