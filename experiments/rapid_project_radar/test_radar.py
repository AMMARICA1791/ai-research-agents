import unittest
from experiments.rapid_project_radar.radar import parse_feed,run,score

XML=b'''<rss><channel><item><title>Agent permission and consent</title>
<link>https://example.org/paper</link><description>web agent authorization</description>
<pubDate>Fri, 23 Oct 2026 10:00:00 GMT</pubDate></item>
<item><title>Unrelated article</title><link>https://example.org/other</link>
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
        r=run({"a":"https://example.org/a","b":"https://example.org/b"},lambda _:XML)
        self.assertEqual(len(r["signals"]),2)
        self.assertEqual(r["successful_feeds"],2)
    def test_source_diversity_under_high_volume(self):
        def feed(url):
            source = "a" if url.endswith("/a") else "b"
            count = 60 if source == "a" else 1
            items = "".join(
                "<item><title>Agent security discovery " + str(i) + "</title>"
                "<link>https://example.org/" + source + "/" + str(i) + "</link>"
                "<description>agent authorization privacy</description></item>"
                for i in range(count))
            return ("<rss><channel>" + items + "</channel></rss>").encode()
        report = run({"a":"https://example.org/a","b":"https://example.org/b"},feed)
        self.assertEqual(len(report["signals"]),40)
        self.assertEqual({x["source"] for x in report["signals"]},{"a","b"})
        self.assertEqual(len({x["id"] for x in report["signals"]}),40)

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
