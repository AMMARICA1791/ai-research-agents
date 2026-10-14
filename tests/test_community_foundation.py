"""Community readiness checks: critical docs, links and CI safety boundaries."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "README.ar.md", "QUICKSTART.md", "CONTRIBUTING.md",
    "SECURITY.md", "CODE_OF_CONDUCT.md", "GOVERNANCE.md",
    "ROADMAP.md", "docs/PROJECT_SCOPE.md",
    "docs/LICENSING_DECISION.md", ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/research_proposal.yml",
]


def test_essential_community_documents_are_real_files():
    assert not [path for path in REQUIRED if not (ROOT / path).is_file()]


def test_main_ci_runs_all_python_tests_not_a_curated_subset():
    workflow = (ROOT / ".github/workflows/validate-mvp.yml").read_text()
    assert "python -m pytest -q tests/" in workflow


def test_no_python_startup_script_is_mistaken_for_a_software_license():
    license_path = ROOT / "LICENSE"
    if license_path.exists():
        legal = license_path.read_text(encoding="utf-8")
        assert "uvicorn.run(" not in legal
        assert "Start the web server" not in legal
    else:
        assert (ROOT / "docs/LICENSING_DECISION.md").exists()


def test_primary_community_docs_have_no_broken_relative_links():
    pages = [
        "README.md", "README.ar.md", "README.pt-BR.md", "README.es.md",
        "README.zh-CN.md", "QUICKSTART.md", "DEMO.md",
        "CONTRIBUTING.md", "SECURITY.md", "GOVERNANCE.md",
        "ROADMAP.md", "docs/PROJECT_SCOPE.md",
        "docs/LICENSING_DECISION.md", "docs/README.md",
        "docs/PROJECT_SHOWCASE.md", "docs/PUBLIC_DEMO.md",
        "docs/GITHUB_DISCOVERY_SETUP.md",
        "docs/NEWS_SEMANTIC_REVIEW_PROTOCOL.md",
        "docs/REAL_NEWS_QWEN_EVIDENCE_2026-10-13.md",
        "docs/NEWS_SEMANTIC_REVIEW_TRIAGE_RUN_38500177379.md",
    ]
    bad = []
    for name in pages:
        file = ROOT / name
        content = file.read_text(encoding="utf-8")
        for href in re.findall(r"\]\(([^)]+)\)", content):
            if href.startswith(("https://", "http://", "#", "mailto:")):
                continue
            target = href.split("#", 1)[0]
            if target and not (file.parent / target).exists():
                bad.append(f"{name}: {href}")
    assert not bad, bad


def test_owner_controls_license_and_merges():
    governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8").lower()
    license_decision = (ROOT / "docs/LICENSING_DECISION.md").read_text().lower()
    assert "owner" in governance
    assert "human" in governance
    assert "owner" in license_decision
    assert "not" in license_decision


def test_external_review_entry_points_visible_in_all_language_readmes():
    for path in ("README.md", "README.ar.md", "README.pt-BR.md",
                 "README.es.md", "README.zh-CN.md"):
        page = (ROOT / path).read_text(encoding="utf-8")
        assert "docs/PROJECT_SHOWCASE.md" in page, path
        assert "issues/54" in page, path


def test_public_showcase_separates_evidence_from_unproven_claims():
    doc = (ROOT / "docs/PROJECT_SHOWCASE.md").read_text(encoding="utf-8")
    assert "issues/22" in doc  # reproduce a result
    assert "issues/52" in doc  # human source-review volunteers
    assert "issues/54" in doc  # project-wide feedback
    assert "not seven separately reasoning agents" in doc
    assert "Quality gate failed" in doc
    assert "not a certification" in doc
    assert "Python 3.11+" in doc


def test_feedback_form_does_not_require_coding_or_private_credentials():
    form = (ROOT / ".github/ISSUE_TEMPLATE/project_feedback.yml").read_text(encoding="utf-8")
    assert "Project-wide feedback" in form
    assert "issues/54" in form
    assert "Do not include secrets" in form
    assert "id: observation" in form
    assert "required: true" in form
