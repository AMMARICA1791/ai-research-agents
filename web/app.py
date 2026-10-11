from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List
import io
import json
import os
import re
import stat
import tempfile
import zipfile

import requests

app = FastAPI(
    title="AI Research Agents",
    version="0.3.0",
    description="AI-powered repository intelligence, graph analysis, reverse engineering, and enterprise-grade digital system analysis"
)


def _safe_repo_path(value: str) -> Path:
    raw = (value or ".").strip()
    if raw in {"", ".", "./"}:
        return Path.cwd().resolve()
    root = Path.cwd().resolve()
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    if not candidate.is_relative_to(root):
        raise HTTPException(status_code=403, detail="Local analysis is restricted to the project directory")
    return candidate


def _is_ignored(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}
    ignore = {
        ".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache",
        ".mypy_cache", ".idea", ".vscode", "dist", "build", ".env", ".next",
        "coverage", "site-packages", ".DS_Store", "__init__.pyc"
    }
    return bool(parts & ignore)


def _language_for(path: Path) -> str:
    ext = path.suffix.lower()
    mapping = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".jsx": "JavaScript",
        ".md": "Markdown",
        ".json": "JSON",
        ".yml": "YAML",
        ".yaml": "YAML",
        ".txt": "Text",
        ".toml": "TOML",
        ".ini": "INI",
        ".csv": "CSV",
        ".html": "HTML",
        ".css": "CSS",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".sql": "SQL",
        ".sh": "Shell",
        ".rb": "Ruby",
        ".php": "PHP",
    }
    return mapping.get(ext, "Other")


def _extract_python_stats(text: str) -> Dict[str, Any]:
    class_count = len(re.findall(r"^\s*class\s+[A-Za-z_][A-Za-z0-9_]*", text, flags=re.MULTILINE))
    function_count = len(re.findall(r"^\s*def\s+[A-Za-z_][A-Za-z0-9_]*", text, flags=re.MULTILINE))
    import_count = len(re.findall(r"^(?:from\s+[A-Za-z0-9_\.]+\s+import|import\s+[A-Za-z0-9_\.]+)", text, flags=re.MULTILINE))
    return {"classes": class_count, "functions": function_count, "imports": import_count}


def analyze_repository(repo_root: Path, max_files: int = 1000) -> Dict[str, Any]:
    repo_root = repo_root.resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        raise HTTPException(status_code=400, detail=f"Invalid path: {repo_root}")

    files: List[Dict[str, Any]] = []
    modules: List[Dict[str, Any]] = []
    graph_nodes: List[Dict[str, Any]] = []
    graph_edges: List[Dict[str, Any]] = []
    file_count = 0

    for path in sorted(repo_root.rglob("*")):
        if file_count >= max_files:
            break
        if path.is_dir():
            if not _is_ignored(path):
                node_id = path.relative_to(repo_root).as_posix()
                graph_nodes.append({"id": node_id, "label": path.name, "type": "directory"})
            continue
        if _is_ignored(path):
            continue

        try:
            rel = path.relative_to(repo_root).as_posix()
            lang = _language_for(path)
            if path.stat().st_size > 1024 * 1024:
                continue  # Do not read huge or potentially sensitive binary files
            content = path.read_text(encoding="utf-8", errors="ignore")
            line_count = len(content.splitlines())

            files.append({
                "path": rel,
                "language": lang,
                "size_bytes": path.stat().st_size,
                "lines": line_count,
                "is_readme": path.name.lower().startswith("readme"),
            })

            graph_nodes.append({"id": rel, "label": path.name, "type": "file", "language": lang})
            parent = path.parent.relative_to(repo_root).as_posix()
            if parent and parent != ".":
                graph_edges.append({"source": parent, "target": rel, "label": "contains"})

            if path.suffix.lower() == ".py":
                stats = _extract_python_stats(content)
                modules.append({
                    "path": rel,
                    "name": rel.replace("/", ".")[:-3],
                    **stats,
                })
            file_count += 1
        except Exception:
            pass

    language_dist: Dict[str, int] = {}
    for item in files:
        lang = item["language"]
        language_dist[lang] = language_dist.get(lang, 0) + 1

    total_lines = sum(item["lines"] for item in files)
    summary = {
        "repo_name": repo_root.name,
        "repo_path": str(repo_root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files),
        "python_files": sum(1 for f in files if f["language"] == "Python"),
        "total_lines": total_lines,
        "languages": language_dist,
    }

    return {
        "status": "ok",
        "summary": summary,
        "files": files,
        "modules": modules,
        "graph": {"nodes": graph_nodes[:500], "edges": graph_edges[:1000]},
        "report": {
            "recommendation": "Repository structure analyzed successfully. Use this output to build better architecture understanding and digital intelligence",
            "focus": ["AI research", "reverse engineering", "identity analysis", "dependency mapping"]
        }
    }


