"""Offline regression tests for evidence-first news evaluation."""
import unittest
from research.news_eval import build, validate, verify_quote, negative_control_ok

class NewsEvalTests(unittest.TestCase):
    def test_exact_quote_only(self):
        self.assertEqual(verify_quote("The result was measured at 87 percent.", "Intro The result was measured at 87 percent. End"), "exact")
        self.assertEqual(verify_quote("The result was measured at 89 percent.", "The result was measured at 87 percent."), "not_found")
        self.assertEqual(verify_quote("87 percent", "The result was measured at 87 percent."), "rejected_too_short")

    def test_failed_article_excluded_and_no_fake_gold(self):
        d={"article_cases":[{"retrieval_status":"ARTICLE_NOT_RETRIEVED","url":"https://example.org/bad"},
                            {"retrieval_status":"ARTICLE_RETRIEVED",
                             "evidence":{"source":{"url":"https://example.org/a","sha256":"abc"},
                                         "source_excerpt":"A documented sentence with enough length to be checked."}}]}
        result=build(d)
        self.assertEqual(len(result["questions"]),3)
        self.assertEqual([q["type"] for q in result["questions"]],["direct","inference","unanswerable"])
        self.assertTrue(all(q["review_status"]=="NEEDS_HUMAN_GOLD_LABEL" for q in result["questions"]))
        self.assertTrue(validate(result))

    def test_empty_or_invalid_dataset_rejected(self):
        self.assertTrue(validate({"questions": []}))
        self.assertTrue(validate({"questions": ["not a question record"]}))
        self.assertTrue(validate({"questions": [{"type": "unknown", "question": "Q", "reference_answer": "A", "source_url": "https://example.org"}]}))

    def test_negative_control_requires_exact_token_empty_quote_and_source(self):
        url = "https://example.org/article"
        self.assertTrue(negative_control_ok("NOT_IN_SOURCE", "", url, url))
        self.assertFalse(negative_control_ok("", "", url, url))
        self.assertFalse(negative_control_ok("SOURCE_RETRIEVED_NOT_INDEPENDENTLY_VERIFIED", "", url, url))
        self.assertFalse(negative_control_ok("NOT_IN_SOURCE", "fabricated", url, url))
        self.assertFalse(negative_control_ok("NOT_IN_SOURCE", "", "https://other.org", url))
        self.assertFalse(negative_control_ok("not_in_source", "", url, url))

    def test_completed_labels_checked(self):
        excerpt="The original report measured an increase of 20 percent."
        data={"questions":[{"type":"direct","question":"What increase was reported?",
                            "reference_answer":"20 percent","reference_quote":excerpt,
                            "archived_excerpt":excerpt,"source_url":"https://example.org/a"},
                           {"type":"unanswerable","question":"What was the budget?",
                            "reference_answer":"NOT_IN_SOURCE","reference_quote":"",
                            "archived_excerpt":excerpt,"source_url":"https://example.org/a"}]}
        self.assertEqual(validate(data),[])
        data["questions"][0]["reference_quote"]="The original report measured an increase of 90 percent."
        self.assertTrue(validate(data))

if __name__=="__main__":
    unittest.main()
