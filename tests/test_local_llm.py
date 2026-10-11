"""Zero-key local model integration tests. Network is mocked here; CI live test is separate."""
import json
from lab.local_model import LocalOllamaModel
from lab.memory import LabMemory
from lab.pipeline import LabOrchestrator
from lab.knowledge import load_state

def test_zero_key_local_model_is_sanitized(monkeypatch):
    import lab.local_model as module
    calls = []
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self): return {"message": {"content": "Counts support a tentative finding."}}
    def fake_post(url, json, timeout, allow_redirects):
        assert url == "http://127.0.0.1:11434/api/chat"
        assert allow_redirects is False
        calls.append(json)
        return FakeResponse()
    monkeypatch.setattr(module.requests, "post", fake_post)
    model=LocalOllamaModel()
    output=model.summarize("CONFIDENTIAL GOAL", [{
        "rule":"syntax_error", "evidence":"secret/private.py:1", "private":"TOPSECRET"
    }])
    assert output["mode"] == "local_model"
    assert len(output["reviews"]) == 2 and len(calls) == 2
    for req in calls:
        text = str(req)
        assert "CONFIDENTIAL GOAL" not in text
        assert "secret/private.py" not in text
        assert "TOPSECRET" not in text
        assert req["model"] == "qwen2.5:0.5b"

def test_local_unavailable_is_explicit(monkeypatch):
    import lab.local_model as module
    def fail(*args, **kwargs):
        raise module.requests.exceptions.ConnectionError("no server")
    monkeypatch.setattr(module.requests, "post", fail)
    answer=LocalOllamaModel().summarize("safe", [])
    assert answer["mode"] == "local_model_unavailable"
    assert answer["narrative"] is None

def test_lab_selects_free_backend_and_journal_records_it(tmp_path, monkeypatch):
    import lab.local_model as module
    monkeypatch.setenv("LAB_MODEL_BACKEND", "ollama")
    (tmp_path/"tests").mkdir()
    (tmp_path/"tests"/"test_example.py").write_text("def test_a(): pass\n")
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self): return {"message":{"content":"Local AI reviewed the counts"}}
    monkeypatch.setattr(module.requests, "post", lambda *a,**kw: FakeResponse())
    knowledge=tmp_path/"knowledge.json"
    run=LabOrchestrator(memory=LabMemory(tmp_path/"test.sqlite"),knowledge_path=knowledge).run(
        tmp_path, "Examine repository structure without modifying source"
    )
    assert run["report"]["model"]["mode"] == "local_model"
    assert len(run["report"]["model"]["reviews"]) == 2
    state=load_state(knowledge)
    assert state["runs"][0]["model_mode"] == "local_model"
    assert "Local AI reviewed" not in knowledge.read_text()

def test_model_rejects_arbitrary_model_choice():
    import pytest
    with pytest.raises(ValueError):
        LocalOllamaModel(model="made-up")
