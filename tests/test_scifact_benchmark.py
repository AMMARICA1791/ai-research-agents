import json

import pytest

from research.scifact_benchmark import benchmark_cases, evaluate


def cases(tmp_path):
    corpus = tmp_path / "corpus.jsonl"
    claims = tmp_path / "claims_dev.jsonl"
    corpus.write_text(json.dumps({"doc_id": 12, "abstract": ["Effect increased.", "Effect did not increase."]}) + "\n")
    claims.write_text(json.dumps({"id": 1, "claim": "The effect increased.", "evidence": {
        "12": [{"label": "SUPPORT", "sentences": [0]}, {"label": "CONTRADICT", "sentences": [1]}]
    }}) + "\n")
    return benchmark_cases(claims, corpus)


def test_ingest_annotated_rationales(tmp_path):
    rows = cases(tmp_path)
    assert len(rows) == 2
    assert {x["gold"] for x in rows} == {"supports", "contradicts"}


def test_per_class_perfect(tmp_path):
    rows = cases(tmp_path)
    predictions = [{"case_id": x["case_id"], "relation": x["gold"]} for x in rows]
    result = evaluate(rows, predictions)
    assert result["per_class"]["supports"]["f1"] == 1
    assert result["per_class"]["contradicts"]["recall"] == 1
    assert result["other_classes_have_gold_labels"] is False


def test_errors_and_abstentions(tmp_path):
    rows = cases(tmp_path)
    result = evaluate(rows, [{"case_id": rows[0]["case_id"], "relation": "contradicts"}])
    assert result["confusion_matrix"]["supports"]["contradicts"] == 1
    assert result["confusion_matrix"]["contradicts"]["abstain"] == 1
    assert result["coverage"] == 0.5


def test_no_predictions_means_zero_coverage_not_accuracy_claim(tmp_path):
    result = evaluate(cases(tmp_path), [])
    assert result["coverage"] == 0
    assert result["accuracy"] == 0


def test_unknown_prediction_rejected(tmp_path):
    with pytest.raises(ValueError, match="Unknown"):
        evaluate(cases(tmp_path), [{"case_id": "unknown", "relation": "supports"}])
