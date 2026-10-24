import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches("Almost 100,000 Commerce.com domains now give AI agents real shopping tools through WebMCP on Cloudflare. Here's how we turned it on across every store at once, while keeping each merchant in control."))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
