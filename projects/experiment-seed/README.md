# Experiment Seed — radar project 6

Turns **actual source-linked radar entries** into reproducible experiment *planning* dossiers. Every seed retains the original article/paper URL, publication metadata, and keyword categories; no scientific verification or experiment execution is claimed.

```sh
python -m unittest discover -s projects/experiment-seed -p 'test_*.py' -v
python -m experiments.rapid_project_radar.radar --output /tmp/radar-report.json
python projects/experiment-seed/seed.py --report /tmp/radar-report.json --output /tmp/experiment-seeds.json
```

This is the bridge from source collection toward later implementation of a falsifiable prototype, not a substitute for one.
