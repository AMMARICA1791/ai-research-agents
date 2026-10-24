import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Fast, focused, low-cost decisions for any application.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
