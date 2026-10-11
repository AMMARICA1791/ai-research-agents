"""Bounded read-only inspection of an arbitrary PUBLIC GitHub Python repository.

No clone, imports, shell commands, external code execution or private tokens.
HTTPS requests only to exact GitHub API/codeload hosts; compressed archives
are bounded and validated before extracting allowlisted files in a tempdir.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urljoin, urlsplit

import requests

from .dependency import analyze_internal_dependencies
from .inspector import ALLOWED, IGNORED, MAX_FILES, MAX_SOURCE_BYTES, PRIVATE, inspect_repository

MAX_ZIP_BYTES = 10_000_000
MAX_UNPACKED_BYTES = 30_000_000
MAX_ZIP_MEMBERS = 2500
MAX_REPORT_FINDINGS = 100
REF_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,99}\Z")
OWNER_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}\Z")
REPO_RE = re.compile(r"[A-Za-z0-9_-][A-Za-z0-9._-]{0,99}\Z")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
HTTP_HEADERS = {"User-Agent": "ai-research-agents-public-readonly-audit/1", "Accept": "application/vnd.github+json"}


def parse_public_github_url(raw: str) -> tuple[str, str]:
    if not isinstance(raw, str) or len(raw) > 220:
        raise ValueError("A short public GitHub URL is required")
    p = urlsplit(raw)
    if (p.scheme != "https" or p.hostname != "github.com" or p.netloc != "github.com"
            or p.query or p.fragment):
        raise ValueError("Only canonical https://github.com/OWNER/REPO URLs are supported")
    parts = p.path.strip("/").split("/")
    if len(parts) != 2 or p.path.endswith("/"):
        raise ValueError("Supply a repository URL without subpaths or a trailing slash")
    owner, name = parts
    if name.endswith(".git"):
        name = name[:-4]
    if (not OWNER_RE.fullmatch(owner) or not REPO_RE.fullmatch(name)
            or name.endswith(".") or ".." in name):
        raise ValueError("Invalid GitHub owner or repository name")
    return owner, name


def validate_ref(ref: str) -> str:
    if (not isinstance(ref, str) or not REF_RE.fullmatch(ref)
            or ".." in ref or "//" in ref or ref.endswith(("/", ".", ".lock"))
            or any(seg.startswith(".") for seg in ref.split("/"))):
        raise ValueError("Invalid public Git reference")
    return ref


def _get_limited(url: str, owner: str, name: str, byte_limit: int, redirects: int = 2) -> bytes:
    """Read only from github.com archive API or this exact codeload repository."""
    for redirect in range(redirects + 1):
        p = urlsplit(url)
        correct_api = (p.netloc == "api.github.com" and
                       p.path.startswith(f"/repos/{owner}/{name}/"))
        correct_archive = (p.netloc == "codeload.github.com" and
                           p.path.startswith(f"/{owner}/{name}/"))
        if (p.scheme != "https" or p.username or p.password or p.port is not None
                or p.query or p.fragment or not (correct_api or correct_archive)):
            raise ValueError("Rejected download redirect outside requested public GitHub repository")
        response = requests.get(
            url, headers=HTTP_HEADERS, allow_redirects=False, stream=True,
            timeout=(5, 25),
        )
        try:
            if response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get("Location", "")
                if not location or redirect == redirects:
                    raise ValueError("Invalid or excessive GitHub redirect")
                url = urljoin(url, location)
                continue
            if response.status_code != 200:
                raise ValueError(f"Public GitHub request failed with HTTP {response.status_code}")
            raw = io.BytesIO()
            for chunk in response.iter_content(chunk_size=65536):
                raw.write(chunk)
                if raw.tell() > byte_limit:
                    raise ValueError("Repository download exceeds bounded size limit")
            return raw.getvalue()
        finally:
            response.close()
    raise ValueError("Too many redirects")


def _safe_archive_path(name: str) -> tuple[str, ...]:
    if (not name or len(name) > 500 or name.startswith("/")
            or "\\" in name or "\x00" in name or "//" in name):
        raise ValueError("Invalid archive member path")
    parts = name.rstrip("/").split("/")
    if any(x in (".", "..", "") for x in parts):
        raise ValueError("Archive contains unsafe member path")
    return tuple(parts)


def _unpack_safe(zipped: bytes, root: Path) -> dict:
    accepted = 0
    skipped = 0
    truncated = False
    total_selected_bytes = 0
    prefixes = set()
    seen = set()
    try:
        archive = zipfile.ZipFile(io.BytesIO(zipped))
    except zipfile.BadZipFile as exc:
        raise ValueError("GitHub returned an invalid ZIP archive") from exc
    with archive:
        members = archive.infolist()
        if len(members) > MAX_ZIP_MEMBERS:
            raise ValueError("Archive has too many entries for safe inspection")
        if sum(x.file_size for x in members) > MAX_UNPACKED_BYTES:
            raise ValueError("Archive exceeds uncompressed inspection limit")
        for info in members:
            parts = _safe_archive_path(info.filename)
            prefixes.add(parts[0])
            if len(prefixes) != 1:
                raise ValueError("Archive has inconsistent repository roots")
            if info.is_dir() or len(parts) < 2:
                continue
            rel = parts[1:]
            normalized = PurePosixPath(*rel)
            # Symlinks and nonregular ZIP entries must never be extracted.
            file_type = stat.S_IFMT(info.external_attr >> 16)
            if file_type not in (0, stat.S_IFREG):
                skipped += 1
                continue
            if (any(part in IGNORED for part in rel[:-1])
                    or any(part.startswith(".env") for part in rel)
                    or rel[-1] in PRIVATE or rel[-1].startswith(".env")
                    or normalized.suffix.lower() not in ALLOWED
                    or info.file_size > MAX_SOURCE_BYTES):
                skipped += 1
                continue
            if normalized.as_posix() in seen:
                raise ValueError("Duplicate archive member would overwrite inspected source")
            seen.add(normalized.as_posix())
            if accepted >= MAX_FILES or total_selected_bytes + info.file_size > MAX_UNPACKED_BYTES:
                truncated = True
                break
            try:
                with archive.open(info) as src:
                    data = src.read(MAX_SOURCE_BYTES + 1)
            except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                raise ValueError("Corrupt or unreadable ZIP member") from exc
            if len(data) != info.file_size:
                raise ValueError("Archive member size mismatch")
            target = root.joinpath(*rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            total_selected_bytes += len(data)
            accepted += 1
    return {
        "files_extracted_for_static_scan": accepted,
        "skipped_entries": skipped,
        "archive_truncated": truncated,
        "zip_entries": len(members),
    }


def audit_public_repository(repository_url: str, ref: str = "HEAD") -> dict:
    owner, name = parse_public_github_url(repository_url)
    ref = validate_ref(ref)
    commit_url = f"https://api.github.com/repos/{owner}/{name}/commits/{quote(ref, safe='/')}"
    commit_body = _get_limited(commit_url, owner, name, 300_000)
    try:
        sha = json.loads(commit_body)["sha"]
    except (ValueError, KeyError, TypeError) as exc:
        raise ValueError("Could not resolve public repository commit") from exc
    if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
        raise ValueError("GitHub commit identifier is not valid")
    archive_url = f"https://api.github.com/repos/{owner}/{name}/zipball/{sha}"
    archive = _get_limited(archive_url, owner, name, MAX_ZIP_BYTES)
    with tempfile.TemporaryDirectory(prefix="ai-lab-public-audit-") as directory:
        root = Path(directory)
        limits = _unpack_safe(archive, root)
        scan = inspect_repository(root)
        deps = analyze_internal_dependencies(scan["files"])
    findings = scan["findings"][:MAX_REPORT_FINDINGS]
    for cycle in deps["cycles"]:
        if len(findings) < MAX_REPORT_FINDINGS:
            findings.append({
                "rule": "internal_dependency_cycle",
                "severity": "medium", "evidence": cycle[0],
                "message": "Internal module cycle: " + " -> ".join(cycle),
            })
    return {
        "schema_version": 1,
        "status": "read_only_public_repository_inspected",
        "repository": f"https://github.com/{owner}/{name}",
        "requested_ref": ref,
        "resolved_commit": sha,
        "archive_sha256": hashlib.sha256(archive).hexdigest(),
        "model_inference": False,
        "untrusted_code_executed": False,
        "source_modified": False,
        "scan_coverage": {
            **limits, "files_scanned": scan["files_scanned"],
            "python_files_parsed": scan["python_files_parsed"],
            "truncated": bool(limits["archive_truncated"] or scan["truncated"]),
        },
        "risk_counts": {
            level: sum(f["severity"] == level for f in findings)
            for level in ("high", "medium", "low")
        },
        "findings": findings,
        "dependencies": {"module_count": deps["module_count"],
                         "edge_count": deps["edge_count"],
                         "cycles": deps["cycles"]},
        "limitations": [
            "static Python AST heuristics, not a general vulnerability scan",
            "ZIP entry and size bounds can leave the scan incomplete",
            "no outside repository code is imported, executed or tested",
            "no autonomous model-generated patch was attempted",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Bounded read-only public GitHub code audit")
    parser.add_argument("--repo-url", required=True)
    parser.add_argument("--ref", default="HEAD", help="Public branch, tag or SHA; HEAD uses default")
    parser.add_argument("--output", default="results/public-repo-audit.json")
    args = parser.parse_args(argv)
    report = audit_public_repository(args.repo_url, args.ref)
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"], "repository": report["repository"],
        "resolved_commit": report["resolved_commit"],
        "coverage": report["scan_coverage"], "risks": report["risk_counts"],
        "model_inference": False, "untrusted_code_executed": False,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
