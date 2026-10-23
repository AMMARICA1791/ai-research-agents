import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('OpenAI is strengthening ChatGPT Atlas against prompt injection attacks using automated red teaming trained with reinforcement learning. This proactive discover-and-patch loop helps identify novel exploits early and harden the browser agent’s defenses as AI becomes more agentic.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
