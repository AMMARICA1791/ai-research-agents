import unittest
from lens import evaluate

class Tests(unittest.TestCase):
    def test_realistic_report_shape(self):
        result = evaluate({"signals":[
            {"source":"a","age_hours":2},
            {"source":"b","age_hours":9},
            {"source":"b","age_hours":27}]})
        self.assertEqual(result["observed_within_6h"], 1)
        self.assertEqual(result["observed_within_24h"], 2)
        self.assertEqual(result["source_diversity"], 2)

    def test_empty_is_honest(self):
        self.assertEqual(evaluate({"signals":[]})["status"], "no_signals")

    def test_invalid_report(self):
        with self.assertRaises(ValueError):
            evaluate({"signals":None})

if __name__ == "__main__":
    unittest.main()
