import unittest
from prototype import evidence_matches
class Tests(unittest.TestCase):
    def test_trace(self):
        self.assertTrue(evidence_matches("Imagine this. You can control Alexa with your voice and ask it to play songs, remember grocery lists, add reminders to your calendar. Elon Musk's Neuralink can interface with your brain and reduce the latency with which you can communicate with computers. What if you had AI applied to your brain and you could train it to think like you just like how you train your agents at work? Comments URL: https://news.ycombinator.com/item?id=50223726 Points:"))
    def test_missing(self):
        self.assertFalse(evidence_matches('unrelated'))
