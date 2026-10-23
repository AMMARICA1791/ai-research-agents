import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.15884v3 Announce Type: replace-cross Abstract: False retry permission (FRP) occurs when an agent retries a timed-out tool call without support from the visible contract. RetryBench separates this error from realized recovery. Successful protected recovery does not imply reliable rejection of unsupported retries. In a 720-response key control, valid keys usually enabled safe progress, but offered changed keys elicited unsupported retrie'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
