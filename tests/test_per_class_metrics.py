"""Per-class metric regression tests use explicit synthetic fixtures, not real research."""
import hashlib

from research.evidence_claims import canonical_digest
from research.per_class_metrics import per_class_report


def fixture(tmp_path, reviewed=True):
    file = tmp_path / "paper.txt"
    file.write_text("No improvement was observed.", encoding="utf-8")
    ledger = {"schema_version": 1, "entries": [{"doi": "10.1234/study"}]}
    ledger["ledger_sha256"] = canonical_digest(ledger)
    return {
        "schema_version": 1, "ledger": ledger,
        "source_texts": [{"doi": "10.1234/study", "file": "paper.txt",
                          "sha256": hashlib.sha256(file.read_bytes()).hexdigest()}],
        "claims": [{"id": "c1", "proposition": "Intervention improves outcomes",
                    "scope": "Adults", "review_status": "unreviewed",
                    "evidence": [{"doi": "10.1234/study", "locator": "Results",
                                  "stance": "supports", "quote": "No improvement was observed."}]}],
        "relationship_reviews": [{
            "claim_id": "c1", "doi": "10.1234/study", "locator": "Results",
            "review_status": "reviewed", "relation": "insufficient",
            "rationale": "This result does not establish the claimed benefit.",
            "reviewer": "synthetic-test-reviewer",
        }] if reviewed else [],
    }


def predictions(label):
    return {"suggestions": [{"claim_id": "c1", "doi": "10.1234/study",
                             "locator": "Results", "relation": label}]}


def test_correct_class_metrics(tmp_path):
    report = per_class_report(fixture(tmp_path), tmp_path, predictions("insufficient"))
    assert report["per_class"]["insufficient"]["precision"] == 1
    assert report["per_class"]["insufficient"]["recall"] == 1
    assert report["confusion_matrix"]["insufficient"]["insufficient"] == 1
    assert report["per_class"]["supports"]["precision"] is None


def test_false_positive_and_false_negative(tmp_path):
    report = per_class_report(fixture(tmp_path), tmp_path, predictions("supports"))
    assert report["per_class"]["supports"]["false_positive"] == 1
    assert report["per_class"]["insufficient"]["false_negative"] == 1
    assert report["accuracy"] == 0


def test_abstention_is_visible(tmp_path):
    report = per_class_report(fixture(tmp_path), tmp_path, predictions(None))
    assert report["confusion_matrix"]["insufficient"]["abstain"] == 1
    assert report["coverage"] == 0


def test_no_human_labels_no_metrics(tmp_path):
    report = per_class_report(fixture(tmp_path, reviewed=False), tmp_path, predictions("insufficient"))
    assert report["reviewed_count"] == 0
    assert report["accuracy"] is None
    assert all(row["precision"] is None for row in report["per_class"].values())
