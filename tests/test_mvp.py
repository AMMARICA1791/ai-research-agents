"""Integration tests: public routes, repository inspection, imports, and boundaries."""
import asyncio
import io
import zipfile

import pytest
from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)

def test_health_and_pages():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert client.get("/").status_code == 200
    assert client.get("/pricing").status_code == 404

def test_local_analysis(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "hello.py").write_text("class Hello:\n    def greet(self):\n        return 1\n", encoding="utf-8")
    data = client.post("/api/analyze", data={"repo_path": "."})
    assert data.status_code == 200, data.text
    report = data.json()
    assert report["status"] == "ok"
    assert report["summary"]["python_files"] == 1
    assert any(x["path"] == "hello.py" and x["classes"] == 1 for x in report["modules"])
    assert client.get("/api/report").status_code == 200

def test_restrict_filesystem_access(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    response = client.post("/api/analyze", data={"repo_path": str(tmp_path.parent)})
    assert response.status_code == 403

def test_valid_zip_upload():
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("src/hello.py", "def hello():\n    return 1\n")
    response = client.post("/api/analyze/upload", files={"file": ("code.zip", stream.getvalue(), "application/zip")})
    assert response.status_code == 200, response.text
    assert response.json()["summary"]["python_files"] == 1

def test_bad_zip_upload():
    result = client.post("/api/analyze/upload", files={"file": ("bad.zip", b"garbage", "application/zip")})
    assert result.status_code == 400

def test_block_archive_traversal():
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("../outside.py", "print('bad')")
    response = client.post("/api/analyze/upload", files={"file": ("evil.zip", stream.getvalue(), "application/zip")})
    assert response.status_code == 400

def test_github_url_metadata(monkeypatch):
    class FakeResponse:
        status_code = 200
        def __init__(self, result):
            self.result = result
        def json(self):
            return self.result

    def fake_get(url, timeout):
        if url == "https://api.github.com/repos/demo/sample":
            return FakeResponse({"default_branch": "main"})
        if url == "https://api.github.com/repos/demo/sample/git/trees/main?recursive=1":
            return FakeResponse({"tree": [{"path": "a.py", "type": "blob", "size": 12}, {"path": "README.md", "type": "blob", "size": 100}]})
        raise AssertionError("unexpected URL: " + url)

    import importlib
    app_module = importlib.import_module("web.app")
    monkeypatch.setattr(app_module.requests, "get", fake_get)
    response = client.post("/api/analyze/url", data={"url": "https://github.com/demo/sample"})
    assert response.status_code == 200, response.text
    assert response.json()["summary"]["total_files"] == 2

def test_core_agents_execute():
    from agents import ExplorerAgent, AnalystAgent, BenchmarkerAgent, SynthesizerAgent, ValidatorAgent
    from agents.nlp_specialist import NLPSpecialistAgent
    from agents.vision_specialist import VisionSpecialistAgent
    from agents.performance_engineer import PerformanceEngineerAgent
    from agents.data_engineer import DataEngineerAgent
    from agents.research_synthesizer import ResearchSynthesizerAgent
    classes = (ExplorerAgent, AnalystAgent, BenchmarkerAgent, SynthesizerAgent, ValidatorAgent,
               NLPSpecialistAgent, VisionSpecialistAgent, PerformanceEngineerAgent,
               DataEngineerAgent, ResearchSynthesizerAgent)
    async def exercise():
        for cls in classes:
            agent = cls()
            result = await agent.execute("demo", {})
            assert isinstance(result, dict) and result
            assert agent.get_status()["status"] == "completed"
    asyncio.run(exercise())

def test_research_types():
    from research import ResearchProject, KnowledgeGraph, KnowledgeNode, KnowledgeEdge, BenchmarkSuite
    from experiments import Experiment
    project = ResearchProject(title="demo", description="test", owner="demo")
    assert project.to_dict()["title"] == "demo"
    graph = KnowledgeGraph()
    first, second = KnowledgeNode(name="first"), KnowledgeNode(name="second")
    graph.add_node(first)
    graph.add_node(second)
    graph.add_edge(KnowledgeEdge(source_id=first.id, target_id=second.id, edge_type="uses"))
    assert graph.get_neighbors(first.id)[0].id == second.id
    assert BenchmarkSuite().list_benchmarks()
    assert Experiment(name="demo").to_dict()["status"] == "planned"
