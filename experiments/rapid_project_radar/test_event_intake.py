import unittest
from experiments.rapid_project_radar.event_intake import intake

class IntakeTests(unittest.TestCase):
    def test_valid(self):
        r=intake({"title":"New agent security protocol announced","url":"https://example.org/news"})
        self.assertFalse(r["project_created"])
        self.assertTrue(r["requires_prior_art_review"])
    def test_stable_id(self):
        e={"title":"New agent security protocol announced","url":"https://example.org/news"}
        self.assertEqual(intake(e)["id"],intake(e)["id"])
    def test_reject_http(self):
        with self.assertRaises(ValueError):
            intake({"title":"New agent security protocol announced","url":"http://example.org/news"})
    def test_reject_credentials(self):
        with self.assertRaises(ValueError):
            intake({"title":"New agent security protocol announced","url":"https://user:pass@example.org/news"})
    def test_reject_short_title(self):
        with self.assertRaises(ValueError):
            intake({"title":"short","url":"https://example.org/news"})
