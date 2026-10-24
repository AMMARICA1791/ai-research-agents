import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches('I wanted a read-aloud extension that could read from the Kindle Online Reader. The ones I tried used voices I did not enjoy listening to or had a UX that was too cluttered or annoying or needed a signup. So I decided to vibe code my own. It is open source and uses open weight models that run in the browser. https://swrdfish.github.io/Narro/ Comments URL: https://news.ycombinator.com/item?id=50224373 Points: 5 # Comments: 1'))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
