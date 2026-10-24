# Genuine-Agent Research Gate — 2026-10-24

## Question

Can the current repository autonomously read an unselected scientific paper, extract a falsifiable quantitative claim, design an independent experiment, run it, and audit its evidence **without a human authoring the experiment**?

## Code-level assessment

**Result: NOT DEMONSTRATED.**

- `experiments/rapid_project_radar/anticipate.py` selects from four hardcoded `SCENARIOS` and `PROTOTYPES`; source text cannot generate a novel scientific experimental protocol.
- `experiments/rapid_project_radar/council.py` implements deterministic word-set comparisons and scoring, not separate language-model agents.
- `experiments/empirical_validation/next_experiment.py` uses a fixed 0.90 decision threshold; it is evidence-conditioned but not open-ended scientific inference.
- The empirical calibration and Iris CI runs establish numerical and engineering reproducibility for human-designed protocols, not agent autonomy.

## Non-negotiable pass criteria

1. Select a new paper with immutable citation, snapshot and source checksum; exclude the existing Iris and birthday examples.
2. Run a real, identifiable model (e.g. Qwen) on the paper text with model name/version, prompt hash, inference parameters and raw response preserved.
3. Require the model to emit a structured claim, exact evidence quotation/location, falsification criterion, data requirements, experimental protocol and anticipated failure modes. Reject missing evidence.
4. Have a separately executed critical review challenge leakage, data provenance, validity and falsifiability; preserve both raw outputs.
5. Execute a sandboxed, allowlisted experiment only after human approval. No unreviewed model-produced code execution, no write-capable credentials in the inference sandbox.
6. Compare measured outcomes to the frozen pre-execution protocol; archive failures as well as passes.
7. Derive a follow-up question that explicitly cites the observed results, then independently review it.

## Verdict

Do not count the current heuristic council, templates or rule-based successor as passing any model-inference gate. Until a real model's original response is captured and evaluated, the core autonomy hypothesis remains **UNTESTED**. The next milestone is one verified Qwen inference on a genuinely new paper, not additional Iris metrics.
