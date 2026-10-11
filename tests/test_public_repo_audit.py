"""Bounded public GitHub audits: tests prohibit outside hosts and code execution."""
from __future__ import annotations

import io
import json
import stat
import zipfile

import pytest

from lab.public_repo_audit import (
    MAX_ZIP_BYTES, _get_limited, _unpack_safe, audit_public_repository,
    parse_public_github_url, validate_ref,
)


def zipped(files: dict[str, bytes]) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as arc:
        for path, value in files.items():
            arc.writestr(path, value)
    return out.getvalue()


class FakeResponse:
    def __init__(self, status=200, content=b"", location=None):
        self.status_code = status
        self.content = content
        self.headers = {"Location": location} if location else {}
        self.closed = False

    def iter_content(self, chunk_size=65536):
        yield self.content

    def close(self):
        self.closed = True


@pytest.mark.parametrize("url", [
    "http://github.com/owner/repo",
    "https://evilgithub.com/owner/repo",
    "https://github.com.evil.org/owner/repo",
    "https://github.com@evil.org/owner/repo",
    "https://github.com/owner/repo/tree/main",
    "https://github.com/owner/repo?token=secret",
    "https://github.com:443/owner/repo",
    "https://github.com/owner/repo/",
    "https://github.com/owner/.git",
    "https://github.com/owner/../x",
    "https://github.com/owner/repo#fragment",
])
def test_repository_url_rejects_spoofing_or_ambiguous_forms(url):
    with pytest.raises(ValueError):
        parse_public_github_url(url)


def test_parses_canonical_public_urls():
    assert parse_public_github_url("https://github.com/Pallets/itsdangerous") == ("Pallets", "itsdangerous")
    assert parse_public_github_url("https://github.com/pallets/itsdangerous.git") == ("pallets", "itsdangerous")


@pytest.mark.parametrize("ref", [
    "../main", ".git/config", "main//sub", "main..bad",
    "feature%2fbad", "main;echo BAD", "HEAD?x=1", "bad branch", "", "/main",
])
def test_unsafe_refs_are_rejected(ref):
    with pytest.raises(ValueError):
        validate_ref(ref)


def test_safe_ref_values():
    assert validate_ref("HEAD") == "HEAD"
    assert validate_ref("release/1.0.0") == "release/1.0.0"
    assert validate_ref("a" * 40) == "a" * 40


def test_public_audit_without_network_execution_or_secrets(tmp_path, monkeypatch):
    marker = tmp_path / "must-not-be-created"
    malicious_source = ("from pathlib import Path\n"
                        f"Path({str(marker)!r}).write_text('executed')\n"
                        "try:\n    1/0\nexcept Exception:\n    pass\n")
    raw = zipped({
        "public-abcdef/README.md": b"public project",
        "public-abcdef/app.py": malicious_source.encode(),
        "public-abcdef/tests/test_ok.py": b"def test_good():\n    assert True\n",
        "public-abcdef/.env": b"API_TOKEN=SECRET_VALUE",
        "public-abcdef/archive/secret.py": b"API_TOKEN='SECRET_VALUE'",
    })
    sha = "a" * 40
    urls = []
    def fake_get(url, **kwargs):
        urls.append(url)
        assert kwargs["allow_redirects"] is False
        assert kwargs["stream"] is True
        assert "Authorization" not in kwargs.get("headers", {})
        if "/commits/HEAD" in url:
            return FakeResponse(content=json.dumps({"sha": sha}).encode())
        if "/zipball/" in url:
            return FakeResponse(status=302, location=f"https://codeload.github.com/example/public/legacy.zip/{sha}")
        if url.startswith("https://codeload.github.com/example/public/"):
            return FakeResponse(content=raw)
        raise AssertionError(f"Unexpected network URL: {url}")
    monkeypatch.setattr("lab.public_repo_audit.requests.get", fake_get)
    data = audit_public_repository("https://github.com/example/public")
    assert data["resolved_commit"] == sha
    assert data["repository"] == "https://github.com/example/public"
    assert data["model_inference"] is False
    assert data["untrusted_code_executed"] is False
    assert data["source_modified"] is False
    assert data["scan_coverage"]["python_files_parsed"] == 2
    assert any(f["rule"] == "silent_exception" and f["evidence"] == "app.py:5"
               for f in data["findings"])
    assert not marker.exists()
    assert "SECRET_VALUE" not in json.dumps(data)
    assert all("github.com" in u for u in urls)


@pytest.mark.parametrize("destination", [
    "https://github.com.evil.org/steal",
    "https://api.github.com.evil.org/repos/example/public/archive",
    "http://codeload.github.com/example/public/archive",
    "https://evil.github.com/example/public/archive",
    "https://codeload.github.com:443/example/public/archive",
    "https://codeload.github.com/another/repo/legacy.zip/x",
])
def test_rejects_any_archive_redirect_outside_requested_repo(monkeypatch, destination):
    monkeypatch.setattr(
        "lab.public_repo_audit.requests.get",
        lambda *_args, **_kwargs: FakeResponse(status=302, location=destination),
    )
    with pytest.raises(ValueError):
        _get_limited("https://api.github.com/repos/example/public/zipball/" + "a"*40,
                     "example", "public", MAX_ZIP_BYTES)


def test_bounded_download_stops_large_content(monkeypatch):
    monkeypatch.setattr(
        "lab.public_repo_audit.requests.get",
        lambda *_args, **_kwargs: FakeResponse(content=b"x" * 200),
    )
    with pytest.raises(ValueError, match="size limit"):
        _get_limited("https://api.github.com/repos/example/public/zipball/abc",
                     "example", "public", 100)


@pytest.mark.parametrize("bad", [
    "root/../escape.py", "root//duplicate.py", "root\\evil.py", "/root/file.py",
])
def test_zip_traversal_or_malformed_paths_fail_closed(tmp_path, bad):
    with pytest.raises(ValueError):
        _unpack_safe(zipped({bad: b"print('bad')"}), tmp_path)
    assert list(tmp_path.rglob("*.py")) == []


def test_no_zip_symlink_is_extracted(tmp_path):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as arc:
        item = zipfile.ZipInfo("root/link.py")
        item.create_system = 3
        item.external_attr = (stat.S_IFLNK | 0o777) << 16
        arc.writestr(item, "../secret.py")
        arc.writestr("root/tests/test_safe.py", "assert True\n")
    result = _unpack_safe(out.getvalue(), tmp_path)
    assert result["files_extracted_for_static_scan"] == 1
    assert not (tmp_path / "link.py").exists()


def test_different_roots_or_zip_bomb_fail_closed(tmp_path):
    with pytest.raises(ValueError, match="inconsistent"):
        _unpack_safe(zipped({"root/a.py": b"pass", "another/b.py": b"pass"}), tmp_path)
    huge = zipped({"root/oversize.py": b"a" * 30_000_001})
    with pytest.raises(ValueError, match="uncompressed"):
        _unpack_safe(huge, tmp_path)
