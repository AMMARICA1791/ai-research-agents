# Signal Bridge — Radar-born experimental project

**Status: runnable candidate-link prototype; NOT a validated scientific discovery or invention.**

## Why this project exists
The repository's Rapid Project Radar gathers time-stamped public RSS signals. Its metadata-only keyword ranking does not yet demonstrate a connection between independent sources. Signal Bridge tests the next narrow hypothesis: *can two separately sourced signals be surfaced together with transparent, reproducible evidence?*

This is motivated by the radar's existing signal-ingestion capability, not by a claimed newly discovered scientific fact. A live candidate must be reviewed before asserting a meaningful scientific relationship.

## Reproduce
From repository root:

```sh
python -m unittest discover -s projects/signal-bridge -p 'test_*.py' -v
python -m experiments.rapid_project_radar.radar --output /tmp/radar-report.json
python projects/signal-bridge/bridge.py --report /tmp/radar-report.json --output /tmp/connections.json
```

The first command is offline. The second requires reachable RSS feeds. The third produces source-linked candidate connections. No external packages or API keys required.

## Falsifiable claim
For two different-source titles sharing at least two non-stopword tokens, the tool creates a candidate link and records the shared terms. For unrelated titles or duplicate-source pairs it creates no link. Tests use deliberately synthetic data; real-world precision has **not** been measured.

## Boundaries
- Matching is deterministic lexical overlap, not AI reasoning, cross-disciplinary insight, or proof of causation.
- Confidence is always LOW until independent source inspection.
- No patents, products or originality search is performed.
- RSS dates and first-seen timestamps are inherited from radar and not independently verified.
- Empty connections are valid results, not a reason to invent links.
- Review source content before any public scientific claim.

## Next empirical validation
Collect a real radar JSON artifact, review 20 candidate pairs and 20 non-matches manually, and publish labeled precision/recall estimates with source snapshots and timestamps. Do not present an untested match as a discovery.
