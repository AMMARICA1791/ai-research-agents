import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('NVIDIA CEO Jensen Huang asked 4 tiny robots to sit, stand, nap, and do somersaults. And they actually did it. NVIDIA is bringing AI agents from virtual world to real world with these robotic ducks. Media'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
