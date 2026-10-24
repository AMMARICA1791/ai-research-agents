import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('LIVE: @NASAAdmin and agency leaders are sharing the latest updates on next year&apos;s Artemis III mission and our plans to return astronauts to the surface of the Moon by 2028. https://x.com/i/broadcasts/1RJZzBdZYQgJB'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
