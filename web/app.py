from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from datetime import datetime, timezone
import json
import re
from typing import Any, Dict, List

app = FastAPI(title="AI Research Agents MVP", version="0.1.0")


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
    ignore = {".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache", ".mypy_cache", ".idea", ".vscode", "dist", "build"}
    return bool(parts & ignore)


def _language_for(path: Path) -> str:
    ext = path.suffix.lower()
    map_ext = {
        ".py": "Python",
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
        ".js": "JavaScript",
        ".ts": "TypeScript",
    }
    return map_ext.get(ext, "Other")


def _extract_python_stats(file_path: Path, text: str) -> Dict[str, Any]:
    class_count = len(re.findall(r"^\s*class\s+[A-Za-z_][A-Za-z0-9_]*", text, flags=re.MULTILINE))
    function_count = len(re.findall(r"^\s*def\s+[A-Za-z_][A-Za-z0-9_]*", text, flags=re.MULTILINE))
    import_count = len(re.findall(r"^(?:from\s+[A-Za-z0-9_\.]+\s+import\s+.+|import\s+[A-Za-z0-9_\.]+)", text, flags=re.MULTILINE))
    return {
        "class_count": class_count,
        "function_count": function_count,
        "import_count": import_count,
        "module_name": file_path.relative_to(file_path.parents[0]).as_posix() if file_path.parent == file_path.parents[0] else file_path.relative_to(file_path.parents[0]).as_posix(),
    }


