# AI Research Agents — Internal Research & Development Laboratory

An owner-directed multi-role R&D environment, currently for internal experimentation — not a commercial offering.

## Phase 2: implemented foundations
- Seven coordinated research roles: Explorer, Analyst, Dependency Mapper, Engineer, Critic, Validator, Synthesizer.
- Read-only Python AST source analysis and conservative internal import-cycle mapping with file evidence.
- SQLite mission reports and human-gated proposed actions. Approving proposals never changes source code.
- Durable **sanitized** cross-run research summaries on a separate lab-memory branch. No raw goals, source or private SQLite history is committed there.
- Optional two-pass language-model critique using an explicitly configured OpenAI-compatible HTTPS provider. Unconfigured by default; no claims of live model execution without evidence.
- Manual and initial main-branch GitHub Actions workflow that executes a research mission and uploads its report.

## Tablet workflow
Open **Actions → Research Lab - Persistent Missions → Run workflow**. Enter a non-sensitive goal. Review the logs and mission artifact. Future runs restore aggregate prior findings from lab-memory.

## Locally
Python 3.11+:

    pip install -r requirements.txt
    python main.py
    python -m lab.cli mission --repo . --goal "Review our laboratory" --knowledge .data/knowledge.json
    python -m pytest -q tests/test_mvp.py tests/test_lab.py

Local dashboard: http://127.0.0.1:8000.

## Optional real AI reasoning
In repository Settings → Secrets and variables → Actions, explicitly add variables LAB_LLM_ENDPOINT, LAB_LLM_MODEL, plus a repository secret LAB_LLM_API_KEY. Then opt in using enable_model=true on manual runs. May incur provider charges. GitHub Models was retired in July 2026 and is not used. The model is given only aggregate finding counts, no source/goal text.

Public repository safety: GitHub Actions artifacts may reveal report details. Do not use private or sensitive mission goals. No automatic source edits or public web deployment.

Read [Phase 2 guide](docs/PHASE2_GUIDE.md) and [Arabic instructions](README.ar.md). Historical commercial materials remain archived.
