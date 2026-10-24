import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Ahh… blue lagoon 🏖️ This deep-blue sea of gas and dust—called Messier 8 or the Lagoon Nebula—is a hotbed of star formation. The young stars within the nebula emit rays of high-energy light, including X-rays shown in pink by @chandraxray.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
