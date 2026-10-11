from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import re
import os
import zipfile
import tempfile

app = FastAPI(
    title="AI Research Agents MVP",
    version="0.1.0",
    description="Intelligent System Analysis Platform"
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
    ignore = {".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache", ".mypy_cache", ".idea", ".vscode", "dist", "build", ".env"}
    return bool(parts & ignore)


def _language_for(path: Path) -> str:
    ext = path.suffix.lower()
    map_ext = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".md": "Markdown", ".json": "JSON", ".yml": "YAML",
        ".yaml": "YAML", ".txt": "Text", ".toml": "TOML",
        ".ini": "INI", ".csv": "CSV", ".html": "HTML",
        ".css": "CSS", ".go": "Go", ".rs": "Rust",
        ".java": "Java", ".cpp": "C++", ".c": "C",
    }
    return map_ext.get(ext, "Other")


def _extract_python_stats(file_path: Path, text: str) -> Dict[str, Any]:
    class_count = len(re.findall(r"^\s*class\s+[A-Za-z_][A-Za-z0-9_]*", text, flags=re.MULTILINE))
    function_count = len(re.findall(r"^\s*def\s+[A-Za-z_][A-Za-z0-9_]*", text, flags=re.MULTILINE))
    import_count = len(re.findall(r"^(?:from\s+[A-Za-z0-9_\.]+\s+import|import\s+[A-Za-z0-9_\.]+)", text, flags=re.MULTILINE))
    return {
        "classes": class_count,
        "functions": function_count,
        "imports": import_count,
    }


def analyze_repository(repo_root: Path, max_files: int = 1000) -> Dict[str, Any]:
    repo_root = repo_root.resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        raise HTTPException(status_code=400, detail=f"Invalid path: {repo_root}")

    files = []
    modules = []
    graph_nodes = []
    graph_edges = []
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
                stats = _extract_python_stats(path, content)
                modules.append({
                    "path": rel,
                    "name": rel.replace("/", ".")[:-3],
                    **stats,
                })

            file_count += 1
        except Exception:
            pass

    language_dist = {}
    for f in files:
        lang = f["language"]
        language_dist[lang] = language_dist.get(lang, 0) + 1

    total_lines = sum(f["lines"] for f in files)
    python_files = sum(1 for f in files if f["language"] == "Python")

    summary = {
        "repo_name": repo_root.name,
        "repo_path": str(repo_root),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_files": len(files),
        "python_files": python_files,
        "total_lines": total_lines,
        "languages": language_dist,
    }

    return {
        "status": "ok",
        "summary": summary,
        "files": files,
        "modules": modules,
        "graph": {"nodes": graph_nodes[:500], "edges": graph_edges[:1000]},
    }


HTML_INTERFACE = open("landing_page.html").read() if os.path.exists("landing_page.html") else "<h1>AI Research Agents</h1>"


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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "ai-research-agents-mvp", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
