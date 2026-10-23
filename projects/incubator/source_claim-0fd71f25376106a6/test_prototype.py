import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('arXiv:2610.31650v1 Announce Type: cross Abstract: Tool-using language model agents rely on environmental facts to decide whether an action is permitted. When a tool response omits a safety-relevant fact, an agent may carry out a prohibited action even though the user request is benign and every returned statement is true. We introduce \\bench{}, an executable benchmark for evaluating unsafe execution, safety boundaries, and evidence recovery in LL'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
