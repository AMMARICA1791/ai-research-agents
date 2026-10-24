import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('🎯 OpenResearch now has @TrackioApp built in 📈 Your agent logs its experiments to Trackio, charts open right next to each run, and it reads the curves back to decide what to try next. Open source and local-first. Running on HF Jobs, Modal, k8s or Slurm? Save a @huggingface Space an…'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
