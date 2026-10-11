"""Public scholarly exploration: simulated providers without running external code."""
import hashlib
import json
import pytest
from research.scholarly_discovery import (
    API, MAX_RESPONSE_BYTES, _entry, discover, normalize_crossref,
    summary_md, validate_question,
)

QUESTION = "small language model evaluation"
SOURCE = API + "?query.bibliographic=small+language+model+evaluation&rows=3"
STAMP = "2026-10-11T18:00:00+00:00"

def provider_bytes(items):
    return json.dumps({"message": {"items": items}}).encode()

def paper(doi="10.1234/EXAMPLE.2026.1", title="Small model benchmark"):
    return {
        "DOI": doi, "title": [title],
        "published": {"date-parts": [[2026, 4, 1]]},
        "type": "journal-article", "container-title": ["Research Studies"],
        "abstract": "UNREAD_SECRET_PAPER_CONTENT",
        "author": [{"family": "NeverCopyThis"}],
    }

def normalize(payload, max_results=5):
    return normalize_crossref(
        payload, question=QUESTION, source_url=SOURCE,
        max_results=max_results, retrieved_at=STAMP,
    )

def test_stable_metadata_inventory_with_exact_source_digest():
    payload = provider_bytes([paper(), paper("10.1000/second", "Second work")])
    result = normalize(payload)
    assert result["candidate_count"] == 2
    assert [p["year"] for p in result["records"]] == [2026, 2026]
    assert result["records"][0]["doi"] == "10.1234/example.2026.1"
    assert result["records"][0]["doi_url"] == "https://doi.org/10.1234/EXAMPLE.2026.1"
    assert result["source"]["response_sha256"] == hashlib.sha256(payload).hexdigest()
    assert result["source"]["retrieved_at_utc"] == STAMP
    assert result["model_inference"] is False
    assert result["scientific_claims_verified"] is False
    assert result["full_papers_reviewed"] is False
    assert "UNREAD_SECRET_PAPER_CONTENT" not in json.dumps(result)
    assert "NeverCopyThis" not in json.dumps(result)
    assert normalize(payload) == result

def test_duplicate_and_invalid_entries_reported_not_invented():
    payload = provider_bytes([
        paper(), paper("10.1234/example.2026.1", "Duplicate"),
        paper("invalid-doi"), paper("10.1000/x", ""),
    ])
    result = normalize(payload)
    assert result["candidate_count"] == 1
    assert result["invalid_or_incomplete_records"] == 2
    assert result["duplicate_dois"] == 1
    assert result["records"][0]["title"] == "Small model benchmark"

def test_no_results_not_proof_of_absence():
    result = normalize(provider_bytes([]))
    assert result["candidate_count"] == 0
    assert "not** proof of absence" in summary_md(result)
    assert result["scientific_claims_verified"] is False

def test_untrusted_title_escaped_for_github_summary():
    report = normalize(provider_bytes([paper(title="<img src=x onerror=alert(1)> [click](evil)")]))
    markdown = summary_md(report)
    assert "<img" not in markdown
    assert "&lt;img" in markdown
    assert r"\[click\]\(evil" in markdown

def test_doi_url_never_contains_unescaped_query_or_fragment():
    entry = _entry(paper(doi="10.1234/abc?token=x#y"))
    assert entry is not None
    assert "?token=" not in entry["doi_url"]
    assert "%3F" in entry["doi_url"] and "%23" in entry["doi_url"]

@pytest.mark.parametrize("bad", [
    "hi", "a" * 121, "", "https://example.org", "search@example.org",
    "token\nsecrets", "<script>alert(1)</script>", "research $SENSITIVE",
])
def test_reject_unsafe_research_queries(bad):
    with pytest.raises(ValueError):
        validate_question(bad)

def test_accept_arabic_research_topics():
    assert validate_question("مقارنة النماذج اللغوية الصغيرة") == "مقارنة النماذج اللغوية الصغيرة"

@pytest.mark.parametrize("payload", [
    b"not json", b"{}", b'{"message": {"items": {}}}',
    b'{"message": {"items": "bad"}}', b"[]",
    b'{"message": {"items": [1,2,3,4,5,6,7,8,9]}}',
])
def test_malformed_provider_response_fails_closed(payload):
    with pytest.raises(ValueError):
        normalize(payload)

def test_large_payload_fails_closed():
    with pytest.raises(ValueError, match="exceeds inspection limits"):
        normalize(b"x" * (MAX_RESPONSE_BYTES + 1))

class FakeResponse:
    status = 200
    def __init__(self, payload):
        self.payload = payload
    def read(self, count):
        assert count == MAX_RESPONSE_BYTES + 1
        return self.payload
    def __enter__(self):
        return self
    def __exit__(self, *_):
        return False

def test_requests_exact_public_provider_only_with_no_token(monkeypatch):
    urls = []
    class FakeOpener:
        def open(self, request, timeout):
            urls.append(request.full_url)
            assert timeout == 20
            assert request.full_url.startswith(API + "?")
            assert "rows=3" in request.full_url
            assert "api_key" not in request.full_url
            assert "Authorization" not in request.headers
            return FakeResponse(provider_bytes([paper()]))
    monkeypatch.setattr("research.scholarly_discovery.build_opener", lambda *handlers: FakeOpener())
    report = discover(QUESTION, max_results=3)
    assert len(urls) == 1 and report["source"]["endpoint"] == urls[0]
    assert report["candidate_count"] == 1 and report["model_inference"] is False

def test_provider_failure_does_not_substitute_fake_results(monkeypatch):
    class FakeOpener:
        def open(self, request, timeout):
            raise OSError("provider returned 429")
    monkeypatch.setattr("research.scholarly_discovery.build_opener", lambda *handlers: FakeOpener())
    with pytest.raises(ValueError, match="no offline results substituted"):
        discover(QUESTION)

def test_oversized_http_response_rejected(monkeypatch):
    class FakeOpener:
        def open(self, request, timeout):
            return FakeResponse(b"x"*(MAX_RESPONSE_BYTES+1))
    monkeypatch.setattr("research.scholarly_discovery.build_opener", lambda *handlers: FakeOpener())
    with pytest.raises(ValueError, match="too large"):
        discover(QUESTION)

@pytest.mark.parametrize("limit", [0, 9, True, -1, 1.3])
def test_invalid_result_caps_rejected(limit):
    with pytest.raises(ValueError):
        discover(QUESTION, max_results=limit)

def test_missing_publication_info_not_fabricated():
    item = _entry({"DOI": "10.5432/x", "title": ["A work"], "type": "proceedings-article"})
    assert item["year"] is None
    assert item["venue"] is None
    assert item["abstract_or_full_text_reviewed"] is False


@pytest.mark.parametrize("payload", [
    b'null', b'{"message": null}', b'{"message": []}',
    b'{"message": {"items": null}}',
])
def test_invalid_provider_envelopes_fail_closed(payload):
    with pytest.raises(ValueError):
        normalize(payload)


def test_provider_cannot_exceed_requested_result_cap():
    payload = provider_bytes([paper(f"10.1234/item{i}") for i in range(4)])
    with pytest.raises(ValueError, match="bounded entry limits"):
        normalize(payload, max_results=3)


def test_exact_cap_accepted_without_fabricating_candidates():
    payload = provider_bytes([paper(f"10.1234/item{i}") for i in range(3)])
    report = normalize(payload, max_results=3)
    assert report["candidate_count"] == 3
    assert len(report["records"]) == 3
