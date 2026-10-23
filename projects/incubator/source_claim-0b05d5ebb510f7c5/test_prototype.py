import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Consensus uses GPT-5 and OpenAI’s Responses API to power a multi-agent research assistant that reads, analyzes, and synthesizes evidence in minutes—helping over 8 million researchers accelerate scientific discovery.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
