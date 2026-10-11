# Public proof tour — review the results in one minute

This is a **small, verifiable demonstration** for developers encountering AI Research Agents for the first time. It does not require paid model keys, your own API keys, a laptop, or a hosted SaaS service.

## On GitHub (including an Android tablet)

1. Open [Public One-Click Proof Tour](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml).
2. Choose **Run workflow**, leave the branch as **main**, then confirm **Run workflow**.
3. Open the newest workflow run and inspect the **Summary** page and the job named **proof-tour**.
4. Look for **three bounded demonstrations**: an eight-case synthetic scanner benchmark, a synthetic before/after repair, and the before/after GitHub URL parser regression associated with [the actual Qwen-authored PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17).
5. Download the **public-proof** artifact for the machine-readable JSON and Markdown report. The artifact is temporary; rerun the workflow for new evidence.

Do not confuse the review of historical code with a new AI-generated fix: **this demo does not run an LLM**. It repeats tests against a reconstructed vulnerable version of the actual repository function and against its merged, repaired version. The real model inference and original patch are documented in PR #17.

## On a computer

Python 3.11+ and the cloned repository:

    python -m lab.public_demo --out results/public-demo

The command needs **no paid model API** and no third-party Python dependencies. Results are written to results/public-demo/evidence.json and results/public-demo/SUMMARY.md; this output directory is ignored by Git.

## Safety and claims

- Only bundled synthetic inputs and the repository's own known function are tested; no outside repository is executed.
- The read-only workflow has contents:read and cannot push to main or automatically create pull requests.
- The eight-case artificial scanner results do **not** measure accuracy on unseen production repositories.
- No new fix is generated in this demo; the previously model-authored code change remains in the historical PR.
- This demonstration is not a general autonomous programming agent or security certification.

Interested in contributing? See [CONTRIBUTING.md](../CONTRIBUTING.md), [ROADMAP.md](../ROADMAP.md) and [the code license](../LICENSE).
