# Claim Stress Lab — مختبر الضغط على الادعاءات

**Research question:** Can inexpensive deterministic counterfactual probes expose weak model citations *before* a human reviewer spends time on them?

This is a new **isolated experiment** inside AI Research Agents, not a replacement for its news gate. It does not use LLMs, paid APIs, third-party services, or publish outputs. It makes **no novelty claim**: citation audits, perturbation tests and lexical overlap have extensive precedents. The experiment tests whether their combination is useful for prioritizing human review.

## What it does
- Checks whether the **model's original quote** occurs verbatim in the archived excerpt.
- Flags numerical assertions in the claim that are absent from that quote.
- Measures crude lexical overlap between claim and quote.
- Performs **quote ablation**: removes the first exact quote occurrence from the source and measures remaining lexical overlap.
- Always returns `semantic_accuracy: null`, `publication_allowed: false`, and `review_required: true`.

## Try it
From repository root, Python 3.11+:

```sh
python -m experiments.claim_stress_lab.lab --input experiments/claim_stress_lab/examples.json
python -m unittest discover -s experiments/claim_stress_lab -p 'test_*.py'
```

## Interpretation
Flags are **review prioritization hints**, not proof of falsehood or truth. Lexical overlap can miss paraphrases, negation, attribution, and domain terminology; numeric matching can overflag formatting differences. Removing a quote can leave other valid evidence in the article. The source URL is carried as metadata, **not verified or fetched**. The tool does not authenticate a publisher or human reviewer.

## Falsifiable next experiment
Use an authorized, locally archived and independently labeled evaluation set. Blind human reviewers to the flags, then compare flagged vs unflagged cases on **human-confirmed unsupported citations**. Report precision/recall with denominators and negative results. Do not close F-002 or loosen its quality gates on the basis of this prototype.

## Verified scope and decision status (2026-10-22)
- GitHub Actions **Claim Stress Lab run #27** passed the offline tests, labeled synthetic benchmark, and example diagnostic. This confirms software checks, **not** real-world citation accuracy.
- The four-case synthetic benchmark was constructed by the developers: 2 planted mechanical defects and 2 controls. Its perfect score cannot be generalized.
- Synthetic adversarial probes show **known missed semantic errors**: reversing a negation and converting an association into a causal claim. Neither mechanical detection nor high lexical overlap establishes entailment.
- Independent real-source evaluation: **not yet conducted**. Independent reviewer labels: **none**. No real-world precision or recall is available.
- The experiment remains isolated in a draft pull request. Do not merge, close F-002, or advertise a scientific advance before satisfying [DECISION_GATE.md](DECISION_GATE.md).

## Evaluation tools
```sh
python -m experiments.claim_stress_lab.benchmark
python -m experiments.claim_stress_lab.adversarial_probes
python -m experiments.claim_stress_lab.evaluate_dataset --input independently_labeled.json
```
The final command requires a real, independently labeled file that is **not supplied**. See [EVALUATION_PROTOCOL.md](EVALUATION_PROTOCOL.md). Do not use synthetic development cases as independent validation.
