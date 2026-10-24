"""Offline contract checks for Community v0.2.0. Not model behavior tests."""
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
        match = re.match(r"\A---\n(.*?)\n---\n", self.text, re.S)
        self.assertIsNotNone(match)
        self.assertRegex(match.group(1), r"(?m)^name: evidence-first-research$")
        self.assertRegex(match.group(1), r"(?m)^description: .+")

    def test_four_rules(self):
        for phrase in ("stay on task", "never invent evidence", "distinguish what you know", "bound the conclusion"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_source_integrity(self):
        for phrase in ("doi", "unverified", "abstract only", "actually accessed", "never manufacture bibliographic metadata"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_scope_and_reproducibility(self):
        for phrase in ("user's current research question", "reproducible test", "worldwide novelty", "human review"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_safe_and_concise(self):
        for phrase in ("never execute untrusted code", "preserve privacy", "do not fill empty templates"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

if __name__ == "__main__":
    unittest.main()
