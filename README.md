# AI Research Agents — Independent Research & Development Laboratory

This is an internal research center, not a commercial SaaS product.

## Implemented

The new lab/ package runs five ordered research stages:
1. Explorer — bounded read-only file inventory.
2. Analyst — real Python AST inspection with file/line evidence.
3. Engineer — creates proposed actions, without changing source code.
4. Validator — checks proposals against evidence.
5. Synthesizer — produces a report and saves SQLite history.

An optional OpenAI-compatible model comments on finding metadata when
LAB_LLM_ENDPOINT, LAB_LLM_MODEL and LAB_LLM_API_KEY are configured.
Otherwise the lab performs deterministic research and explicitly reports
that language-model inference is not configured. Original agents under
agents/ remain demonstration implementations.

## On GitHub, including an Android tablet

Open Actions → Research Lab - Manual Mission → Run workflow.
Enter a research goal. Download mission.json and SQLite from run Artifacts.
Each GitHub Actions run starts with fresh SQLite memory; a long-term cloud
database is planned for a later phase.

## Local setup

Python 3.11+:

    pip install -r requirements.txt
    python main.py

Dashboard: http://127.0.0.1:8000

    python -m lab.cli mission --repo . --goal "Inspect this research laboratory"
    python -m lab.cli history
    python -m lab.cli proposals
    python -m pytest -q tests/test_mvp.py tests/test_lab.py

All source change proposals require human review; approval does not
automatically edit code, open PRs or merge. This is an early research
foundation, not a full autonomous coding agent or security audit.
Do not publish its HTTP interface without authentication.

See docs/RESEARCH_LAB_VISION.md, docs/MISSION_PROTOCOL.md and README.ar.md.
Past business, investor and pricing drafts are preserved under
archive/commercial-drafts/ and are not part of this phase.

License: MIT.
