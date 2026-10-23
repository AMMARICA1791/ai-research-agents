import tempfile
import unittest
from pathlib import Path
from experiments.rapid_project_radar.anticipate import generate,hypotheses

class AnticipateTests(unittest.TestCase):
    def test_no_signal(self):
        self.assertEqual(generate({"signals":[]},tempfile.mkdtemp()),[])
    def test_topic_hypothesis(self):
        h=hypotheses({"signal":{"topics":{"privacy":["privacy"]}}})
        self.assertEqual(len(h),1)
        self.assertFalse(h[0]["novelty_verified"])
    def test_distinct_signals_get_distinct_projects(self):
        report={"signals":[{"id":"a","signal":{"topics":{"privacy":["privacy"]}}},
                           {"id":"b","signal":{"topics":{"privacy":["privacy"]}}}]}
        with tempfile.TemporaryDirectory() as d:
            result=generate(report,d)
            self.assertEqual(len(result),2)
            self.assertNotEqual(result[0]['project_id'],result[1]['project_id'])
            for item in result:
                self.assertTrue((Path(item['path'])/'prototype.py').exists())
                self.assertTrue((Path(item['path'])/'test_prototype.py').exists())
    def test_unsupported_topic_not_executed(self):
        with tempfile.TemporaryDirectory() as d:
            r=generate({"signals":[{"signal":{"topics":{"evil_code":["exec"]}}}]},d)
            self.assertEqual(r,[])
