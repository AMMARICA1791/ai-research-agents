# Freshness Lens

A second independent, runnable project born from the Rapid Project Radar's actual metadata fields: feed publication ages, source identifiers, and feed errors.

**Purpose:** reveal whether the radar is surfacing recent signals from more than one source. The output is a compact JSON scorecard, not an originality or scientific validation claim.

Run from repository root:

```sh
python -m unittest discover -s projects/freshness-lens -p 'test_*.py' -v
python -m experiments.rapid_project_radar.radar --output /tmp/radar-report.json
python projects/freshness-lens/lens.py --report /tmp/radar-report.json --output /tmp/freshness.json
```

Uses Python standard library. A report may legitimately contain zero signals. RSS pubDate does not establish true discovery latency.
