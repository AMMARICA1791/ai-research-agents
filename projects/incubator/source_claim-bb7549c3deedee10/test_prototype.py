import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('NASA just shared some major updates on the road ahead for Artemis 🚀 2027: Artemis III tests Orion and two lunar landers in low Earth orbit. 2028: Artemis IV returns Americans to the Moon. Catch up on today&apos;s announcements in this special edition NASA Minute! Media'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
