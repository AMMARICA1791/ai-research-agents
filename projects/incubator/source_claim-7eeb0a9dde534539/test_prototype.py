import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Open and Emergent Problems in Agentic Privacy and Security: A Contextual Angle'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
