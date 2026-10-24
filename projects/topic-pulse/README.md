# Topic Pulse — radar project 4

Produces a transparent JSON summary of which radar topic tags occur most frequently and how many independent feeds contribute. No third-party libraries.

```sh
python -m unittest discover -s projects/topic-pulse -p 'test_*.py' -v
python -m experiments.rapid_project_radar.radar --output /tmp/radar-report.json
python projects/topic-pulse/pulse.py --report /tmp/radar-report.json --output /tmp/topic-pulse.json
```

These are radar keyword categories, not proof of global scientific momentum.
