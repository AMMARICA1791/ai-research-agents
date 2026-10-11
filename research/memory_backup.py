"""Verified local SQLite evidence backup and conservative restore.

Backups use SQLite's online backup API; restore refuses existing destinations.
No remote synchronization, key management, or disaster-recovery guarantee.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import tempfile
from pathlib import Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _verify(conn: sqlite3.Connection) -> dict:
    if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise ValueError("SQLite integrity check failed")
    if conn.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("SQLite foreign-key check failed")
    required = {"evidence_snapshots", "evidence_entries"}
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if not required.issubset(tables):
        raise ValueError("Missing evidence memory tables")
    snapshots = conn.execute("SELECT count(*) FROM evidence_snapshots").fetchone()[0]
    entries = conn.execute("SELECT count(*) FROM evidence_entries").fetchone()[0]
    for digest, payload in conn.execute("SELECT ledger_sha256, payload_json FROM evidence_snapshots"):
        ledger = json.loads(payload)
        unsigned = {k: v for k, v in ledger.items() if k != "ledger_sha256"}
        canonical = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        if digest != expected or ledger.get("ledger_sha256") != digest:
            raise ValueError("Stored evidence ledger digest mismatch")
    return {"snapshots": snapshots, "entries": entries}


def _inspect(path: Path) -> dict:
    # SQLite read-only URI avoids silently creating an absent or invalid DB.
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as conn:
        return _verify(conn)


def backup(source: str | Path, destination: str | Path) -> dict:
    src, dst = Path(source), Path(destination)
    if not src.is_file() or src.resolve() == dst.resolve():
        raise ValueError("Source database missing or destination matches source")
    if dst.exists() or dst.with_name(dst.name + ".manifest.json").exists():
        raise FileExistsError("Backup or manifest already exists")
    _inspect(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(prefix=".research-backup-", suffix=".sqlite3",
                                         dir=dst.parent, delete=False) as temp:
            temp_path = Path(temp.name)
        with sqlite3.connect(src.resolve().as_uri() + "?mode=ro", uri=True) as original:
            with sqlite3.connect(temp_path) as copy:
                original.backup(copy)
        counts = _inspect(temp_path)
        digest = _sha256(temp_path)
        manifest = {"schema_version": 1, "backup_sha256": digest, **counts}
        # Exclusive creation: never overwrite a pre-existing backup.
        with dst.open("xb") as target, temp_path.open("rb") as incoming:
            for block in iter(lambda: incoming.read(1024 * 1024), b""):
                target.write(block)
            target.flush()
            os.fsync(target.fileno())
        with dst.with_name(dst.name + ".manifest.json").open("x", encoding="utf-8") as target:
            json.dump(manifest, target, sort_keys=True, indent=2)
            target.write("\n")
            target.flush()
            os.fsync(target.fileno())
        return manifest
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def restore(source: str | Path, destination: str | Path) -> dict:
    src, dst = Path(source), Path(destination)
    if not src.is_file() or dst.exists() or src.resolve() == dst.resolve():
        raise ValueError("Backup missing, destination exists, or paths overlap")
    manifest_path = src.with_name(src.name + ".manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (manifest.get("schema_version") != 1 or
            manifest.get("backup_sha256") != _sha256(src)):
        raise ValueError("Backup manifest mismatch")
    counts = _inspect(src)
    if any(counts[key] != manifest.get(key) for key in ("snapshots", "entries")):
        raise ValueError("Backup record counts differ")
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive copy to avoid replacing a live database. Remove partial output on failure.
    created = False
    try:
        with dst.open("xb") as output:
            created = True
            with src.open("rb") as incoming:
                for block in iter(lambda: incoming.read(1024 * 1024), b""):
                    output.write(block)
            output.flush()
            os.fsync(output.fileno())
        if _sha256(dst) != manifest["backup_sha256"] or _inspect(dst) != counts:
            raise ValueError("Restored database failed verification")
    except Exception:
        if created:
            dst.unlink(missing_ok=True)
        raise
    return {"restored": True, "backup_sha256": manifest["backup_sha256"], **counts}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Local verified research memory backup and restore")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("backup", "restore"):
        command = commands.add_parser(name)
        command.add_argument("--source", required=True)
        command.add_argument("--destination", required=True)
    args = parser.parse_args(argv)
    result = backup(args.source, args.destination) if args.command == "backup" else restore(args.source, args.destination)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
