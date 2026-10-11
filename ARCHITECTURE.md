# AI Research Agents — evidence-first laboratory architecture

**Seven coordinated pipeline stages are NOT seven independent LLM agents.** The present mission orchestrator performs mostly deterministic steps and can optionally request a local Qwen/Ollama summary. Specialist-agent modules in `agents/` contain prototypes and demonstrations; their presence does not prove a deployed multi-model research team.

## Current verified execution

```text
Research question
    ↓
Explorer → Analyst → Dependency mapper → Engineer (review proposals)
    ↓
Critic → Validator → Synthesizer (optional local-model commentary)
    ↓
Per-run report + local SQLite + sanitized cross-run counts
    ↓
Human reviews; no automatic merge
```

This routine performs bounded AST and dependency analysis and records evidence. A separate **pre-scoped** Qwen patch experiment demonstrated one real GitHub URL validation repair. A separate read-only workflow evaluates public repositories without running their code.

## Intended research-center disciplines

Research/exploration; substantive specialist roles; comparative experiments; knowledge with provenance; bounded engineering; and independent verification. These are project goals, **not all verified active features**. [Roadmap](ROADMAP.md) and [Research scope](docs/PROJECT_SCOPE.md) distinguish completed work from research directions.

## Reproducibility and limits

[Run the standard-library three-command evidence demo](DEMO.md). Scanner benchmark inputs are synthetic and do not demonstrate broad accuracy. The historical Qwen-generated source fix is recorded in [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17); the demo reruns its regression, not the model itself. No experiment grants untrusted third-party code execution with repository write credentials.
