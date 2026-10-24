import json
import tempfile
import unittest
from pathlib import Path
from experiments.rapid_project_radar.anticipate import scaffold
from experiments.rapid_project_radar.successors import successors

class SuccessorTests(unittest.TestCase):
    def test_distinct_question_creates_traceable_successor(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            current = {"topic":"source_claim","source_id":"bbbbbbbbbbbbbbbb",
                       "research_question":"Can new evidence verify B?",
                       "source_excerpt":"Evidence B"}
            scaffold(current,root/"current","source_claim-bbbbbbbbbbbbbbbb")
            inventory = {"projects":[{"project_id":"source_claim-aaaaaaaaaaaaaaaa",
                       "branch":"radar/incubator-source_claim-aaaaaaaaaaaaaaaa",
                       "hypothesis":{"topic":"source_claim","source_id":"aaaaaaaaaaaaaaaa",
                                     "research_question":"Can old evidence verify A?"}}]}
            (root/"portfolio.json").write_text(json.dumps(inventory))
            found=successors(root/"current",root/"portfolio.json",root/"output")
            self.assertEqual(len(found),1)
            h=json.loads((Path(found[0]["path"])/"hypothesis.json").read_text())
            self.assertEqual(h["parent_project_id"],"source_claim-aaaaaaaaaaaaaaaa")
            self.assertEqual(h["research_question"],current["research_question"])
            self.assertEqual(found,successors(root/"current",root/"portfolio.json",root/"output"))
    def test_identical_question_does_not_branch(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            current={"topic":"source_claim","source_id":"bbbbbbbbbbbbbbbb",
                     "research_question":"Same question","source_excerpt":"Evidence B"}
            scaffold(current,root/"current","source_claim-bbbbbbbbbbbbbbbb")
            inventory={"projects":[{"project_id":"source_claim-aaaaaaaaaaaaaaaa",
                       "branch":"radar/incubator-source_claim-aaaaaaaaaaaaaaaa",
                       "hypothesis":{"topic":"source_claim","source_id":"aaaaaaaaaaaaaaaa",
                                     "research_question":"Same question"}}]}
            (root/"portfolio.json").write_text(json.dumps(inventory))
            self.assertEqual(successors(root/"current",root/"portfolio.json",root/"output"),[])
