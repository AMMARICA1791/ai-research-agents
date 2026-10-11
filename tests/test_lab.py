"""End-to-end checks for real static research, shared memory, and review gates."""
import json
from fastapi.testclient import TestClient
from lab.cli import main
from lab.inspector import inspect_repository
from lab.memory import LabMemory
from lab.model import OptionalModel
from lab.pipeline import LabOrchestrator
from web.app import app

def seed_repo(root):
    (root / "agent.py").write_text(
        "import os\n"
        "def inspect():\n"
        "    try:\n"
        "        return 3\n"
        "    except Exception:\n"
        "        pass\n", encoding="utf-8")
    (root / ".env").write_text("SECRET_DO_NOT_EXPOSE=hello", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests/test_agent.py").write_text("def test_one():\n    assert True\n", encoding="utf-8")

def test_scanner_real_evidence_and_ignores_secrets(tmp_path):
    seed_repo(tmp_path)
    result = inspect_repository(tmp_path)
    assert result["python_files_parsed"] == 2
    assert result["files_scanned"] == 2
    assert ".env" not in json.dumps(result)
    assert any(x["rule"] == "silent_exception" and x["evidence"] == "agent.py:6" for x in result["findings"])

def test_syntax_error_is_grounded(tmp_path):
    (tmp_path / "bad.py").write_text("def broken(:\n", encoding="utf-8")
    data = inspect_repository(tmp_path)
    assert any(x["rule"] == "syntax_error" and x["evidence"].startswith("bad.py:") for x in data["findings"])

def test_pipeline_durable_memory_and_review_gate(tmp_path):
    seed_repo(tmp_path)
    store = LabMemory(tmp_path / ".data" / "memory.sqlite")
    orchestrator = LabOrchestrator(store, model=OptionalModel(endpoint="", api_key="", model=""))
    report = orchestrator.run(tmp_path, "Find improvements for the laboratory itself")
    assert report["agent_stages"] == ["explorer", "analyst", "engineer", "validator", "synthesizer"]
    assert report["report"]["model"]["mode"] == "not_configured"
    assert report["report"]["validation"]["evidence_grounded"] is True
    assert report["report"]["validation"]["changes_applied"] is False
    assert store.get_mission(report["id"])["events"]
    assert len(store.list_missions()) == 1
    proposal = report["proposals"][0]
    assert proposal["status"] == "pending_review"
    before = (tmp_path / "agent.py").read_bytes()
    assert store.decide(proposal["id"], approve=True)
    assert not store.decide(proposal["id"], approve=True)
    assert store.get_mission(report["id"])["proposals"][0]["status"] == "approved"
    assert before == (tmp_path / "agent.py").read_bytes()

def test_cli_generates_artifact_and_history(tmp_path, capsys):
    seed_repo(tmp_path)
    dest = tmp_path / "results" / "mission.json"
    db = str(tmp_path / ".data" / "lab.sqlite")
    assert main(["--db", db, "mission", "--repo", str(tmp_path),
                 "--goal", "Inspect this laboratory and propose repairs", "--output", str(dest)]) == 0
    body = json.loads(dest.read_text())
    assert body["status"] == "completed"
    assert body["report"]["discovery"]["python_files_parsed"] == 2
    assert main(["--db", db, "history"]) == 0

def test_local_lab_http_end_to_end(tmp_path, monkeypatch):
    seed_repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    client = TestClient(app)
    assert client.get("/api/lab/status").status_code == 200
    assert "Research Laboratory" in client.get("/").text
    response = client.post("/api/lab/missions", json={"goal": "Inspect our research lab for improvements"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "completed"
    assert data["report"]["discovery"]["python_files_parsed"] == 2
    assert data["report"]["validation"]["changes_applied"] is False
    assert client.get("/api/lab/missions").json()["missions"]
    detail = client.get("/api/lab/missions/" + data["id"])
    assert detail.status_code == 200
    assert detail.json()["proposals"][0]["status"] == "pending_review"
    assert client.get("/api/lab/missions/" + "not-an-id").status_code == 404
    assert client.get("/pricing").status_code == 404

def test_missing_provider_is_explicit():
    assert OptionalModel(endpoint="", api_key="", model="").summarize("test", []) == {
        "mode": "not_configured", "narrative": None
    }

def test_model_adapter_mock_no_source_sent(monkeypatch):
    import lab.model as provider
    class FakeReply:
        def raise_for_status(self): return None
        def json(self): return {"choices": [{"message": {"content": "Review the recorded finding"}}]}
    captured = {}
    def fake_post(url, headers, json, timeout):
        captured["body"] = json
        return FakeReply()
    monkeypatch.setattr(provider.requests, "post", fake_post)
    p = OptionalModel(endpoint="https://models.example.test/v1/chat/completions", api_key="test-key", model="test-model")
    result = p.summarize("Improve our lab", [{"rule": "syntax_error", "severity": "high", "evidence": "bad.py:1", "secret": "NEVER_SEND"}])
    assert result["mode"] == "remote_model"
    assert "NEVER_SEND" not in str(captured["body"])
    assert "test-key" not in str(captured["body"])
