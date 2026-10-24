import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Over half of reported crimes in Singapore use sophisticated social engineering. With @GovTechSG, we’re building on-device fraud detection using our open model Gemma. By fine-tuning it on local scam tactics, it identifies threats in real time without compromising personal privacy → https://goo.gle/4ygVkJa'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