def _parse_github_url(url: str) -> Dict[str, str]:
    value = (url or "").strip()
    if not value:
        raise ValueError("GitHub URL is required")
    match = re.search(r"github\.com/([^/]+)/([^/]+)", value)
    if not match:
        raise ValueError("Invalid GitHub URL")
    owner, repo = match.group(1), match.group(2)
    repo = repo.rstrip("/").split("?", 1)[0].split("#", 1)[0]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return {"owner": owner, "repo": repo}


def analyze_github_repository(url: str) -> Dict[str, Any]:
    parsed = _parse_github_url(url)
    owner = parsed["owner"]
    repo = parsed["repo"]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_meta = requests.get(api_url, timeout=20)
    if repo_meta.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub repository not found or inaccessible")
    meta = repo_meta.json()
    default_branch = meta.get("default_branch", "main")
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    tree_resp = requests.get(tree_url, timeout=20)
    if tree_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Unable to retrieve repository tree")
    tree = tree_resp.json().get("tree", [])
    files: List[Dict[str, Any]] = []
    graph_nodes: List[Dict[str, Any]] = []
    graph_edges: List[Dict[str, Any]] = []
    modules: List[Dict[str, Any]] = []

    for item in tree:
        path = item.get("path")
        if not path or item.get("type") != "blob":
            continue
        if any(part in {".git", ".venv", "venv", "node_modules", "__pycache__"} for part in Path(path).parts):
            continue
        rel = path
        language = _language_for(Path(path))
        files.append({
            "path": rel,
            "language": language,
            "size_bytes": item.get("size", 0),
            "is_readme": Path(path).name.lower().startswith("readme"),
        })
        graph_nodes.append({"id": rel, "label": Path(path).name, "type": "file", "language": language})
        parent = str(Path(rel).parent)
        if parent and parent != ".":
            graph_edges.append({"source": parent, "target": rel, "label": "contains"})
        if path.endswith(".py"):
            modules.append({"path": rel, "name": rel.replace("/", ".")[:-3], "classes": 0, "functions": 0, "imports": 0})

    language_dist: Dict[str, int] = {}
    for item in files:
        lang = item["language"]
        language_dist[lang] = language_dist.get(lang, 0) + 1

    return {
        "status": "ok",
        "source": "github",
        "summary": {
            "repo_name": repo,
            "owner": owner,
            "repo_url": f"https://github.com/{owner}/{repo}",
            "default_branch": default_branch,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_files": len(files),
            "python_files": sum(1 for f in files if f["language"] == "Python"),
            "languages": language_dist,
        },
        "files": files,
        "modules": modules,
        "graph": {"nodes": graph_nodes[:500], "edges": graph_edges[:1000]},
        "report": {
            "recommendation": "Repository imported successfully. Use the platform to analyze architecture, risk areas, and evolution opportunities.",
            "focus": ["reverse engineering", "dependency mapping", "AI research", "digital identity intelligence"]
        }
    }


from lab.memory import LabMemory
from lab.pipeline import LabOrchestrator
from lab.model import OptionalModel
from lab.local_model import LocalOllamaModel
from pydantic import BaseModel

HTML_LANDING = """
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Research Agents | Internal Research Laboratory</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0a1524;color:#e8f0fa;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif}
main{max-width:1010px;margin:0 auto;padding:42px 20px 70px}
.small{font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:#91bded}h1{font-size:clamp(30px,5vw,52px);margin:15px 0}p{line-height:1.65;color:#bcccdc}
.card{background:#12243a;border:1px solid #29415d;border-radius:16px;padding:21px;margin:18px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.role{background:#1a304b;padding:16px;border-radius:12px}
input,button{font:inherit;padding:13px;border-radius:9px}
input{width:100%;border:1px solid #527094;background:#0b1b30;color:#fff}
button{margin-top:12px;background:#78c0ff;border:0;font-weight:700;color:#061725;cursor:pointer}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#061120;border:1px solid #29415d;padding:16px;border-radius:10px;font-size:12px;max-height:420px;overflow:auto}
a{color:#a8d8ff}.status{color:#88e7ba}.muted{font-size:13px;color:#a9bdce}
</style></head>
<body><main>
<div class="small">INDEPENDENT RESEARCH & DEVELOPMENT LAB</div>
<h1>AI Research Agents</h1>
<p>Private research workspace. Five evidence-based agents collaborate on read-only repository analysis, propose improvements and record a reviewable mission journal. No commerce or autonomous code changes.</p>
<section class="grid">
<div class="role"><b>01 — Explorer</b><p>Source inventory</p></div>
<div class="role"><b>02 — Analyst</b><p>Actual Python AST findings</p></div>
<div class="role"><b>03 — Engineer</b><p>Grounded improvement proposals</p></div>
<div class="role"><b>04 — Validator</b><p>Evidence and safety checks</p></div>
<div class="role"><b>05 — Synthesizer</b><p>Mission reports and memory</p></div>
</section>
<section class="card"><h2>Launch a research mission</h2>
<p class="muted">Run on this local checkout; source code is never changed. Proposals stay pending review. For GitHub Actions use the manual workflow on the repository.</p>
<label for="goal">Research goal</label>
<input id="goal" maxlength="500" value="Inspect this research laboratory and suggest evidence-based improvements">
<button id="run" type="button">Run five-stage research</button>
<p id="state" class="status">Ready</p>
<pre id="output" aria-live="polite">Mission results will appear here.</pre></section>
<section class="card"><h2>Research memory</h2>
<button id="history" type="button">Load recent missions</button><pre id="log">History stored in local SQLite.</pre>
<p class="muted">External language-model reasoning is optional and disabled until explicitly configured. Approval never runs or merges code.</p>
</section>
<footer class="muted">AI Research Agents • Internal laboratory • <a href="/docs">API documentation</a></footer>
</main>
<script>
const out=document.getElementById('output'), state=document.getElementById('state');
document.getElementById('run').addEventListener('click',async()=>{
  const goal=document.getElementById('goal').value.trim();
  state.textContent='Running read-only analysis...';
  try{
    const res=await fetch('/api/lab/missions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({goal:goal})});
    const data=await res.json();
    if(!res.ok)throw new Error(JSON.stringify(data));
    out.textContent=JSON.stringify(data,null,2);state.textContent='Mission recorded; proposals require review';
  }catch(err){state.textContent='Mission failed';out.textContent=String(err);}
});
document.getElementById('history').addEventListener('click',async()=>{
  try{const res=await fetch('/api/lab/missions');document.getElementById('log').textContent=JSON.stringify(await res.json(),null,2)}
  catch(err){document.getElementById('log').textContent=String(err);}
});
</script></body></html>
"""

