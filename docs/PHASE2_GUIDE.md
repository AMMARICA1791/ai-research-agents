# Phase 2 — Research reasoning, cross-run knowledge and deeper code mapping

## What was built
- Seven ordered research roles: Explorer, Analyst, Dependency Mapper, Engineer, Critic, Validator, Synthesizer.
- Real Python AST inspection and conservative internal-import cycle detection.
- Durable **sanitized aggregate** history on a separate Git branch, lab-memory.
- Two *optional* external language-model reviewers (research analyst and skeptic), with strict bounded prompts containing only rule counts.
- No autonomous code edits, pushes to main or PR merges. Research findings are proposals.

## How persistent memory works
The main-branch workflow restores knowledge/state.json from lab-memory, runs the mission and writes only redacted totals back to lab-memory. Concurrency is serialized for that workflow. The public branch contains timestamps, counts, categorical rules and model mode only; it never contains goals, source code, filenames, raw LLM responses or keys.

The detailed local SQLite mission history still belongs to an individual GitHub Actions runner. Per-run JSON reports are retained as downloadable Actions artifacts for 7 days and may be visible to people with access to this public repository. **Never put secrets, passwords, names of private systems or confidential information into mission goals.**

## Optional real model connection
GitHub Models was discontinued on July 30, 2026. This laboratory does not rely on it.

An OpenAI-compatible HTTPS chat completions provider can be enabled in repository Settings → Secrets and variables → Actions:

- **Variable** LAB_LLM_ENDPOINT: HTTPS complete API URL, for example https://api.openai.com/v1/chat/completions (provider charges and API terms may apply).
- **Variable** LAB_LLM_MODEL: supported model identifier for that provider.
- **Repository secret** LAB_LLM_API_KEY: the corresponding provider token.

These settings must be provided explicitly by the owner; no tokens are created, read from other services or hardcoded by the lab. For manual GitHub Actions runs select **enable_model: true**. Automatic push-triggered research always leaves it disabled.

Even when configured, only aggregated category counts leave the runner. The model receives no goal, source text, filename, message memory or sensitive payload. At most two constrained review calls are made per mission. Outputs are explanatory notes, not evidence or executable directions.

## GitHub workflow
Actions → Research Lab - Persistent Missions → Run workflow. Enter a non-sensitive goal. Check logs for:
- RESTORED KNOWLEDGE RUNS: number
- RESEARCH MISSION COMPLETED
- TOTAL SHARED KNOWLEDGE RUNS: number after append
- MODEL MODE: not_configured / remote_model / provider_error

The workflow commits **only** knowledge/state.json to lab-memory, never main. Reports appear in run artifacts.

## Current limits
Cross-run persistence is aggregate-only, not the complete private SQLite journal. Module graphs are conservative and may omit dynamic or relative imports. No live LLM execution is claimed unless actual workflow logs show model_mode=remote_model; unit-test mocks do not prove provider access.
