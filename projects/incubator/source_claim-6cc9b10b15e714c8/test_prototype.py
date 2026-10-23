import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.29929v2 Announce Type: replace-cross Abstract: In response to vast and widespread online tracking, regulators and technologists alike have worked to develop laws and tools that allow people to express their privacy preferences. These measures seek to offer users greater control over the sale and sharing of personal information, putting agency in their hands to protect their privacy. However, the web is undergoing a seismic shift, away '))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
