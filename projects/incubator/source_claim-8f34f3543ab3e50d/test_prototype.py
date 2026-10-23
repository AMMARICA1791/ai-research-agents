import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.28655v1 Announce Type: cross Abstract: Publishers and funders increasingly ask authors to disclose how AI tools contributed to a piece of research. In computational work the repository is where an author or an auditor would look for the answer, and we ask what it can actually supply. We audit two single-investigator repositories by the same author in the same field, each carrying a different class of agent residue: a prescriptive trace'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
