import unittest
from pulse import analyze

class Tests(unittest.TestCase):
    def test_counts_and_sources(self):
        r = analyze({"signals":[
            {"source":"a","signal":{"topics":{"privacy":["privacy"]}},"title":"A","url":"https://example.org/a"},
            {"source":"b","signal":{"topics":{"privacy":["data"]}},"title":"B","url":"https://example.org/b"},
            {"source":"b","signal":{"topics":{"provenance":["evidence"]}},"title":"C","url":"https://example.org/c"}
        ]})
        self.assertEqual(r["topics"][0]["topic"], "privacy")
        self.assertEqual(r["topics"][0]["distinct_sources"], 2)

    def test_empty(self):
        self.assertEqual(analyze({"signals":[]})["topics"], [])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            analyze({"signals":None})

if __name__ == "__main__":
    unittest.main()
