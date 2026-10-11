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
