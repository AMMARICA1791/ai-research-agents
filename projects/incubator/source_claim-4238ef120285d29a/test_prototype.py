import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://noyb.eu/en/ai-eu-member-states-approve-digital-expropriation-europeans-ai-companies Comments URL: https://news.ycombinator.com/item?id=50223856 Points: 3 # Comments: 2'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
