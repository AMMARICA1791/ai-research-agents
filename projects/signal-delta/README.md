# Signal Delta — Radar-born project 3

Consumes the public Rapid Project Radar JSON report and highlights signals newly observed in that scan, with their source links. No claim of first discovery in the world.

## Run

```sh
python -m unittest discover -s projects/signal-delta -p 'test_*.py' -v
python projects/signal-delta/delta.py --report /tmp/radar-report.json --output /tmp/signal-delta.json
```

Use a radar report with a persistent first-seen registry for meaningful cross-run newness. Without persistent state, all signals may appear new each run.
