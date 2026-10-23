import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.29178v1 Announce Type: cross Abstract: Before an AI agent takes a consequential action, such as paying, messaging or changing code, several monitors check it. Their verdicts are combined by aggregating scores or by counting approvals, whatever inputs the monitors share. Monitors that share a base model or a poisoned input, however, may fail together. We borrow the fail-prone systems of distributed computing: lists of monitor sets that '))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
