import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2609.31713v2 Announce Type: replace-cross Abstract: As large language models (LLMs) become capable of processing increasingly diverse modalities and longer temporal contexts, an emerging line of work is moving beyond fixed video-language inference toward agentic systems that actively decide what information to inspect, retain, verify, and act upon. This survey reviews video understanding agents: systems that use video as the primary informa'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
