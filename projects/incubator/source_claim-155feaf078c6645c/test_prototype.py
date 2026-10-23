import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2607.03651v4 Announce Type: replace Abstract: While traditional hub capacity planning models optimize effectively for quantitative inputs, they often fail to digest qualitative business context. We propose a novel framework where a large language model (LLM) agent iteratively proposes hub capacity decisions guided by natural-language business context descriptions. The key mechanism is a chain-of-thought reasoning protocol: the LLM construct'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
