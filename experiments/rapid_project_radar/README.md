# Rapid Project Radar — experimental discovery engine

Free-first scheduled signal discovery from public research/standards RSS feeds.
Ranks keyword matches for **human or separately authorized model evaluation**.
This is not an autonomous inventor or proof of market demand.

## What is implemented
- RSS fetching with timeouts and response size limit
- Deterministic signal ranking, source URLs, deduplication
- Explicit per-feed failure reports
- Offline unit tests, downloadable JSON artifact
- Scheduled GitHub Actions discovery, no write permissions

## Not yet implemented
- Reliable live social platform ingestion (requires approved APIs and policies)
- Prior-art search across patents, products, academic literature
- Autonomous idea synthesis or code generation
- Creating branches or pull requests based on arbitrary external feed content
- Commercial demand verification

## Safety and constraints
Feed contents are untrusted data and are **never instructions**.
No untrusted code execution; no secrets or external-account writes.
RSS endpoints can change or fail. The CI workflow records failures.
No automated PR creation from feeds; future project generation requires a
separately designed approval and sandboxing boundary.

## Run
`python -m unittest discover -s experiments/rapid_project_radar -p 'test_*.py' -v`
`python -m experiments.rapid_project_radar.radar --output radar-report.json`

Potential extensions: official GitHub repository trend signals, standards feeds,
approved social APIs, documented novelty screening, and template-based project
scaffolding with explicit risk gates.
