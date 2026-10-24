import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Our newest decision model is the world&apos;s best decision model. Introducing GLiDE v1.2, the #1 model on the @huggingface Decision Index. With an overall score of 71.5, GLiDE v1.2 also has one of the lowest calibration errors on the entire Decision Index, meaning its confidence more closely reflects how often its answers are correct. Beyond improved benchmark performance, it also adds support for multimodal inputs, enabling decision-making usin'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
