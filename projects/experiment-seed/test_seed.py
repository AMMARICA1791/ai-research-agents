import unittest
from seed import build

class Tests(unittest.TestCase):
    def test_real_source_traceability(self):
        report = {"signals":[{"id":"abc123456","title":"New Test","url":"https://example.org/paper",
            "source":"arxiv","signal":{"score":2,"topics":{"privacy":["privacy"]}}}]}
        result = build(report)
        self.assertEqual(result["experiments"][0]["source_url"], "https://example.org/paper")
        self.assertFalse(result["experiments"][0]["experiment_executed"])
        self.assertEqual(result["experiments"][0]["radar_topics"], ["privacy"])

    def test_rejects_unlinked(self):
        self.assertEqual(build({"signals":[{"title":"A","url":"http://unsafe"}]})["experiments"], [])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            build({"signals":None})

if __name__ == "__main__":
    unittest.main()
