from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List
import json
import os
import re
import tempfile
import zipfile

import requests

app = FastAPI(
    title="AI Research Agents MVP",
    version="0.2.0",
    description="AI-powered repository intelligence, graph analysis, and reverse engineering platform"
)


def _safe_repo_path(value: str) -> Path:
    raw = (value or ".").strip()
    if raw in {"", ".", "./"}:
        return Path.cwd().resolve()
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = (Path.cwd() / candidate).resolve()
    return candidate


def _is_ignored(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}
    ignore = {
        ".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache",
        ".mypy_cache", ".idea", ".vscode", "dist", "build", ".env", ".next",
        "coverage", "site-packages"
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

    summary = {
        "repo_name": repo_root.name,
        "repo_path": str(repo_root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files),
        "python_files": sum(1 for f in files if f["language"] == "Python"),
        "total_lines": sum(f["lines"] for f in files),
        "languages": language_dist,
    }

    return {
        "status": "ok",
        "summary": summary,
        "files": files,
        "modules": modules,
        "graph": {"nodes": graph_nodes[:500], "edges": graph_edges[:1000]},
    }


def _parse_github_url(url: str) -> Dict[str, str]:
    value = (url or "").strip()
    if not value:
        raise ValueError("GitHub URL is required")
    match = re.search(r"github\.com/([^/]+)/([^/]+)", value)
    if not match:
        raise ValueError("Invalid GitHub URL")
    owner, repo = match.group(1), match.group(2)
    repo = repo.rstrip("/")
    repo = repo.split("#", 1)[0].split("?", 1)[0]
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
    files = []
    graph_nodes = []
    graph_edges = []
    modules = []
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

    language_dist = {}
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
    }


HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Research Agents</title>
  <style>
    body { margin:0; font-family: Inter, Arial, sans-serif; background: linear-gradient(135deg,#061421,#0c2033,#112f47); color:#edf6ff; }
    .container { max-width:1200px; margin:0 auto; padding:32px 20px 80px; }
    .nav { display:flex; justify-content:space-between; align-items:center; padding:12px 0 20px; border-bottom:1px solid rgba(255,255,255,.1); }
    .brand { font-weight:800; font-size:1.3rem; background:linear-gradient(135deg,#5da8ff,#82d9ff); -webkit-background-clip:text; color:transparent; }
    a { color:#5da8ff; text-decoration:none; }
    .hero { padding:52px 0 32px; text-align:center; }
    .tag { display:inline-block; padding:8px 14px; background:rgba(93,168,255,.14); border:1px solid rgba(93,168,255,.35); border-radius:999px; font-size:12px; letter-spacing:.08em; text-transform:uppercase; }
    h1 { font-size:clamp(2.4rem,6vw,4rem); margin:18px 0 18px; }
    .subtitle { max-width:760px; margin:0 auto; color:#d8ebff; font-size:1.15rem; line-height:1.7; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:22px; margin-top:40px; }
    .card { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:22px; }
    .card h3 { margin:0 0 10px; }
    .card p { color:#bfd5ed; margin:0; }
    form { display:flex; gap:12px; flex-wrap:wrap; margin-top:22px; }
    input, select { flex:1 1 380px; padding:15px 17px; border-radius:12px; border:1px solid rgba(255,255,255,.12); background:rgba(7,17,27,.7); color:#fff; font-size:1rem; }
    button { padding:15px 22px; border:none; border-radius:12px; background:linear-gradient(135deg,#4da3ff,#82d9ff); color:#061421; font-weight:800; cursor:pointer; }
    .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:20px; margin:42px 0 22px; }
    .stat { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08); border-radius:14px; padding:20px; text-align:center; }
    .stat strong { display:block; font-size:2rem; color:#82d9ff; }
    .section-title { margin:48px 0 24px; font-size:2.1rem; }
    .pricing { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:22px; }
    .price-card { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.09); border-radius:16px; padding:28px; }
    .price-card.featured { border-color:rgba(93,168,255,.4); background:rgba(93,168,255,.08); }
    .price { font-size:2rem; font-weight:800; }
    .result-box { margin-top:22px; background:rgba(2,11,18,.75); border:1px solid rgba(255,255,255,.1); border-radius:16px; padding:18px; white-space:pre-wrap; overflow:auto; }
    footer { margin-top:50px; padding-top:30px; border-top:1px solid rgba(255,255,255,.1); text-align:center; color:#9bb2c8; }
    @media (max-width: 760px) { .nav { flex-direction:column; gap:12px; } form { display:block; } input, button { width:100%; display:block; margin-bottom:10px; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="nav">
      <div class="brand">AI Research Agents</div>
      <div>
        <a href="#features">Features</a> ·
        <a href="#pricing">Pricing</a> ·
        <a href="#demo">Demo</a>
      </div>
    </div>

    <section class="hero">
      <div class="tag">v0.2.0 • Active MVP</div>
      <h1>Reveal the hidden architecture of digital systems.</h1>
      <div class="subtitle">
        AI-powered repository intelligence for reverse engineering, graph mapping, digital identity analysis,
        and system-level knowledge discovery.
      </div>
      <form id="repo-form">
        <input id="repo_path" value="." placeholder="Enter local path or GitHub URL" />
        <button type="submit">Analyze</button>
      </form>
      <div class="stats">
        <div class="stat"><strong>100x</strong><span>Faster than manual review</span></div>
        <div class="stat"><strong>90%</strong><span>Lower cost than consulting</span></div>
        <div class="stat"><strong>95%+</strong><span>Visibility into system structure</span></div>
        <div class="stat"><strong>24/7</strong><span>Continuous intelligence</span></div>
      </div>
    </section>

    <section id="features">
      <h2 class="section-title">Core capabilities</h2>
      <div class="grid">
        <div class="card"><h3>🧠 AI Discovery</h3><p>Identify code, modules, patterns and architecture without manual inspection.</p></div>
        <div class="card"><h3>🕸️ Graph Mapping</h3><p>Connect directories, files and modules into a relationship model for system understanding.</p></div>
        <div class="card"><h3>🔎 Reverse Engineering</h3><p>Reveal internal dependencies, structure and hidden system logic.</p></div>
        <div class="card"><h3>🎯 Identity Intelligence</h3><p>Model digital identities and trust relationships across entities and systems.</p></div>
        <div class="card"><h3>📊 Analytics</h3><p>Measure file counts, language mix, complexity and architecture signals.</p></div>
        <div class="card"><h3>📦 GitHub Support</h3><p>Analyze public GitHub repositories directly with a URL and inspect the structure instantly.</p></div>
      </div>
    </section>

    <section id="demo">
      <h2 class="section-title">Live result</h2>
      <div id="result" class="result-box">Waiting for analysis...</div>
    </section>

    <section id="pricing">
      <h2 class="section-title">Pricing</h2>
      <div class="pricing">
        <div class="price-card">
          <h3>Starter</h3>
          <div class="price">$29<span style="font-size:1rem;">/mo</span></div>
          <p>For developers and small teams.</p>
        </div>
        <div class="price-card featured">
          <h3>Professional</h3>
          <div class="price">$149<span style="font-size:1rem;">/mo</span></div>
          <p>For teams needing repository intelligence and analysis.</p>
        </div>
        <div class="price-card">
          <h3>Enterprise</h3>
          <div class="price">Custom</div>
          <p>For compliance, transformation and enterprise systems.</p>
        </div>
      </div>
    </section>

    <footer>
      <p>Built with AI, graph intelligence, and reverse engineering.</p>
      <p><a href="https://github.com/AMMARICA1791/ai-research-agents">GitHub</a> · <a href="mailto:enterprise@ai-research-agents.io">Contact</a></p>
    </footer>
  </div>

  <script>
    const form = document.getElementById('repo-form');
    const resultBox = document.getElementById('result');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const raw = document.getElementById('repo_path').value.trim() || '.';
      resultBox.textContent = 'Analyzing repository...';

      try {
        let endpoint = '/api/analyze';
        const isGithubUrl = raw.includes('github.com') || raw.includes('http://') || raw.includes('https://');
        if (isGithubUrl) {
          endpoint = '/api/analyze/url';
        }

        const data = new URLSearchParams();
        if (isGithubUrl) {
          data.append('url', raw);
        } else {
          data.append('repo_path', raw);
        }

        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: data.toString(),
        });

        const payload = await res.json();
        if (!res.ok) {
          throw new Error(payload.detail || 'Error analyzing repository');
        }

        resultBox.textContent = JSON.stringify(payload, null, 2);
      } catch (error) {
        resultBox.textContent = 'Error: ' + error.message;
      }
    });
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return HTML_INTERFACE


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
            content = await file.read()
            zip_path.write_bytes(content)
            extract_dir = Path(tmpdir) / "extracted"
            extract_dir.mkdir()
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(extract_dir)
            report = analyze_repository(extract_dir)
            return JSONResponse(content=report)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "ai-research-agents-mvp", "version": "0.2.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
