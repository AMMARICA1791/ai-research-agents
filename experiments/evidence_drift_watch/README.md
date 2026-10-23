# Evidence Drift Watch

**Question:** When a cited source changes, can we detect which previously
recorded verbatim evidence disappeared?

An offline, deterministic snapshot-diff prototype with SHA256 provenance and
quote-loss checks. Does **not** prove that a claim has become false, nor fetch
sites, circumvent access controls, or verify semantic entailment.

## Run
`python -m unittest discover -s experiments/evidence_drift_watch -p 'test_*.py' -v`

`python -m experiments.evidence_drift_watch.lab --before old.txt --after new.txt --quote "verbatim excerpt"`

## Prior art and novelty caution
Version control, webpage monitoring, citation tracking and diff tools are
established. This prototype claims no novelty. A useful future study would
compare evidence-level drift alerts against raw text diff and webpage-change
baselines, using independently labeled real archived snapshots.

## Safety
No automatic web requests, notifications, or publication. User-provided
snapshots only. Outputs must be reviewed by a human.
