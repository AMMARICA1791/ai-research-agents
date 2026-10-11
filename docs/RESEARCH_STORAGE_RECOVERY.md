# Research evidence storage: integrity and recovery gates

This phase tests the **existing** SQLite evidence memory without changing its production behavior.

## Offline regression

```sh
python -m pytest -q tests/test_research_memory_recovery.py tests/test_research_integration.py
```

The tests cover reopening a committed store, SQLite integrity checks, atomic rollback on a deliberately rejected entry insert, foreign-key enforcement, idempotent replay, and explicit failure on invalid SQLite bytes. A corrupt database must **not** be silently overwritten or treated as an empty store.

## Boundaries

These are deterministic failure-injection tests, not proof against power loss, filesystem corruption, disk-full errors, or simultaneous writers. This PR does **not** implement backup or automatic recovery. Before using important research records in production, add a verified SQLite backup/restore path, checksum manifest, recovery rehearsal, and tests for incomplete or tampered backups.

No scientific claims, LLM inference, or cross-paper contradiction detection is implied by passing these tests.
