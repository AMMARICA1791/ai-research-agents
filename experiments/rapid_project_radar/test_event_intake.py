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


class EventPipelineContractTests(unittest.TestCase):
    def test_push_signal_flows_to_hypothesis_generator(self):
        from experiments.rapid_project_radar.event_intake import to_radar_report
        from experiments.rapid_project_radar.anticipate import hypotheses
        report = to_radar_report({"title": "A novel scientific experiment on optical clocks",
                                  "url": "https://example.org/research/clock",
                                  "description": "We introduce a clock stability measurement technique."})
        self.assertEqual(len(report["signals"]), 1)
        self.assertTrue(report["signals"][0]["event_driven"])
        self.assertEqual(hypotheses(report["signals"][0])[0]["topic"], "source_claim")
