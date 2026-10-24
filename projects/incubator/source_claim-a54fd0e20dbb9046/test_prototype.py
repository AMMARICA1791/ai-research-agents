import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Article URL: https://www.apollo.com/wealth/insights-news/insights/daily-spark/no-signs-of-ai-payoff-outside-the-tech-sector Comments URL: https://news.ycombinator.com/item?id=50224463 Points: 156 # Comments: 110'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
