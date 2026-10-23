import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('This system card outlines the comprehensive safety measures implemented for GPT‑5.1-CodexMax. It details both model-level mitigations, such as specialized safety training for harmful tasks and prompt injections, and product-level mitigations like agent sandboxing and configurable network access.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
