import tempfile
import unittest
from pathlib import Path
from experiments.rapid_project_radar.council import review, write_review

class CouncilTests(unittest.TestCase):
    def test_peer_communication_and_priority(self):
        h = {"topic": "source_claim", "source_id": "abc", "source_title": "Agent security evaluation",
             "source_excerpt": "We propose an independently testable approach to evaluate agents.",
             "research_question": "Can this result be replicated?", "independent_validation": False}
        result = review(h, [{"source_title": "Agent security evaluation methods"}])
        self.assertEqual(len(result["reviewers"]), 4)
        self.assertEqual(len(result["peer_messages"]), 3)
        self.assertFalse(result["reviewers"][2]["scientific_result_reproduced"])
        self.assertTrue(result["reviewers"][1]["possible_overlaps"])
        self.assertEqual(result["status"], "reviewed_not_validated")

    def test_incomplete_evidence_gets_lower_priority(self):
        empty = review({"topic": "source_claim", "source_id": "a"})
        rich = review({"topic": "source_claim", "source_id": "b",
                       "source_title": "Some research", "source_excerpt": "We introduce a method.",
                       "research_question": "Can it work?"})
        self.assertLess(empty["priority"]["score"], rich["priority"]["score"])

if __name__ == "__main__":
    unittest.main()
