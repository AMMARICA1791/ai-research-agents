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


HTML_LANDING = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Research Agents | Reverse Engineering & Intelligence Platform</title>
  <style>
    :root {
      --bg1: #061421;
      --bg2: #0c2033;
      --bg3: #112f47;
      --text: #edf6ff;
      --muted: #adc7db;
      --accent: #5da8ff;
      --accent-2: #82d9ff;
      --card: rgba(255,255,255,0.03);
      --line: rgba(255,255,255,0.08);
    }
    * { box-sizing:border-box; }
    body { margin:0; background:linear-gradient(135deg,var(--bg1),var(--bg2) 38%,var(--bg3)); color:var(--text); font-family: Inter, Segoe UI, Arial, sans-serif; }
    .container { max-width:1200px; margin:0 auto; padding:18px 20px 80px; }
    .nav { display:flex; justify-content:space-between; align-items:center; padding:14px 0 18px; border-bottom:1px solid var(--line); }
    .brand { font-weight:900; font-size:1.3rem; letter-spacing:-.04em; background:linear-gradient(135deg,#5da8ff,#82d9ff); -webkit-background-clip:text; color:transparent; }
    .nav a { color:#dfeeff; text-decoration:none; margin-left:18px; font-size:.96rem; }
    .hero { padding:78px 0 32px; text-align:center; }
    .tag { display:inline-block; padding:9px 16px; background:rgba(93,168,255,.14); border:1px solid rgba(93,168,255,.4); border-radius:999px; font-size:12px; letter-spacing:.08em; text-transform:uppercase; }
    h1 { margin:18px 0 12px; font-size:clamp(2.6rem,6vw,4.5rem); line-height:1.1; }
    .subtitle { max-width:760px; margin:0 auto; line-height:1.8; font-size:1.14rem; color:var(--muted); }
    .cta-row { display:flex; justify-content:center; flex-wrap:wrap; gap:14px; margin:30px 0 40px; }
    .btn { display:inline-block; padding:16px 24px; border-radius:12px; font-weight:800; text-decoration:none; }
    .btn.primary { background:linear-gradient(135deg,#4da3ff,#82d9ff); color:#061421; }
    .btn.secondary { background:transparent; border:1px solid rgba(93,168,255,.4); color:#8dc7ff; }
    .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:18px; margin-top:16px; }
    .stat { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:18px; text-align:center; }
    .stat strong { display:block; color:#82d9ff; font-size:1.9rem; margin-bottom:6px; }
    .stat span { color:var(--muted); }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:22px; margin-top:38px; }
    .card { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:26px; }
    .card h3 { margin:0 0 12px; }
    .card p { color:var(--muted); line-height:1.7; margin:0; }
    .section { margin-top:52px; }
    .section h2 { margin:0 0 18px; font-size:2.2rem; }
    .price-box { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:20px; }
    .price-card { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:24px; }
    .price-card.featured { background:rgba(93,168,255,.08); border-color:rgba(93,168,255,.4); }
    .price { font-size:2.1rem; font-weight:800; }
    ul { color:var(--muted); padding-left:18px; line-height:1.8; }
    .cta-panel { margin-top:54px; text-align:center; padding:52px 24px; background:rgba(93,168,255,.08); border:1px solid rgba(93,168,255,.2); border-radius:18px; }
    footer { margin-top:52px; border-top:1px solid var(--line); padding-top:26px; text-align:center; color:#9bb2c8; }
    a.link { color:#5da8ff; text-decoration:none; }
    @media (max-width:760px){ .nav{flex-direction:column; gap:10px;} .nav a{margin:0 8px;} .cta-row{display:block;} .btn{display:block; margin-bottom:10px;} }
  </style>
</head>
<body>
  <div class="container">
    <div class="nav">
      <div class="brand">AI Research Agents</div>
      <div>
        <a href="#features">Features</a>
        <a href="#pricing">Pricing</a>
        <a href="/pricing">Plans</a>
        <a href="mailto:enterprise@ai-research-agents.io">Contact</a>
      </div>
    </div>

    <section class="hero">
      <div class="tag">v0.3.0 • Active Platform</div>
      <h1>Reveal the hidden structure of digital systems.</h1>
      <p class="subtitle">
        AI-driven platform for repository intelligence, graph analysis, dependency discovery, reverse engineering,
        and identity-aware digital system understanding.
      </p>
      <div class="cta-row">
        <a class="btn primary" href="/">Launch analysis</a>
        <a class="btn secondary" href="/pricing">View plans</a>
      </div>
      <div class="stats">
        <div class="stat"><strong>100x</strong><span>Faster than manual review</span></div>
        <div class="stat"><strong>90%</strong><span>Lower cost than consulting</span></div>
        <div class="stat"><strong>95%+</strong><span>System visibility</span></div>
        <div class="stat"><strong>24/7</strong><span>Continuous intelligence</span></div>
      </div>
    </section>

    <section id="features" class="section">
      <h2>Core capabilities</h2>
      <div class="grid">
        <div class="card"><h3>🔍 Repository Discovery</h3><p>Scan any project or GitHub repository and identify every major structure, file group, and dependency.</p></div>
        <div class="card"><h3>🕸️ Graph Intelligence</h3><p>Map relationships between directories, files, modules, and code objects with a structure-first model.</p></div>
        <div class="card"><h3>⚙️ Reverse Engineering</h3><p>Surface architecture patterns, hidden connections, and logical system structure for deeper understanding.</p></div>
        <div class="card"><h3>🎯 Identity Mapping</h3><p>Model digital identities, entities, and trust relationships as connected intelligence.</p></div>
        <div class="card"><h3>📊 Analytics Engine</h3><p>Measure file counts, languages, module stats, and system complexity from the repository itself.</p></div>
        <div class="card"><h3>📦 GitHub & ZIP Input</h3><p>Analyze directly from a GitHub URL or from a compressed project archive.</p></div>
      </div>
    </section>

    <section id="pricing" class="section">
      <h2>Pricing</h2>
      <div class="price-box">
        <div class="price-card">
          <h3>Starter</h3>
          <div class="price">$29<span style="font-size:1rem;">/mo</span></div>
          <ul>
            <li>Basic repo analysis</li>
            <li>Single-project usage</li>
            <li>JSON output</li>
            <li>Email support</li>
          </ul>
          <p style="margin-top:20px;"><a class="btn secondary" href="/">Start now</a></p>
        </div>
        <div class="price-card featured">
          <h3>Professional</h3>
          <div class="price">$149<span style="font-size:1rem;">/mo</span></div>
          <ul>
            <li>Unlimited repo analysis</li>
            <li>GitHub URL support</li>
            <li>Advanced reporting</li>
            <li>Priority support</li>
          </ul>
          <p style="margin-top:20px;"><a class="btn primary" href="/">Launch analysis</a></p>
        </div>
        <div class="price-card">
          <h3>Enterprise</h3>
          <div class="price">Custom</div>
          <ul>
            <li>Custom integrations</li>
            <li>Private deployment</li>
            <li>Compliance guidance</li>
            <li>Dedicated support</li>
          </ul>
          <p style="margin-top:20px;"><a class="btn secondary" href="mailto:enterprise@ai-research-agents.io">Contact sales</a></p>
        </div>
      </div>
    </section>

    <section class="cta-panel">
      <h2>Ready to see the hidden architecture of your systems?</h2>
      <p style="color:var(--muted); margin:12px 0 24px;">Try the platform or book a product walkthrough.</p>
      <div class="cta-row">
        <a class="btn primary" href="/">Start free analysis</a>
        <a class="btn secondary" href="mailto:enterprise@ai-research-agents.io">Book demo</a>
      </div>
    </section>

    <footer>
      <p>Built for AI research, graph intelligence, reverse engineering, and system understanding.</p>
      <p><a class="link" href="https://github.com/AMMARICA1791/ai-research-agents">GitHub</a> · <a class="link" href="mailto:enterprise@ai-research-agents.io">Contact</a></p>
    </footer>
  </div>
</body>
</html>
"""


HTML_PRICING = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Research Agents | Pricing</title>
  <style>
    body { margin:0; background:linear-gradient(135deg,#061421,#0c2033,#112f47); color:#edf6ff; font-family:Inter,Segoe UI,Arial,sans-serif; }
    .wrap { max-width:1100px; margin:0 auto; padding:40px 20px 80px; }
    .nav { display:flex; justify-content:space-between; align-items:center; padding-bottom:18px; border-bottom:1px solid rgba(255,255,255,.1); }
    .brand { font-weight:900; background:linear-gradient(135deg,#5da8ff,#82d9ff); -webkit-background-clip:text; color:transparent; }
    .pricing { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:22px; margin-top:36px; }
    .card { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08); border-radius:16px; padding:26px; }
    .featured { background:rgba(93,168,255,.08); border-color:rgba(93,168,255,.4); }
    .price { font-size:2.2rem; font-weight:800; }
    .btn { display:inline-block; padding:12px 20px; border-radius:10px; text-decoration:none; font-weight:800; }
    .btn-primary { background:linear-gradient(135deg,#4da3ff,#82d9ff); color:#071821; }
    .btn-secondary { border:1px solid rgba(93,168,255,.4); color:#8dc7ff; background:transparent; }
    ul { color:#bfd5ed; line-height:1.9; padding-left:18px; }
    .hero { margin:38px 0 22px; }
    footer { text-align:center; color:#9bb2c8; margin-top:48px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="nav">
      <div class="brand">AI Research Agents</div>
      <div><a href="/" style="text-decoration:none; color:#8dc7ff;">Back to platform</a></div>
    </div>

    <div class="hero">
      <h1 style="font-size:clamp(2.2rem,5vw,3.6rem); margin:0 0 14px;">Simple, transparent pricing.</h1>
      <p style="color:#d8ebff; line-height:1.7; max-width:760px;">From individual analysis to enterprise-grade digital system intelligence, choose the level that matches your work.</p>
    </div>

    <div class="pricing">
      <div class="card">
        <h2>Starter</h2>
        <div class="price">$29<span style="font-size:1rem;">/mo</span></div>
        <p style="color:#bfd5ed;">For developers and researchers.</p>
        <ul>
          <li>Repository analysis</li>
          <li>Basic graph output</li>
          <li>1 active project</li>
          <li>Email support</li>
        </ul>
        <p style="margin-top:20px;"><a class="btn btn-primary" href="/">Start now</a></p>
      </div>

      <div class="card featured">
        <h2>Professional</h2>
        <div class="price">$149<span style="font-size:1rem;">/mo</span></div>
        <p style="color:#bfd5ed;">For product, engineering, and security teams.</p>
        <ul>
          <li>Unlimited repository analysis</li>
          <li>GitHub URL integration</li>
          <li>Report generation</li>
          <li>Priority support</li>
        </ul>
        <p style="margin-top:20px;"><a class="btn btn-primary" href="/">Launch analysis</a></p>
      </div>

      <div class="card">
        <h2>Enterprise</h2>
        <div class="price">Custom</div>
        <p style="color:#bfd5ed;">For digital transformation and enterprise intelligence.</p>
        <ul>
          <li>Private deployment</li>
          <li>Security review support</li>
          <li>Custom.dashboard</li>
          <li>Dedicated onboarding</li>
        </ul>
        <p style="margin-top:20px;"><a class="btn btn-secondary" href="mailto:enterprise@ai-research-agents.io">Contact sales</a></p>
      </div>
    </div>

    <footer>
      <p>AI Research Agents • Reverse engineering • Identity intelligence • Graph analysis</p>
    </footer>
  </div>
</body>
</html>
"""


def _render_json_report(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


@app.get("/", response_class=HTMLResponse)
def landing() -> str:
    return HTML_LANDING


@app.get("/pricing", response_class=HTMLResponse)
def pricing() -> str:
    return HTML_PRICING


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
