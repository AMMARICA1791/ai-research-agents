# Verified MVP release

This release adds an automated integration test suite, repairs the misplaced Python
modules and import errors, and restricts local repository inspection to the current
project tree. Archive uploads are limited to 10 MB compressed and 50 MB extracted
with traversal/symlink checks. The development server binds to localhost by default.

The web service exposes /health, /, /pricing, /api/demo, /api/analyze,
/api/analyze/url, /api/analyze/upload and /api/report. The GitHub analyzer
inspects repository file names and metadata, not the complete source semantics.

Run locally with:
  pip install -r requirements.txt
  python main.py

Validate with:
  python -m compileall -q agents research experiments web main.py run_server.py
  pytest -q tests/test_mvp.py

The agents still produce demonstration/static example data, not verified external
AI research. This MVP is not an independently deployed hosted SaaS product.

## Reproducible baseline identity (historical, not a fresh test)

- Baseline candidate: experimental v0.1.0.
- Baseline source commit: [`c6e86db7aecc7c73b12a18715ee2b4802545352d`](https://github.com/AMMARICA1791/ai-research-agents/commit/c6e86db7aecc7c73b12a18715ee2b4802545352d).
- Commit date (GitHub record): 2026-10-11 (UTC).
- Recorded verification at that point: the commit message reports 149 tests passing, synthetic red/green experiments, and a local HTTP smoke test before merge. This is **historical commit-message evidence**, not an independently rerun test in this documentation update.
- Subsequent development: Phase 7A scholarly metadata discovery was merged in commit `0e09698ca0629bc48f2aa51029ed6a4fd9fbd8b4`; it is **not** part of the frozen baseline above.
- Release tag and release artifact: **not verified by this document**. Do not infer either from a filename or commit message.

To independently verify a candidate release, check out its exact SHA, record Python version and UTC time, run `python -m pytest -q tests/` and the three commands in [DEMO.md](DEMO.md), then record exact outputs and failures. Do not label a later commit as tested using the baseline's results.
