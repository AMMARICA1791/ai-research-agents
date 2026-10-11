# Laboratory Mission Protocol

1. Owner submits a research goal.
2. Explorer inventories permitted files without executing code.
3. Analyst checks actual Python AST and records path/line evidence.
4. Engineer proposes repairs without changing files.
5. Validator checks evidence.
6. Synthesizer records the mission in local SQLite.
7. Human review is mandatory before any change.

CLI: python -m lab.cli mission --repo . --goal "Audit this research laboratory"
GitHub Actions: Research Lab - Manual Mission is manually dispatched and exports a JSON report.
No unattended modifications; HTTP service binds to localhost by default.
