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


def test_legacy_knowledge_migrates_to_evidence_lessons(tmp_path):
    from lab.knowledge import empty_state, record, historical_context, load_state, save_state
    import json
    p = tmp_path / "knowledge.json"
    old = {"schema_version": 1, "runs": [
        {"at": "2026-10-01T00:00:00+00:00", "files_scanned": 10, "python_parsed": 5,
         "finding_count": 1, "risk_counts": {"high": 0, "medium": 1, "low": 0},
         "rule_counts": {"silent_exception": 1}, "model_mode": "not_configured"}]}
    p.write_text(json.dumps(old), encoding="utf-8")
    state = load_state(p)
    assert state["lessons"][0]["rule"] == "silent_exception"
    assert state["lessons"][0]["consecutive_runs"] == 1
    assert state["lessons"][0]["next_check"] == "test_exception_observability"
    assert historical_context(state)["previous_runs"] == 1
    # Work is still observed, do not claim it is repaired.
    response = {"report": {
        "discovery": {"files_scanned": 10, "python_files_parsed": 5},
        "risk_counts": {"high": 0, "medium": 1, "low": 0},
        "findings": [{"rule": "silent_exception", "evidence": "private.py:3"}],
        "model": {"mode": "local_model"}
    }}
    record(state, response)
    save_state(p, state)
    reloaded = load_state(p)
    assert len(reloaded["runs"]) == 2
    assert reloaded["lessons"][0]["consecutive_runs"] == 2
    text = p.read_text()
    assert "private.py" not in text
    assert "test_exception_observability" in text


def test_public_lessons_reject_injected_free_text(tmp_path):
    from lab.knowledge import load_state
    import json
    import pytest
    p = tmp_path / "knowledge.json"
    p.write_text(json.dumps({
        "schema_version": 1, "runs": [],
        "lessons": [{"rule": "secret leaked", "next_check": "run unsafe code"}]
    }), encoding="utf-8")
    with pytest.raises(ValueError):
        load_state(p)


def test_previous_research_data_reaches_local_model_without_sensitive_text(monkeypatch):
    import lab.local_model as module
    requests_seen = []
    class Reply:
        def raise_for_status(self): pass
        def json(self): return {"message": {"content": "Observe the recurrence before changing code."}}
    def post(url, json, timeout, allow_redirects):
        requests_seen.append(json)
        return Reply()
    monkeypatch.setattr(module.requests, "post", post)
    model = LocalOllamaModel()
    answer = model.summarize("PRIVATE GOAL", [
        {"rule": "silent_exception", "evidence": "internal/private.py:5", "secret": "HIDDEN"},
    ], history={
        "previous_runs": 3,
        "previous_rule_counts": {"silent_exception": 2, "SHOULD_NOT_LEAK": "PRIVATE_VALUE"},
        "lessons": [
            {"rule": "silent_exception", "consecutive_runs": 2, "malicious": "HIDDEN"},
        ],
        "raw_memory": "TOP_SECRET_JOURNAL",
    })
    assert answer["mode"] == "local_model"
    assert len(requests_seen) == 2
    for entry in requests_seen:
        wire = str(entry)
        assert "'previous_runs': 3" in wire
        assert "'consecutive_runs': 2" in wire
        assert "PRIVATE GOAL" not in wire
        assert "SHOULD_NOT_LEAK" not in wire
        assert "TOP_SECRET_JOURNAL" not in wire
        assert "internal/private.py" not in wire
        assert "HIDDEN" not in wire


def test_laboratory_produces_self_improvement_work_order(tmp_path, monkeypatch):
    import lab.local_model as model_api
    monkeypatch.setenv("LAB_MODEL_BACKEND", "ollama")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_basic.py").write_text("def test_sanity(): assert True\n")
    (tmp_path / "bad.py").write_text(
        "def foo():\n    try:\n        return 1\n    except Exception:\n        pass\n", encoding="utf-8")
    class Reply:
        def raise_for_status(self): pass
        def json(self): return {"message": {"content": "Recommend testing this behavior."}}
    monkeypatch.setattr(model_api.requests, "post", lambda *a, **kw: Reply())
    kb = tmp_path / ".data" / "knowledge.json"
    research = LabOrchestrator(LabMemory(tmp_path / ".data" / "audit.sqlite"),
                               knowledge_path=kb)
    first = research.run(tmp_path, "Identify self-improvement tasks in the laboratory")
    second = research.run(tmp_path, "Compare with our previous research observations")
    assert first["report"]["model"]["mode"] == "local_model"
    orders = second["report"]["work_orders"]
    assert orders
    assert orders[0]["rule"] == "silent_exception"
    assert orders[0]["evidence"] == "bad.py:4"
    assert orders[0]["observed_in_prior_run"] is True
    assert orders[0]["status"] == "proposed_not_executed"
    assert orders[0]["approval"] == "required"
    assert second["report"]["prior_knowledge"]["previous_runs"] == 1
    assert load_state(kb)["lessons"][0]["consecutive_runs"] == 2
    assert (tmp_path / "bad.py").read_text().endswith("        pass\n")
