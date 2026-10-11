"""Grounded review triage: priorities are deterministic, never a security verdict."""
import copy
import json

import pytest

from lab.triage import build_work_orders


REPO = "https://github.com/sample/public-project"
SHA = "a" * 40


def sample_findings():
    return [
        {"rule": "missing_tests", "severity": "medium", "evidence": ".", "message": "No tests"},
        {"rule": "silent_exception", "severity": "medium", "evidence": "src/worker.py:12", "message": "pass"},
        {"rule": "dynamic_execution", "severity": "medium", "evidence": "src/danger.py:8", "message": "eval"},
        {"rule": "syntax_error", "severity": "high", "evidence": "src/broken.py:2", "message": "Syntax"},
    ]


def test_priority_is_review_order_and_evidence_links_pin_to_commit():
    original = sample_findings()
    before = copy.deepcopy(original)
    queue = build_work_orders(REPO, SHA, original)
    work = queue["work_orders"]
    assert [w["rule"] for w in work] == [
        "syntax_error", "dynamic_execution", "silent_exception", "missing_tests"
    ]
    assert [w["priority"] for w in work] == ["P1", "P2", "P2", "P3"]
    assert work[0]["evidence_url"] == REPO + "/blob/" + SHA + "/src/broken.py#L2"
    assert work[3]["evidence_url"] == REPO + "/tree/" + SHA
    assert all(w["fix_generated"] is False for w in work)
    assert all(w["review_status"] == "pending_human_verification" for w in work)
    assert all("not" in w["uncertainty"].lower() for w in work)
    assert queue["automated_patch_generated"] is False
    assert queue["human_review_required"] is True
    assert original == before
    assert build_work_orders(REPO, SHA, original) == queue


def test_unknown_or_malicious_evidence_is_rejected_not_emitted():
    malicious = sample_findings() + [
        {"rule": "syntax_error", "severity": "high", "evidence": "../escape.py:10"},
        {"rule": "syntax_error", "severity": "high", "evidence": "bad\nissue.py:10"},
        {"rule": "syntax_error", "severity": "high", "evidence": "/root/secret.py:20"},
        {"rule": "syntax_error", "severity": "high", "evidence": "src\\secret.py:20"},
        {"rule": "unverified_rule", "severity": "high", "evidence": "x.py:3"},
        {"rule": ["unhashable"], "severity": "high", "evidence": "x.py:4"},
        {"rule": "syntax_error", "severity": "low", "evidence": {"not": "path"}},
    ]
    queue = build_work_orders(REPO, SHA, malicious)
    assert queue["rejected_malformed_findings"] == 7
    assert len(queue["work_orders"]) == 4
    assert "../escape" not in json.dumps(queue)
    assert "bad\nissue" not in json.dumps(queue)


def test_duplicates_and_limit_are_bounded():
    f = sample_findings()
    q = build_work_orders(REPO, SHA, f + [f[0]], limit=2)
    assert q["total_valid_unique_findings"] == 4
    assert len(q["work_orders"]) == 2
    assert q["not_shown_due_to_cap"] == 2
    assert q["rejected_malformed_findings"] == 0


def test_no_findings_does_not_invent_any_problem():
    q = build_work_orders(REPO, SHA, [])
    assert q["work_orders"] == []
    assert q["total_valid_unique_findings"] == 0


@pytest.mark.parametrize("identity", [
    "http://github.com/sample/public-project",
    "https://github.com.evil.org/sample/public-project",
    "https://github.com/sample/public-project/other",
    "https://evil.test/sample/public-project",
    "https://github.com/sample/public-project?token=secret",
])
def test_reject_untrusted_repo_identity(identity):
    with pytest.raises(ValueError):
        build_work_orders(identity, SHA, sample_findings())


@pytest.mark.parametrize("sha", ["b"*39, "c"*41, "X"*40, "main", "b"*40 + "/other"])
def test_reject_untrusted_source_revision(sha):
    with pytest.raises(ValueError):
        build_work_orders(REPO, sha, sample_findings())


@pytest.mark.parametrize("limit", [0, -1, 21, 1.5, True])
def test_reject_unbounded_or_invalid_caps(limit):
    with pytest.raises(ValueError):
        build_work_orders(REPO, SHA, sample_findings(), limit=limit)


def test_nonfindings_or_oversized_reports_fail_closed():
    with pytest.raises(ValueError):
        build_work_orders(REPO, SHA, [{}] * 101)
    with pytest.raises(ValueError):
        build_work_orders(REPO, SHA, "not a list")


def test_url_encoding_does_not_create_a_fake_source_link():
    findings = [{"rule": "silent_exception", "severity": "medium", "evidence": "odd[#].py:3"}]
    q = build_work_orders(REPO, SHA, findings)
    url = q["work_orders"][0]["evidence_url"]
    assert url.endswith("/odd%5B%23%5D.py#L3")
    assert q["work_orders"][0]["evidence"] == "odd[#].py:3"
