import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2609.17631v2 Announce Type: replace Abstract: AI-assisted claims can appear authoritative when evidence, analysis, human authorization, presentation, and correction history describe different states. We develop Publication Authority: an exact-state, non-transferable, single-use publication capability within PAC-2026 (Publication-Accountability Calculus), an AIJIM Protocol candidate. The evaluated specification version (SF-4) defines six non'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
