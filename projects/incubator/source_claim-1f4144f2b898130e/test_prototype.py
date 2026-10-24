import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('SynthID timeline over the last few weeks has been momentous – from opening SynthID Detector to the public, to launching SynthID Bio to watermark functional, AI-designed proteins. Each moment brought us a step closer to our broader vision on provenance, or helping verify what is AI-generated and what isn’t. Recently, Dartmouth Professor Hany Farid and I discussed why solving provenance is vital to @GoogleDeepMind’s broader mission to develop AI to'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
