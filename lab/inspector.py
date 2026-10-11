"""Read-only repository inspection. No code execution, compilation or source upload."""
from __future__ import annotations

import ast
import os
from pathlib import Path

IGNORED = {
    ".git", ".venv", "venv", ".data", "__pycache__", ".pytest_cache",
    "node_modules", ".idea", ".vscode", "dist", "build", "archive",
}
PRIVATE = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519"}
ALLOWED = {".py", ".md", ".json", ".yml", ".yaml", ".toml", ".html", ".css", ".js", ".ts", ".txt"}
MAX_FILES = 400
MAX_SOURCE_BYTES = 180_000


def inspect_repository(root: Path) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Repository path must be a directory")
    entries, findings = [], []
    parsed = 0
    files_seen = 0
    truncated = False
    for folder, dirs, filenames in os.walk(root, topdown=True, followlinks=False):
        base = Path(folder)
        dirs[:] = sorted(d for d in dirs if d not in IGNORED and not (base / d).is_symlink())
        for filename in sorted(filenames):
            if files_seen >= MAX_FILES:
                truncated = True
                break
            path = base / filename
            if path.is_symlink() or filename in PRIVATE or filename.startswith(".env"):
                continue
            if path.suffix.lower() not in ALLOWED or path.stat().st_size > MAX_SOURCE_BYTES:
                continue
            rel = path.relative_to(root).as_posix()
            files_seen += 1
            entry = {"path": rel, "language": path.suffix.lower(), "bytes": path.stat().st_size}
            if path.suffix.lower() == ".py":
                try:
                    source = path.read_text("utf-8")
                except (UnicodeError, OSError):
                    findings.append({"rule": "unreadable_python", "severity": "low", "evidence": rel, "message": "Python file could not be decoded"})
                    entries.append(entry)
                    continue
                try:
                    tree = ast.parse(source, filename=rel)
                    parsed += 1
                    entry["functions"] = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree))
                    entry["classes"] = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
                    entry["imports"] = sorted({a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names} |
                                              {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module})
                    for n in ast.walk(tree):
                        if isinstance(n, ast.ExceptHandler) and len(n.body) == 1 and isinstance(n.body[0], ast.Pass):
                            findings.append({"rule": "silent_exception", "severity": "medium", "evidence": f"{rel}:{n.lineno}", "message": "Exception handler silently discards errors"})
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {"eval", "exec"}:
                            findings.append({"rule": "dynamic_execution", "severity": "medium", "evidence": f"{rel}:{n.lineno}", "message": "Dynamic execution requires manual review"})
                except SyntaxError as e:
                    findings.append({"rule": "syntax_error", "severity": "high", "evidence": f"{rel}:{e.lineno or 1}", "message": e.msg})
            entries.append(entry)
        if truncated:
            break
    if not any(e["path"].startswith("tests/") and e["path"].endswith(".py") for e in entries):
        findings.append({"rule": "missing_tests", "severity": "medium", "evidence": ".", "message": "No Python tests directory found in inspected tree"})
    if truncated:
        findings.append({"rule": "inspection_limit", "severity": "low", "evidence": ".", "message": "Inspection reached the file-count limit"})
    findings = sorted(findings, key=lambda f: ({"high": 0, "medium": 1, "low": 2}[f["severity"]], f["evidence"]))[:100]
    return {
        "root": root.name,
        "files_scanned": files_seen,
        "python_files_parsed": parsed,
        "truncated": truncated,
        "files": entries,
        "findings": findings,
        "sources": sorted(e["path"] for e in entries),
    }
