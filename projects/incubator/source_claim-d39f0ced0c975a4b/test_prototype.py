import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('Even the most regulated industries are going open-source 🤗 The AI question in financial services has moved from which model to use to where that model is allowed to run. New post with @TangriKunal and @huggingface on why firms want to run models on their own infrastructure, and how governance gets them approved to run there. Read it here…'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
