import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches("arXiv:2604.24920v4 Announce Type: replace-cross Abstract: Agentic systems now act with user secrets for APIs, messaging platforms, and cloud services. Today's agent runtimes typically implement authorization by exposure: enabling action means placing a reusable secret, or a reusable artifact derived from it, inside the runtime, so a transient prompt-injection or tool-side compromise becomes durable account compromise. Existing defenses cover adja"))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
