import unittest
from delta import evaluate

class Tests(unittest.TestCase):
    def test_counts(self):
        data = evaluate({"signals":[
            {"title":"a","url":"https://example.org/a","first_seen_this_scan":True},
            {"title":"b","url":"https://example.org/b","first_seen_this_scan":False},
            {"title":"c"}]})
        self.assertEqual((data["newly_observed"],data["previously_observed"],data["unknown_first_seen_status"]), (1,1,1))

    def test_empty(self):
        self.assertEqual(evaluate({"signals":[]})["newly_observed"], 0)

if __name__ == "__main__":
    unittest.main()
