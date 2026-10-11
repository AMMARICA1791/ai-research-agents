import copy
import hashlib
import json

import pytest

from research.evidence_ledger import build_ledger


def report():
    return {
        "status": "public_scholarly_metadata_candidates",
        "research_question": "small language model evaluation",
        "candidate_count": 1,
        "source": {
            "provider": "Crossref",
            "endpoint": "https://api.crossref.org/works?rows=1",
            "retrieved_at_utc": "2026-10-11T18:00:00+00:00",
            "response_sha256": hashlib.sha256(b"public metadata").hexdigest(),
        },
        "records": [{
            "doi": "10.1234/example",
            "doi_url": "https://doi.org/10.1234/example",
            "title": "Example research metadata",
            "year": 2026,
        }],
    }


def test_deterministic_ledger_has_traceable_unverified_evidence():
    first = build_ledger(report())
    assert first == build_ledger(report())
    assert first["entries"][0]["scientific_claim_verified"] is False
    assert first["entries"][0]["source_response_sha256"] == report()["source"]["response_sha256"]
    assert len(first["ledger_sha256"]) == 64


def test_digest_changes_when_source_changes():
    modified = report()
    modified["source"]["response_sha256"] = "f" * 64
    assert build_ledger(modified)["ledger_sha256"] != build_ledger(report())["ledger_sha256"]


@pytest.mark.parametrize("change", [
    lambda r: r.update(candidate_count=2),
    lambda r: r["source"].update(response_sha256="invalid"),
    lambda r: r["source"].update(retrieved_at_utc="2026-10-11T18:00:00"),
    lambda r: r["source"].update(provider="unknown"),
    lambda r: r["records"].append(copy.deepcopy(r["records"][0])),
    lambda r: r["records"][0].update(doi="bad"),
    lambda r: r["records"][0].update(doi_url="https://doi.org/10.1234/other"),
    lambda r: r["records"][0].update(year=True),
    lambda r: r["records"][0].update(year=3000),
])
def test_inconsistent_evidence_rejected(change):
    value = report()
    change(value)
    with pytest.raises(ValueError):
        build_ledger(value)


def test_ledger_serializable_without_paper_content():
    ledger = build_ledger(report())
    data = json.dumps(ledger)
    assert "full_text" not in data
    assert "unreviewed_bibliographic_metadata" in data
