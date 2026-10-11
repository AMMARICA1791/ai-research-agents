"""Research baseline: no marketing claims or silent regression in release artifacts."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_legacy_commercial_drafts_absent_from_active_release_tree():
    assert not (ROOT / "archive/commercial-drafts").exists()


def test_canonical_license_and_attribution_survive_release():
    assert "Apache License" in text("LICENSE")
    assert "Version 2.0" in text("LICENSE")
    assert "Copyright 2026" in text("NOTICE")


def test_readme_leads_with_evidence_and_agent_limitations():
    content = text("README.md")
    assert "Seven coordinated pipeline stages, NOT seven independent thinking AI agents" in content[:650]
    assert content.index("## See the evidence") < content.index("## Reproduce the research")
    assert "DEMO.md" in content
    assert "experimental baseline release notes" in content


def test_demo_contains_exactly_three_standard_library_commands():
    content = text("DEMO.md")
    blocks = re.findall(r"(?ms)^\x60\x60\x60sh\n(.*?)^\x60\x60\x60", content)
    assert len(blocks) == 1
    commands = [l.strip() for l in blocks[0].splitlines() if l.strip()]
    assert commands == [
        "python -m lab.public_demo --repo . --out results/public-demo",
        "python -m lab.benchmark",
        "python -m lab.autorepair",
    ]
    assert "does not rerun Qwen" in content
    assert "not" in content.lower() and "synthetic" in content.lower()


def test_release_notes_include_success_and_historical_failures():
    notes = text("docs/RELEASE_0.1.0_EXPERIMENTAL.md")
    for item in ("## Repeat the evidence", "### Positive evidence",
                 "### Negative evidence and limitations", "Qwen",
                 "GitHub Actions", "human", "not", "public repository"):
        assert item.lower() in notes.lower()
    assert "not a stable product" in notes
    assert "tag/release actually created" in notes


def test_no_old_mit_or_commercial_claim_in_active_launch_docs():
    for path in ("README.md", "README.ar.md", "CHANGELOG.md",
                 "DEMO.md", "ARCHITECTURE.md",
                 "docs/RELEASE_0.1.0_EXPERIMENTAL.md"):
        content = text(path)
        assert "MIT License" not in content
        assert "Enterprise support available" not in content
        assert "Production Ready" not in content
        assert "Seed/Series A" not in content
    assert "Apache-2.0" in text("CHANGELOG.md")
    assert "0.1.0-experimental" in text("CHANGELOG.md")


def test_research_mission_not_reduced_to_python_repair():
    roadmap = text("ROADMAP.md").lower()
    scope = text("docs/PROJECT_SCOPE.md").lower()
    for area in ("research and exploration", "experiments and comparisons",
                 "cumulative knowledge", "engineering and independent validation"):
        assert area in roadmap
    assert "not the entire mission" in scope


def test_release_workflow_requires_tests_before_publishing():
    workflow = text(".github/workflows/experimental-release.yml")
    assert "python -m pytest -q tests/" in workflow
    assert "python -m lab.public_demo" in workflow
    assert "python -m lab.benchmark" in workflow
    assert "python -m lab.autorepair" in workflow
    assert "needs: verify" in workflow
    assert "github.event_name == 'push'" in workflow
    assert "contents: write" in workflow
    assert "gh release create" in workflow
    assert "--prerelease" in workflow
    assert "--verify-tag" in workflow
