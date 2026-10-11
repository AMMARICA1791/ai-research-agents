# Verified local evidence memory backup and restore

Experimental offline backup uses Python SQLite's **online backup API** (not a live database file copy), and produces a standalone SQLite snapshot plus `<backup>.manifest.json` containing SHA-256 and row counts.

```sh
python -m research.memory_backup backup --source results/research-memory.sqlite3 --destination results/research-memory-backup.sqlite3
python -m research.memory_backup restore --source results/research-memory-backup.sqlite3 --destination results/research-memory-restored.sqlite3
python -m pytest -q tests/test_research_memory_backup.py
```

Restore checks the SHA-256 manifest, SQLite integrity and foreign-key checks, ledger content digests, record counts, and the copied output. It **refuses to overwrite an existing database**. Use a fresh destination, then point the application to the restored path only after verification. Backups must be stored separately from the original database for meaningful recovery.

## Limits and security

- This is local snapshot/restore, not scheduled backups, offsite disaster recovery, encryption, authentication, concurrent restore coordination, or full crash/power-loss simulation.
- SHA-256 in a sidecar manifest detects accidental changes **but does not authenticate an attacker who can edit both files**.
- Restore is deliberately non-destructive; operators must manage database cutover, retention and access permissions.
- Backup publication is not an atomic two-file operation; interrupted backup may leave an incomplete snapshot without a manifest. Such snapshots must never be restored.
- Keep database files and backups out of public commits and logs. Never ingest secrets or private research data into public CI fixtures.
