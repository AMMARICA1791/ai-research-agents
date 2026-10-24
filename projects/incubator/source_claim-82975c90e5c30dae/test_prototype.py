import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('That&apos;s our jam 🎼 Astronomers used @ChandraXray to find out that this radio wave formation, known as the &quot;Treble Clef&quot; thanks to its distinctive shape, was likely caused by an outburst from a supermassive black hole, followed by a collision of two galaxy clusters.'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
