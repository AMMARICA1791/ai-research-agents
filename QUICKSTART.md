# Quick start

**No laptop or setup required for the public proof:** open [Public One-Click Proof Tour](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml) → **Run workflow** → **Summary**. It rechecks known test evidence; it does not generate new AI patches. See [public demo guide](docs/PUBLIC_DEMO.md).

## On an Android tablet

1. Open [GitHub Actions](https://github.com/AMMARICA1791/ai-research-agents/actions).
2. Choose **Research Lab - Persistent Missions** → **Run workflow**.
3. Enter a non-sensitive goal, for example: "Audit our research laboratory".
4. Read the results and download the report artifact.

This runs static analysis, **not** automatic code repair. For genuine local open-weight Qwen review, choose **Zero-Key Local Qwen Research**. No paid LLM API key is required for either default workflow, but runner resources have limits.

## On a computer with Python 3.11+

```sh
git clone https://github.com/AMMARICA1791/ai-research-agents.git
cd ai-research-agents
python -m pip install -r requirements.txt
python -m pytest -q tests/
python -m lab.cli mission --repo . --goal "Inspect this research lab"
python main.py
```

Open http://127.0.0.1:8000 locally.

**Results:** `not_configured` means no model was used. The `lab-memory` branch stores allowlisted summary counts, not private research content. Public workflow reports may expose details, so do not enter secrets, passwords, or private source. See [scope](docs/PROJECT_SCOPE.md).