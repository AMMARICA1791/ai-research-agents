import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2609.22486v2 Announce Type: replace-cross Abstract: Large language models (LLMs) increasingly ground their answers in proprietary data and live web content through both single-shot retrieval-augmented generation (RAG) and multi-turn agentic search. Yet the web path they use was built for human readers: search services return URLs and snippets ranked by generic relevance, and content delivery networks (CDNs) cache URL-addressed objects witho'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
