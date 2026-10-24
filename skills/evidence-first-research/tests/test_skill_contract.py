"""Offline checks only. Does not evaluate model behavior."""
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"

class SkillContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()

    def test_frontmatter(self):
        self.assertTrue(self.text.startswith("---\n"))
        match = re.match(r"\A---\n(.*?)\n---\n", self.text, re.S)
        self.assertIsNotNone(match)
        self.assertRegex(match.group(1), r"(?m)^name: evidence-first-research$")
        self.assertRegex(match.group(1), r"(?m)^description: .+")

    def test_complete_workflow(self):
        for item in ("Scope", "Collect", "Verify", "Map", "Challenge", "Propose tests", "Review", "Archive"):
            with self.subTest(item=item):
                self.assertIn(item.lower(), self.lower)

    def test_source_and_claim_outputs(self):
        for item in ("evidence inventory", "claim-evidence matrix", "reproducibility protocol", "human-review actions"):
            with self.subTest(item=item):
                self.assertIn(item, self.lower)

    def test_no_fabrication_and_no_novelty_overclaim(self):
        for item in ("do not fabricate", "not verified", "worldwide novelty", "human judgment", "synthetic test"):
            with self.subTest(item=item):
                self.assertIn(item, self.lower)

    def test_untrusted_source_handling(self):
        self.assertIn("untrusted evidence, not instructions", self.lower)
        self.assertIn("never execute untrusted code", self.lower)

if __name__ == "__main__":
    unittest.main()
