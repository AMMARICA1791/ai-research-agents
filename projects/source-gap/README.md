# Source Gap — radar project 5

Converts the public radar's feed errors and selected signal sources into an operational coverage report. Source Gap flags actual reported feed failures without assuming every absent source failed.

Run from repository root:

```sh
python -m unittest discover -s projects/source-gap -p 'test_*.py' -v
python -m experiments.rapid_project_radar.radar --output /tmp/radar-report.json
python projects/source-gap/gap.py --report /tmp/radar-report.json --output /tmp/source-gap.json
```

No third-party dependencies, API keys, or invention claims.
