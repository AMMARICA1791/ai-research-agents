"""Regression safeguards for the owner-approved Apache-2.0 transition.

This checks repository consistency, not legal ownership or license compatibility
of external packages and other people's code.
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
READMES = [
    "README.md", "README.ar.md", "README.pt-BR.md", "README.es.md",
    "README.zh-CN.md",
]
RIGHTS_DOCS = [
    "NOTICE", "TRADEMARKS.md", "CONTRIBUTING.md",
    "GOVERNANCE.md", "docs/LICENSING_DECISION.md",
]


def test_canonical_full_apache_2_license_is_present():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert len(text) > 11_000, "Truncated Apache license"
    for required in (
        "Apache License", "Version 2.0, January 2004",
        "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION",
        "2. Grant of Copyright License.",
        "3. Grant of Patent License.",
        "4. Redistribution.",
        "5. Submission of Contributions.",
        "6. Trademarks.",
        "7. Disclaimer of Warranty.",
        "8. Limitation of Liability.",
        "9. Accepting Warranty or Additional Liability.",
        "END OF TERMS AND CONDITIONS",
        "APPENDIX: How to apply the Apache License to your work.",
    ):
        assert required in text
    assert "uvicorn.run(" not in text
    assert "MIT License" not in text


@pytest.mark.parametrize("path", READMES)
def test_every_public_language_homepage_has_correct_license(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    assert "Apache" in text and "2.0" in text
    assert "(LICENSE)" in text
    assert "MIT\n" not in text
    assert "MIT\r\n" not in text


def test_notices_and_trademark_rights_are_explained():
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    assert "Copyright 2026 AMMARICA1791" in notice
    assert "Apache License, Version 2.0" in notice
    marks = (ROOT / "TRADEMARKS.md").read_text(encoding="utf-8")
    assert "Section 6" in marks
    assert "not" in marks.lower()
    for path in RIGHTS_DOCS:
        assert (ROOT / path).exists(), path


def test_contributions_do_not_assign_copyright_or_claim_exclusivity():
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
    decision = (ROOT / "docs/LICENSING_DECISION.md").read_text(encoding="utf-8")
    assert "retain copyright" in contributing
    assert "no assignment" in contributing.lower()
    assert "retai" in governance.lower()
    assert "commercial" in decision
    assert "irrevoc" in decision
    assert "owner" in decision


def test_current_contribution_forms_do_not_claim_license_is_pending():
    template = (ROOT / ".github/pull_request_template.md").read_text()
    research = (ROOT / ".github/ISSUE_TEMPLATE/research_proposal.yml").read_text()
    assert "has not yet been selected" not in template + research
    assert "Apache-2.0" in template + research
