"""Durable SQLite audit trail and explicit, human-gated proposals."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class LabMemory:
    def __init__(self, db_path: str | Path = ".data/lab.sqlite"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        with self.connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS missions (
                id TEXT PRIMARY KEY, goal TEXT NOT NULL, created_at TEXT NOT NULL,
                status TEXT NOT NULL, report_json TEXT NOT NULL)""")
            db.execute("""CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT, mission_id TEXT NOT NULL,
                stage TEXT NOT NULL, created_at TEXT NOT NULL, payload_json TEXT NOT NULL)""")
            db.execute("""CREATE TABLE IF NOT EXISTS proposals (
                id TEXT PRIMARY KEY, mission_id TEXT NOT NULL, title TEXT NOT NULL,
                evidence TEXT NOT NULL, status TEXT NOT NULL, updated_at TEXT NOT NULL)""")

    def save_mission(self, goal: str, report: dict, events: list[dict], proposals: list[dict]) -> str:
        mission_id = uuid4().hex
        with self.connect() as db:
            db.execute("INSERT INTO missions VALUES (?, ?, ?, ?, ?)",
                       (mission_id, goal, utc_now(), "completed", json.dumps(report, ensure_ascii=False)))
            for event in events:
                db.execute("INSERT INTO events (mission_id, stage, created_at, payload_json) VALUES (?, ?, ?, ?)",
                           (mission_id, event["stage"], utc_now(), json.dumps(event["result"], ensure_ascii=False)))
            for proposal in proposals:
                db.execute("INSERT INTO proposals VALUES (?, ?, ?, ?, ?, ?)",
                           (uuid4().hex, mission_id, proposal["title"], proposal["evidence"], "pending_review", utc_now()))
        return mission_id

    def list_missions(self, limit: int = 20) -> list[dict]:
        with self.connect() as db:
            rows = db.execute("SELECT id, goal, created_at, status FROM missions ORDER BY created_at DESC LIMIT ?", (max(1, min(limit, 100)),)).fetchall()
        return [dict(row) for row in rows]

    def get_mission(self, mission_id: str) -> dict | None:
        with self.connect() as db:
            mission = db.execute("SELECT * FROM missions WHERE id = ?", (mission_id,)).fetchone()
            if mission is None:
                return None
            events = db.execute("SELECT stage, payload_json FROM events WHERE mission_id = ? ORDER BY id", (mission_id,)).fetchall()
            proposals = db.execute("SELECT id, title, evidence, status FROM proposals WHERE mission_id = ? ORDER BY rowid", (mission_id,)).fetchall()
        return {**dict(mission), "report": json.loads(mission["report_json"]),
                "events": [{"stage": e["stage"], "result": json.loads(e["payload_json"])} for e in events],
                "proposals": [dict(row) for row in proposals]}

    def list_proposals(self, limit: int = 30) -> list[dict]:
        with self.connect() as db:
            rows = db.execute("SELECT id, mission_id, title, evidence, status FROM proposals ORDER BY updated_at DESC LIMIT ?", (max(1, min(limit, 100)),)).fetchall()
        return [dict(row) for row in rows]

    def decide(self, proposal_id: str, approve: bool) -> bool:
        with self.connect() as db:
            result = db.execute("UPDATE proposals SET status = ?, updated_at = ? WHERE id = ? AND status = ?",
                                ("approved" if approve else "rejected", utc_now(), proposal_id, "pending_review"))
        # Approval records the decision ONLY. It does not change source files or run commands.
        return result.rowcount == 1
