import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('OpenAI explains how we strengthened containment for frontier model training and evaluation, including offline environments and high-compute red-teaming.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