def analyze_repository(repo_root: Path) -> Dict[str, Any]:
    repo_root = repo_root.resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        raise HTTPException(status_code=400, detail=f"Path does not exist or is not a directory: {repo_root}")

    files: List[Dict[str, Any]] = []
    modules: List[Dict[str, Any]] = []
    graph_nodes: List[Dict[str, Any]] = []
    graph_edges: List[Dict[str, Any]] = []

    top_dirs = sorted({p.name for p in repo_root.iterdir() if p.is_dir() and not _is_ignored(p)})

    for path in sorted(repo_root.rglob("*")):
        if path.is_dir():
            if _is_ignored(path):
                continue
            node_id = path.relative_to(repo_root).as_posix() or "."
            graph_nodes.append({"id": node_id, "label": path.name, "type": "directory"})
            continue

        if _is_ignored(path):
            continue

        rel = path.relative_to(repo_root).as_posix()
        lang = _language_for(path)
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            content = fh.read()

        line_count = len(content.splitlines())

        file_entry = {
            "path": rel,
            "language": lang,
            "size_bytes": path.stat().st_size,
            "line_count": line_count,
            "is_readme": path.name.lower().startswith("readme"),
            "is_python": path.suffix.lower() == ".py",
        }
        files.append(file_entry)

        graph_nodes.append({"id": rel, "label": path.name, "type": "file"})
        parent = path.parent.relative_to(repo_root).as_posix()
        if parent and parent != ".":
            graph_edges.append({"source": parent, "target": rel, "label": "contains"})

        if path.suffix.lower() == ".py":
            stats = _extract_python_stats(path, content)
            modules.append({
                "path": rel,
                "module_name": rel.replace("/", ".").replace("\\", ".")[:-3],
                "class_count": stats["class_count"],
                "function_count": stats["function_count"],
                "import_count": stats["import_count"],
            })

    readme_files = [f["path"] for f in files if f["is_readme"]]
    readme_title = ""
    if readme_files:
        readme_path = repo_root / readme_files[0]
        with readme_path.open("r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                if line.strip() and not line.startswith("#"):
                    continue
                if line.startswith("#"):
                    readme_title = line.strip("# ")
                    break

    repo_name = repo_root.name
    python_count = sum(1 for f in files if f["language"] == "Python")
    markdown_count = sum(1 for f in files if f["language"] == "Markdown")
    total_lines = sum(f["line_count"] for f in files)

    summary = {
        "repo_name": repo_name,
        "repo_path": str(repo_root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files),
        "python_files": python_count,
        "markdown_files": markdown_count,
        "total_lines": total_lines,
        "top_level_directories": top_dirs,
        "readme_title": readme_title,
        "research_focus": {
            "ai_research": "yes" if "agent" in repo_name.lower() or python_count > 0 else "possible",
            "reverse_engineering": "yes" if any("engineer" in f["path"].lower() for f in files) or "reverse" in repo_name.lower() else "possible",
            "digital_identity": "yes" if any("identity" in f["path"].lower() for f in files) or "identity" in repo_name.lower() else "possible",
        },
    }

    return {
        "status": "ok",
        "summary": summary,
        "files": files,
        "modules": modules,
        "graph": {"nodes": graph_nodes, "edges": graph_edges},
    }


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Research Agents MVP</title>
    <style>
      body {
        font-family: Inter, Arial, sans-serif;
        margin: 0;
        background: linear-gradient(135deg, #061421, #0c2033 40%, #112f47);
        color: #edf6ff;
      }
      .container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 48px 20px 80px;
      }
      .hero {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
        padding: 28px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.22);
      }
      .tag {
        display: inline-block;
        padding: 8px 12px;
        background: rgba(93, 168, 255, 0.15);
        border: 1px solid rgba(93,168,255,0.4);
        border-radius: 999px;
        font-size: 12px;
        letter-spacing: 0.08em;
        margin-bottom: 18px;
        text-transform: uppercase;
      }
      h1 {
        margin: 0 0 18px;
        font-size: clamp(2rem, 5vw, 4rem);
      }
      p {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #dfeeff;
      }
      form {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 20px;
      }
      input {
        flex: 1 1 700px;
        padding: 16px 18px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.14);
        background: rgba(7, 17, 27, 0.7);
        color: white;
        font-size: 1rem;
      }
      button {
        padding: 16px 22px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(135deg, #4da3ff, #82d9ff);
        color: #071821;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
      }
      .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-top: 32px;
      }
      .stat {
        padding: 20px;
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
      }
      .stat strong {
        display: block;
        font-size: 1.75rem;
        margin-bottom: 8px;
        color: #95d9ff;
      }
      pre {
        white-space: pre-wrap;
        word-break: break-word;
        margin-top: 18px;
        background: rgba(2, 11, 18, 0.75);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 18px;
        overflow: auto;
      }
      .muted {
        color: #adc7db;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="hero">
        <div class="tag">AI Research Agent MVP</div>
        <h1>Reveal the hidden architecture of digital systems.</h1>
        <p>
          This lightweight research engine analyzes a repository, extracts file structure,
          highlights Python modules, builds a relationship graph, and presents a clear technical summary.
        </p>

        <form id="analyze-form">
          <input id="repo_path" name="repo_path" value="." placeholder="Enter repo path or use '.' for current project" />
          <button type="submit">Analyze</button>
        </form>

        <div class="stats">
          <div class="stat"><strong>AI</strong><span class="muted">Research pipeline</span></div>
          <div class="stat"><strong>Graph</strong><span class="muted">Relationship mapping</span></div>
          <div class="stat"><strong>Reverse</strong><span class="muted">Engineering insight</span></div>
          <div class="stat"><strong>Identity</strong><span class="muted">Digital intelligence</span></div>
        </div>
      </div>

      <pre id="result">Waiting for analysis...</pre>
    </div>

    <script>
      const form = document.getElementById('analyze-form');
      const resultBox = document.getElementById('result');

      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const value = document.getElementById('repo_path').value.trim() || '.';
        resultBox.textContent = 'Analyzing repository...';

        try {
          const formData = new URLSearchParams();
          formData.append('repo_path', value);

          const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData.toString(),
          });

          const payload = await response.json();
          if (!response.ok) {
            throw new Error(payload.detail || 'Something went wrong');
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
def root() -> HTMLResponse:
    return HTMLResponse(content=HTML_PAGE)


@app.get("/api/demo")
def api_demo() -> JSONResponse:
    return JSONResponse(content=analyze_repository(Path.cwd()))


@app.post("/api/analyze")
def api_analyze(repo_path: str = Form(...)) -> JSONResponse:
    target = _safe_repo_path(repo_path)
    report = analyze_repository(target)
    return JSONResponse(content=report)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "ai-research-agents-mvp"}
