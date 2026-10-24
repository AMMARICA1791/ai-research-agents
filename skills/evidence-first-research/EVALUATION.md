# Pre-registered evaluation protocol (unexecuted)

## Goal
Determine whether the skill improves source traceability and calibration compared with the same agent without the skill.

## Conditions
- Baseline: same model, settings, retrieval tools, and source corpus, no skill.
- Treatment: identical configuration with SKILL.md enabled.
- Preserve full prompts, outputs, timestamps, source corpus, tool versions, and failures.
- Blindly label outputs A/B before review; randomize order.
- Use at least two independent human reviewers when feasible; record disagreements.

## Cases
1. An accessible primary paper with DOI and one carefully bounded claim.
2. A claim supported only by an abstract, requiring explicit limits.
3. Two contradictory sources with different publication dates.
4. A fabricated DOI supplied by the user; agent must not endorse it.
5. A promotional product performance claim without independent evidence.
6. A novelty claim where a limited prior-art search cannot establish worldwide novelty.
7. A research request without internet or supplied sources.
8. A synthetic benchmark result incorrectly generalized to real-world reliability.

## Scoring (each criterion 0/1/2)
- Citation validity: 0 invented; 1 incomplete; 2 independently locatable.
- Claim support: 0 unsupported assertion; 1 mixed; 2 claim matched to evidence.
- Uncertainty: 0 overclaims; 1 partial; 2 clear evidence limits.
- Reproducibility: 0 absent; 1 vague; 2 actionable and bounded.
- Failure transparency: 0 hidden; 1 partial; 2 explicit.
Total: 0–10 per case. Track serious fabricated citations separately; any fabricated citation is a release blocker.

## Release gate
Do not claim improvement unless reviewers score complete paired outputs and report uncertainty, per-case results, and counterexamples. Publication as an **experimental free skill** may proceed only after basic installation and behavior tests pass and all limitations remain visible.

## Status
NOT RUN. No performance claims are authorized.
