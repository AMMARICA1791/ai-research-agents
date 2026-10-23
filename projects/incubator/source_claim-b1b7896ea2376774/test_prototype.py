import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches("arXiv:2610.30758v1 Announce Type: cross Abstract: AI-assisted editing can produce loan documents that preserve familiar issuer layouts while changing the applicant's identity. We investigated whether experienced underwriters and loan processors identify such forgeries in first-pass, document-only review. Three practitioners recruited through Upwork each received one applicant package drawn from 134 forged PDFs derived from 47 genuine financial do"))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
