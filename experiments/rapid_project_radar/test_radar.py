import unittest
import datetime as dt
from experiments.rapid_project_radar.radar import parse_feed,run,score

XML=b'''<rss><channel><item><title>Agent permission and consent</title>
<link>https://example.org/paper</link><description>web agent authorization</description>
<pubDate>Fri, 23 Oct 2026 10:00:00 GMT</pubDate></item>
<item><title>Unrelated article</title><link>https://example.org/other</link><pubDate>Fri, 23 Oct 2026 10:00:00 GMT</pubDate>
</item></channel></rss>'''

class RadarTests(unittest.TestCase):
    def test_relevant_feed(self):
        items=parse_feed(XML,"sample")
        self.assertEqual(len(items),2)
        self.assertGreater(items[0]["signal"]["score"],0)
        self.assertFalse(items[0]["novelty_verified"])
    def test_no_keyword_signal_still_retained(self):
        self.assertEqual(score("gardening","flowers")["score"],0)
        items=parse_feed(XML,"sample")
        self.assertIn("Unrelated article",[item["title"] for item in items])
    def test_deduplicate(self):
        r=run({"a":"https://example.org/a","b":"https://example.org/b"},lambda _:XML,now=dt.datetime(2026,10,24,0,tzinfo=dt.timezone.utc))
        self.assertEqual(len(r["signals"]),2)
        self.assertEqual(r["successful_feeds"],2)
        self.assertEqual(r["selected_within_24_hours"],2)
        self.assertAlmostEqual(r["selected_age_hours_median"],14)
        self.assertIn("not first-seen latency",r["latency_measurement_note"])
    def test_source_diversity_under_high_volume(self):
        def feed(url):
            source = "a" if url.endswith("/a") else "b"
            count = 60 if source == "a" else 1
            items = "".join(
                "<item><title>Agent security discovery " + str(i) + "</title>"
                "<link>https://example.org/" + source + "/" + str(i) + "</link>"
                "<description>agent authorization privacy</description><pubDate>Fri, 23 Oct 2026 10:00:00 GMT</pubDate></item>"
                for i in range(count))
            return ("<rss><channel>" + items + "</channel></rss>").encode()
        report = run({"a":"https://example.org/a","b":"https://example.org/b"},feed,now=dt.datetime(2026,10,24,0,tzinfo=dt.timezone.utc))
        self.assertEqual(len(report["signals"]),40)
        self.assertEqual({x["source"] for x in report["signals"]},{"a","b"})
        self.assertEqual(len({x["id"] for x in report["signals"]}),40)

    def test_older_arxiv_month_is_not_a_new_discovery(self):
        xml=b"""<rss><channel><item><title>Old submission reappears</title>
<link>https://arxiv.org/abs/2607.27204</link>
<pubDate>Fri, 23 Oct 2026 10:00:00 GMT</pubDate></item>
<item><title>Current month submission</title>
<link>https://arxiv.org/abs/2610.29812</link>
<pubDate>Fri, 23 Oct 2026 10:00:00 GMT</pubDate></item></channel></rss>"""
        report=run({"a":"https://example.org/a"},lambda _:xml,
                   now=dt.datetime(2026,10,24,0,tzinfo=dt.timezone.utc))
        self.assertEqual(len(report["signals"]),1)
        self.assertEqual(report["excluded_older_arxiv_submission_month"],1)

    def test_stale_and_undated_excluded(self):
        report=run({"a":"https://example.org/a"},lambda _:XML,
                   now=dt.datetime(2026,10,28,0,tzinfo=dt.timezone.utc))
        self.assertEqual(len(report["signals"]),0)
        self.assertEqual(report["excluded_stale"],2)

    def test_failures_visible(self):
        def fail(_): raise OSError("offline")
        r=run({"a":"https://example.org/a"},fail)
        self.assertEqual(r["successful_feeds"],0)
        self.assertEqual(r["feed_errors"][0]["error"],"OSError")
    def test_no_auto_build_claim(self):
        r=run({"a":"https://example.org/a"},lambda _:XML)
        self.assertFalse(r["autonomous_code_generation"])

if __name__=="__main__":
    unittest.main()
