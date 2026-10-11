"""Regression tests for previously silent repository-scanning exceptions."""
import logging
from pathlib import Path

import pytest

from lab.inspector import inspect_repository
from web.app import analyze_repository


def test_unreadable_file_is_reported_and_valid_files_are_preserved(tmp_path, monkeypatch, caplog):
    (tmp_path / "good.py").write_text("def okay():\n    return 7\n", encoding="utf-8")
    (tmp_path / "restricted.py").write_text("def secret():\n    pass\n", encoding="utf-8")
    original_read_text = Path.read_text

    def reject_restricted(self, *args, **kwargs):
        if self.name == "restricted.py":
            raise PermissionError("PRIVATE_DETAIL_MUST_NOT_APPEAR")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", reject_restricted)
    with caplog.at_level(logging.WARNING, logger="web.app"):
        report = analyze_repository(tmp_path)

    assert report["status"] == "ok"
    assert report["summary"]["python_files"] == 1
    assert report["summary"]["skipped_file_count"] == 1
    assert report["skipped_files"] == [
        {"path": "restricted.py", "error_type": "PermissionError"}
    ]
    assert {x["path"] for x in report["files"]} == {"good.py"}
    assert all(x["id"] != "restricted.py" for x in report["graph"]["nodes"])
    assert all(x["path"] != "restricted.py" for x in report["modules"])
    assert "restricted.py" in caplog.text
    assert "PRIVATE_DETAIL_MUST_NOT_APPEAR" not in caplog.text


def test_bad_utf8_is_reported_instead_of_silently_ignored(tmp_path, caplog):
    (tmp_path / "valid.py").write_text("def valid():\n    return True\n", encoding="utf-8")
    (tmp_path / "corrupt.py").write_bytes(b"def broken():\n    return b'\xff'\n\xff")
    with caplog.at_level(logging.WARNING, logger="web.app"):
        report = analyze_repository(tmp_path)
    assert report["summary"]["python_files"] == 1
    assert report["summary"]["skipped_file_count"] == 1
    assert report["skipped_files"][0] == {
        "path": "corrupt.py", "error_type": "UnicodeDecodeError"
    }
    assert "corrupt.py" in caplog.text


def test_programming_defects_are_not_swallowed(tmp_path, monkeypatch):
    (tmp_path / "foo.py").write_text("def inspect():\n    return 4\n", encoding="utf-8")
    from importlib import import_module
    web_module = import_module('web.app')

    def unexpected_bug(_content):
        raise RuntimeError("Unexpected analyzer defect")

    monkeypatch.setattr(web_module, "_extract_python_stats", unexpected_bug)
    with pytest.raises(RuntimeError, match="Unexpected analyzer defect"):
        analyze_repository(tmp_path)


def test_self_inspector_does_not_flag_web_scanner_as_silent(tmp_path):
    web_root = Path(__file__).resolve().parents[1] / "web"
    findings = inspect_repository(web_root)["findings"]
    assert not any(f["rule"] == "silent_exception" for f in findings)
