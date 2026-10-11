# Research Lab Quick Start

GitHub: Actions → Research Lab - Manual Mission → Run workflow.
Enter a goal and download the resulting report artifact.
No language-model API key is required for deterministic source analysis.

Locally:
    pip install -r requirements.txt
    python main.py
    python -m lab.cli mission --repo . --goal "Review this laboratory"
    python -m pytest -q tests/test_mvp.py tests/test_lab.py

Dashboard: http://127.0.0.1:8000
History: .data/lab.sqlite on that machine. GitHub Actions uses
independent per-run memory until a shared store is provided.
Optional model commentary requires explicitly configured LAB_LLM_ENDPOINT,
LAB_LLM_MODEL, and LAB_LLM_API_KEY. Never commit credentials.
