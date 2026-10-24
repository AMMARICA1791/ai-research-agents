import unittest
from bridge import analyze, connect

class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.a = {"source":"journal","title":"Quantum sensor detects magnetic field variation","url":"https://example.org/a"}
        self.b = {"source":"laboratory","title":"Quantum sensor measures magnetic field changes","url":"https://example.org/b"}

    def test_cross_source_connection(self):
        result = connect([self.a,self.b])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["confidence"], "low")
        self.assertFalse(result[0]["novelty_verified"])

    def test_same_source_excluded(self):
        self.b["source"] = "journal"
        self.assertEqual(connect([self.a,self.b]), [])

    def test_no_false_connection(self):
        self.b["title"] = "Unrelated biological microscopy sample"
        self.assertEqual(connect([self.a,self.b]), [])

    def test_invalid_report(self):
        with self.assertRaises(ValueError):
            analyze({"signals": "wrong"})

if __name__ == "__main__":
    unittest.main()
