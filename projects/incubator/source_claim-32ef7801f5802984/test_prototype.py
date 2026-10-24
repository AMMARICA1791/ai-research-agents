import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Bringing foundational models to the front lines of TB screening'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
