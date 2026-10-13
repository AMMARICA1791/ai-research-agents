# Laboratory Demonstration — Iron-Group Nucleosynthesis

**Status:** Reproducible, source-anchored research demonstration; **not independently scientifically validated**.

## Research question
What can two original supernova-nucleosynthesis papers establish about the production of iron-group isotopes, and what do they *not* establish about the provenance of iron in Earth?

## Primary literature
1. Woosley & Weaver (1995), *The Evolution and Explosion of Massive Stars. II. Explosive Hydrodynamics and Nucleosynthesis*, ApJS 101, 181–235. [Original PDF](https://articles.adsabs.harvard.edu/pdf/1995ApJS..101..181W).
2. Iwamoto et al. (1999), *Nucleosynthesis in Chandrasekhar Mass Models for Type Ia Supernovae and Constraints on Progenitor Systems and Burning-Front Propagation*, ApJS 125, 439–462. [Original PDF](https://arxiv.org/pdf/astro-ph/0002337).

## Source-anchored findings

| ID | Paper | PDF page | Bounded finding | Status |
| --- | --- | --- | --- | --- |
| F1 | Woosley & Weaver | 1 | The authors report calculating 78 model supernova explosions. | Provisional textual support |
| F2 | Woosley & Weaver | 1 | The authors identify uncertainty in the explosion mechanism as a limitation for predicting some isotope abundances. | Provisional textual support |
| F3 | Woosley & Weaver | 2 | The authors present ejected isotope yields from modeled stars over multiple initial metallicities. | Provisional textual support |
| F4 | Iwamoto et al. | 1 | The authors model explosive nucleosynthesis while varying deflagration speeds and ignition densities. | Provisional textual support |
| F5 | Iwamoto et al. | 1 | In the modeled scenarios, the total nickel-56 yield and Si–Ca/Fe ratio depend on the deflagration-to-detonation transition density. | **Edited claim: semantic review pending** |
| F6 | Iwamoto et al. | 1 | Some modeled neutron-rich iron-group isotope abundances are sensitive to electron captures. | Provisional textual support |

Page references are physical PDF page numbers, not journal page numbers. The excerpt behind F5 is truncated in the extraction; it requires full-paragraph inspection before approval. None of these claims has an independent expert label.

## Comparison and interpretation
These studies investigate **different modeled stellar explosion channels**: massive-star explosions and Chandrasekhar-mass Type Ia explosions. Both are relevant to iron-group nucleosynthesis, but this two-paper exercise does **not** normalize their isotope yields or establish their relative contribution to the solar system.

**Supported bounded conclusion:** The cited papers provide model-based evidence that supernova nucleosynthesis can produce iron-group material, and that predicted abundances depend on physical assumptions and model parameters.

**Not established:** The fraction of Earth's iron originating from each explosion channel; a unique stellar source for terrestrial iron; a quantitative cosmic iron budget; or an independent experimental confirmation of all modeled yields. Establishing those would require additional work on galactic chemical evolution, solar-system formation, isotopic constraints, and full-context review.

## Demonstrated laboratory capabilities
- Retrieve/extract original PDF text in CI, with source references.
- Record source-linked findings, PDF-page references and verbatim-text fingerprints.
- Reject silent edits to previously frozen scientific claims.
- Queue new or edited claims for semantic adjudication rather than silently approving them.
- Produce a conservative comparison and explicitly abstain from unsupported conclusions.

## Not yet demonstrated
- General-purpose semantic entailment or contradiction detection on unseen scientific literature.
- Autonomous expert-quality interpretation of complete papers.
- Independent expert adjudication.
- Quantitative synthesis across heterogeneous nucleosynthesis models.

## Acceptance statement
**Technical provenance demonstration: completed on the latest passing workflows.**

**Scientific semantic validation: NOT_PASSED.** This demonstration must not be marketed as an autonomous scientific discovery or as proof of the provenance of Earth's iron.

## Reproducibility
- Structured report: `research/scoped_iron_report.json`
- Frozen reviewed claims: `research/reviewed_iron_claims_baseline.json`
- Provisional evidence decisions: `research/provisional_primary_paper_review.json`
- Pending adjudication queue: `research/semantic_review_queue.py`
- Workflow: `.github/workflows/paper-evidence-pilot.yml`

The edited F5 remains pending; it is deliberately not incorporated into the frozen baseline. No claim of external scientific peer review is made.
