"""Honest safety tests for a real LLM candidate gate (unit mocks only)."""
import json

import lab.model_patch as trial
from lab.autorepair import FIXTURE, propose_fail_closed


class FakeReply:
    def __init__(self, value):
        self.value = value
    def raise_for_status(self):
        return None
    def json(self):
        return {"response": json.dumps(self.value)}


def test_valid_model_written_code_must_pass_real_red_green(monkeypatch):
    captured = {}
    proposed = propose_fail_closed(FIXTURE)["candidate"]
    def mock_post(url, json, timeout, allow_redirects):
        assert url == "http://127.0.0.1:11434/api/generate"
        assert json["model"] == "qwen2.5-coder:1.5b"
        assert allow_redirects is False
        assert "pass" in json["prompt"]
        captured["request"] = json
        return FakeReply({"code": proposed})
    monkeypatch.setattr(trial.requests, "post", mock_post)
    result = trial.run_coder_challenge()
    assert result["status"] == "accepted_verified_model_generated_patch"
    assert result["repository_modified"] is False
    assert result["baseline_failed_as_expected"] is True
    assert result["repaired_test_passed"] is True
    assert captured["request"]["stream"] is False


def test_wrong_model_patch_is_rejected_without_execution(monkeypatch):
    def mock_post(*args, **kwargs):
        return FakeReply({"code": FIXTURE + "\nimport os\nos.system('echo unsafe')\n"})
    monkeypatch.setattr(trial.requests, "post", mock_post)
    def never_run(*args, **kwargs):
        raise AssertionError("Rejected candidate must never be executed")
    monkeypatch.setattr(trial, "_run_fixture", never_run)
    answer = trial.run_coder_challenge()
    assert answer["candidate_rejected"] is True
    assert answer["repository_modified"] is False
    assert "candidate" not in answer


def test_model_cannot_return_only_rhetorical_claim(monkeypatch):
    monkeypatch.setattr(trial.requests, "post", lambda *a, **kw: FakeReply({"passed": True}))
    answer = trial.run_coder_challenge()
    assert answer["status"] == "rejected_unsafe_or_incorrect_candidate"
    assert answer["candidate_rejected"] is True


def test_model_unreachable_is_not_a_success(monkeypatch):
    def fail(*args, **kwargs):
        raise trial.requests.ConnectionError("mock outage")
    monkeypatch.setattr(trial.requests, "post", fail)
    answer = trial.run_coder_challenge()
    assert answer["candidate_rejected"] is True
    assert answer["status"] == "model_unavailable_or_invalid_response"
