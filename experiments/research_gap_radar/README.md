# Research Gap Radar

A **hypothesis readiness** checker for a portfolio of research ideas.
Checks for a falsifiable prediction, proposed experiment, comparison baseline,
prior-art note, and a crude quantitative signal. It **cannot** search the
literature, validate novelty, or infer scientific feasibility.

## Run
`python -m unittest discover -s experiments/research_gap_radar -p 'test_*.py' -v`

`python -m experiments.research_gap_radar.lab --input hypotheses.json`

Input is a JSON array of objects with `hypothesis`,
`falsifiable_prediction`, `experiment`, `baseline`, and `prior_art`
strings. Outputs indicate only readiness for **human** research review.

## Prior art
Literature-review tools, novelty scoring and hypothesis-generation systems
already exist. No first-in-world claim. A meaningful next experiment would
test inter-rater agreement with blinded reviewers and compare against a simple
research checklist on genuinely new submissions.

No web access, model inference, external accounts, or automated publication.
