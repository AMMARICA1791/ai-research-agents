import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://www.militarytimes.com/industry/techwatch/2026/10/23/us-air-force-wants-ai-to-assist-aerial-refueling/ Comments URL: https://news.ycombinator.com/item?id=50221226 Points: 2 # Comments: 1'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
