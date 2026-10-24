import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('W3C launches a Patent Advisory Group (PAG) to resolve issues in the event a patent has been disclosed that may be essential, but is not available under the W3C Royalty-Free licensing terms.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
