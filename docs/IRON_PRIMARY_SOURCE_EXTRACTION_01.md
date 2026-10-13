# Primary-source extraction 01 — Cosmic origin of iron

**Source:** Woosley, S. E. & Weaver, T. A. (1995), *The Evolution and Explosion of Massive Stars. II. Explosive Hydrodynamics and Nucleosynthesis*, ApJS 101, 181–235. Primary scanned PDF: https://articles.adsabs.harvard.edu/pdf/1995ApJS..101..181W

**Method / provenance:** Human-directed review of the publicly accessible primary PDF and its extracted text, 2026-10-11. Page numbers below are printed journal pages. This document is **not** an output of the repository's automated Qwen pipeline, does not demonstrate full-text ingestion, and is **not** scientific fact verification.

| Field | Extracted claim | Primary location | Type / limitation |
| --- | --- | --- | --- |
| Objective | Calculate nucleosynthetic yields for isotopes lighter than zinc over a grid of stellar masses and metallicities. | p. 181, abstract | Authors' modeled research objective |
| Methods | 78 simulated supernova explosions, with 200-isotope nucleosynthesis tracking and a piston-driven explosion model. | p. 181, abstract; p. 182, §2.1 | Computational simulation, not a direct measurement of Earth's iron |
| Evidence / results | The authors report a grid of predicted isotopic yields; the mass cut and fallback depend on explosion energy, stellar structure, mass, and metallicity. | p. 181, abstract and §1; p. 182, §§1–2 | Model outputs conditional on assumptions |
| Limitations | The authors identify uncertainty in explosion mechanisms, nuclear and stellar physics, and convection; calculations use one spatial dimension. | p. 181, §1 | The model's applicability is bounded |
| Scope boundary | This paper alone does not trace individual iron atoms into Earth or determine an interpretation of Quran 57:25. | Scope of paper, pp. 181–235 | Reviewer inference about scope; **not** an author quote |

## Small verbatim anchors (not full text)

- p. 181, abstract: “Altogether 78” (model count; verify surrounding sentence in original PDF).
- p. 181, §1: “one spatial dimension” (computational simplification).

These brief anchors are for locating evidence; the original PDF is authoritative, especially where OCR introduces spacing errors. No claim-to-evidence semantic entailment was independently machine-verified.

## Outcome and failure boundary

**Primary-paper review: completed with human direction. Automated extraction: NOT PASSED.** The existing pilot's latest model-generated synthetic-excerpt result was 0/5 exact matches (GitHub Actions run 38196635024); its seven offline tests passed. The separately added real-paper fixture verifies supplied quotes against supplied lines, **not** independent discovery from a PDF. F-001 remains OPEN.

**Next narrow engineering gate:** Fetch and text-extract the real PDF in CI with page identifiers, retain the extraction artifact and digest, run the model without prefilled answers, and verify every returned quote against the extracted page. Distinguish absent fields from wrong answers. Keep PR #44 unmerged until this is demonstrated.
