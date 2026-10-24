import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Learn how OpenAI scaled Habitat with reliable multi-tenancy, global caching, and Azure Cosmos DB to deliver 12× faster reads for ChatGPT.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
