import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Learn how OpenAI protects user data when AI agents open links, preventing URL-based data exfiltration and prompt injection with built-in safeguards.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
