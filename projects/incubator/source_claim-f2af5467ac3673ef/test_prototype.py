import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.29961v1 Announce Type: new Abstract: Given the enormous number of claims to be checked, verifiable legal AI requires scalable, cost-effective models that answer the practical needs of law. System One decision models are built on large language models but, instead of generating text, return a calibrated probability for each option. This suits the verification of legal authority, where the question is closed: a given holding, or none of '))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