def _render_json_report(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


@app.get("/", response_class=HTMLResponse)
def landing() -> str:
    return HTML_LANDING



@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "ai-research-agents", "version": "0.3.0"}


@app.get("/api/demo")
def api_demo() -> JSONResponse:
    return JSONResponse(content=analyze_repository(Path.cwd()))


@app.post("/api/analyze")
def api_analyze(repo_path: str = Form(...)) -> JSONResponse:
    target = _safe_repo_path(repo_path)
    report = analyze_repository(target)
    return JSONResponse(content=report)


@app.post("/api/analyze/url")
def api_analyze_url(url: str = Form(...)) -> JSONResponse:
    report = analyze_github_repository(url)
    return JSONResponse(content=report)


@app.post("/api/analyze/upload")
async def api_analyze_upload(file: UploadFile = File(...)) -> JSONResponse:
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / "uploaded.zip"
            content = await file.read(10 * 1024 * 1024 + 1)
            if len(content) > 10 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="Archive exceeds 10 MB upload limit")
            zip_path.write_bytes(content)
            extract_dir = Path(tmpdir) / "extracted"
            extract_dir.mkdir()
            with zipfile.ZipFile(zip_path, 'r') as z:
                members = z.infolist()
                if len(members) > 1000 or sum(m.file_size for m in members) > 50 * 1024 * 1024:
                    raise HTTPException(status_code=413, detail="Archive exceeds extraction limits")
                for item in members:
                    target = (extract_dir / item.filename).resolve()
                    if (not target.is_relative_to(extract_dir)
                        or item.filename.startswith(("/", "\\"))
                        or "\\" in item.filename
                        or stat.S_ISLNK(item.external_attr >> 16)):
                        raise HTTPException(status_code=400, detail="Unsafe archive entry")
                z.extractall(extract_dir)
            report = analyze_repository(extract_dir)
            return JSONResponse(content=report)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/api/report")
def api_report() -> JSONResponse:
    report = analyze_repository(Path.cwd())
    return JSONResponse(content={"report": _render_json_report(report)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


class LabMissionRequest(BaseModel):
    goal: str


def _lab_memory() -> LabMemory:
    return LabMemory(Path.cwd() / ".data" / "lab.sqlite")


@app.get("/api/lab/status")
def lab_status() -> Dict[str, Any]:
    return {
        "purpose": "internal_research",
        "roles": list(LabOrchestrator.stages),
        "model_enabled": (LocalOllamaModel().configured if os.getenv("LAB_MODEL_BACKEND") == "ollama" else OptionalModel().configured),
        "autonomous_code_changes": False,
        "history_scope": "local_sqlite",
    }


@app.get("/api/lab/missions")
def lab_missions() -> Dict[str, Any]:
    return {"missions": _lab_memory().list_missions()}


@app.get("/api/lab/missions/{mission_id}")
def lab_mission_detail(mission_id: str) -> Dict[str, Any]:
    report = _lab_memory().get_mission(mission_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return report


@app.post("/api/lab/missions")
def lab_execute_mission(request: LabMissionRequest) -> Dict[str, Any]:
    try:
        return LabOrchestrator(_lab_memory()).run(Path.cwd(), request.goal)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
