# Cosmic Origin of Iron — Research Protocol 01

**Status:** Approved research question; evidence collection pending. No scientific conclusion has yet been established by the lab.

## Title (Arabic)
الأصل الكوني للحديد: دراسة مقارنة بين الأدلة الفيزيائية الفلكية، والتاريخ الجيولوجي للأرض، ودلالة قوله تعالى: ﴿وَأَنزَلْنَا الْحَدِيدَ﴾ [الحديد: 25].

## Central question
What do independent astrophysical and geochemical measurements establish about the synthesis and delivery of iron to the material that formed Earth, and how should those findings be distinguished from classical Arabic exegetical readings of Quran 57:25?

## Workstreams
1. **Astrophysics:** Stellar nucleosynthesis, iron-group elements, supernovae, and the origin of solar-system matter. Distinguish synthesis of isotopes from delivery to Earth.
2. **Earth science:** Solar nebula, planetary accretion, differentiation, and Earth's core; distinguish primordial terrestrial iron from later meteoritic delivery.
3. **Archaeology (optional context):** Earliest documented use of meteoritic iron vs smelted terrestrial ores; do not confuse human discovery with the element's origin.
4. **Textual exegesis:** Read Quran 57:25 in Arabic, compare documented interpretations of «أنزلنا» in al-Tabari, Ibn Kathir and other recognized commentaries. Preserve interpretive plurality; do not assume one cosmological interpretation is the only legitimate reading.

## Method and acceptance gates
- Retrieve DOI/title/year/author metadata with the existing Crossref discovery workflow; this stage verifies metadata only.
- Identify primary sources, inspect accessible abstracts/full text, record the exact evidence and limitations; do not mark a scientific claim as verified based on titles.
- Separate: (a) directly measured evidence, (b) model-based scientific inference, (c) historical textual interpretation, and (d) philosophical or theological claims outside experimental adjudication.
- Record provenance (URL, DOI where available, retrieval date), disagreements, uncertainty, and alternative explanations.
- Compare claims only when their definitions and evidence types align. Do not claim the Quran is scientifically proven or disproven by astronomical data.
- **No new code, models, workflows, or repeated benchmark runs** until an existing tool's actual limitation is demonstrated and the owner approves a scoped fix.

## Initial test query
`stellar nucleosynthesis iron group elements supernova solar system Earth core formation meteoritic iron`

## Deliverable
A source-grounded Arabic report with a claim/evidence matrix, explicit uncertainty, and a separate section on classical interpretation of «أنزلنا».

## Current status
Protocol registered; no workflow has been run for this question, and no paper's full text has been verified for this protocol.

## Actual laboratory discovery run #7 (2026-10-11)

**Evidence:** Owner-provided GitHub Actions run #7 screenshot and complete job summary text. **Status: Success (14s).** Crossref retrieval timestamp: 2026-10-11T23:38:36+00:00. Metadata candidates: 5; invalid/incomplete records: 0. Response SHA-256: `36173f9ec796cdc813102e2887956ecdba01771caeb7c388dd2650cecb3d2e3a`. Artifact: `public-research-metadata` (2.29 KB; SHA-256 `778ec76680ec89011906e7fcf8ce317a5ed5b0ee25a42619fe7be8888cd7b83e`).

**Returned titles (unreviewed Crossref metadata, not paper findings):**
1. *Chapter 8 Part B. Rare Earth Elements in Iron-Formation* (1983) — weak direct relevance.
2. *Challenges in nucleosynthesis of trans-iron elements* (2014) — indirect context (beyond iron).
3. *Nuclear Aspects of Stellar and Explosive Nucleosynthesis* (2002) — high apparent relevance to stellar production.
4. *Supernova Pumps Iron in Inside-Out Blast* (2021) — potentially relevant; publication type and underlying evidence not verified.
5. *IRON ISOTOPE CONSTRAINTS ON PLANETESIMAL CORE FORMATION IN THE EARLY SOLAR SYSTEM* (2016) — high apparent relevance to differentiation of early solar system bodies.

**Assessment:** Discovery and provenance gate passed; source relevance mixed. No abstracts, full texts, isotopic measurements, models, or claims were checked by the workflow. The query returned no Quranic exegesis; classical tafsir must be evaluated in a separate textual track. Two GitHub annotations concern Node.js 20 deprecation and future ubuntu-latest migration; they did not prevent this run. **Do not present these five titles as verified evidence of any cosmological or theological claim.**

**Next gate:** Manually examine original research sources (especially stellar nucleosynthesis and isotope constraints), document methods and limitations, and keep the tafsir comparison separate. No new workflow or code changes needed.

## Evidence-analysis acceptance test 01 — 2026-10-11

**Test goal:** Can the existing GitHub scholarly-discovery workflow extract a scientific hypothesis, methods, evidence, limitations, and a bounded conclusion from one original paper?

**Code inspection:** `research/scholarly_discovery.py` requests only Crossref fields `DOI,title,published,type,container-title`; `.github/workflows/scholarly-discovery.yml` runs that metadata fetch and asserts `scientific_claims_verified == False`, `full_papers_reviewed == False`, and `model_inference == False`. **Outcome: NOT IMPLEMENTED in this workflow.** Re-running discovery cannot test full-text analysis; no workflow was re-run or changed.

**Manual control test, external to lab:** S. E. Woosley and T. A. Weaver (1995), *The Evolution and Explosion of Massive Stars. II. Explosive Hydrodynamics and Nucleosynthesis*, *The Astrophysical Journal Supplement Series* 101, 181–235, primary full text: https://articles.adsabs.harvard.edu/pdf/1995ApJS..101..181W . This is an independent primary source, **not one of the five titles returned by run #7**.

- Research objective: Model nucleosynthetic isotope yields from evolving and exploding massive stars across stellar masses and metallicities (paper pp. 181–182, abstract and §1).
- Methods: 78 model explosions, a 200-isotope reaction network, different initial stellar masses and metallicities; explosion initiated with a modeled piston and a specified energy (§2).
- Findings: Heavy-element ejection and fallback vary with progenitor properties and explosion parameters; some massive stars retain much of their heavy-element yield (abstract and §1).
- Caveats: Results depend on explosion mechanism, convective/nuclear inputs, energy and mass cut, and a one-dimensional approximation (§1–2). The work is simulation-based rather than direct measurement of Earth's iron.
- Bounded conclusion: Supports plausible physical mechanisms for stellar production and dispersal of iron-group matter; does not independently reconstruct the provenance of every terrestrial iron atom, quantify all iron sources, or establish an interpretation of Quran 57:25.

**Test verdict:** Human-assisted original-paper evidence extraction: **demonstrated on one study**. Automated laboratory evidence extraction: **NOT PASSED / capability absent in inspected scholarly workflow**. Do not report this manual extraction as an autonomous GitHub pipeline success. No new model, workflow, or experimental run was created.
