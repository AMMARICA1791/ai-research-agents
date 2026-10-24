import unittest
from gap import analyze

class Tests(unittest.TestCase):
    def test_failures(self):
        r = analyze({"signals":[{"source":"a"}],"feed_errors":[{"feed":"b","error":"TimeoutError"}],"successful_feeds":1})
        self.assertEqual(r["failed_feeds"], ["b"])
        self.assertEqual(r["selected_signal_counts"]["a"], 1)

    def test_empty(self):
        self.assertEqual(analyze({"signals":[],"feed_errors":[]})["coverage_warning"], "no_selected_signals")

    def test_invalid(self):
        with self.assertRaises(ValueError):
            analyze({"signals":"bad"})

if __name__ == "__main__":
    unittest.main()
