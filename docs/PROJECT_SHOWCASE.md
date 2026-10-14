# AI Research Agents — public research review dossier

**Status: OPEN FOR EXTERNAL REVIEW · experimental public prototype, not a completed autonomous research institute or production service.**

[**Contribute an idea or critical review — Issue #54**](https://github.com/AMMARICA1791/ai-research-agents/issues/54) · [**Reproduce the public demo — Issue #22**](https://github.com/AMMARICA1791/ai-research-agents/issues/22) · [**Volunteer for source checking — Issue #52**](https://github.com/AMMARICA1791/ai-research-agents/issues/52)

## Why this laboratory exists

We want to study how small, open-weight models and deterministic tools can cooperate to gather evidence, test limited hypotheses, propose bounded improvements, and preserve both successful and failed experimental results — using free resources wherever practical. We are **looking for counterexamples and advice**, not only praise.

Seven pipeline stages are *organizational steps*, **not seven separately reasoning agents**. Most of the current implementation is deterministic; local Qwen/Ollama experiments are identifiable separately. The project is not a general autonomous code-repair or science-discovery platform.

## What can be inspected right now

| Demonstration or artifact | Evidence a visitor can inspect | Limits |
| --- | --- | --- |
| Three-command Python demo | [DEMO.md](../DEMO.md) and [public proof workflow](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml) | Eight scanner cases are synthetic; historical fix replay does **not** rerun Qwen |
| Real narrow model-authored code patch | [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17) and [recorded model run](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38120082970) | One pre-scoped GitHub host-validation bug; not discovery/repair of unknown bugs |
| Read-only public Python audit | [Workflow](../.github/workflows/public-repo-audit.yml) and [protocol](PUBLIC_REPO_AUDIT.md) | Static hints need human checking; no running unrelated repositories |
| Real scientific metadata exploration | [Scholarly discovery workflow](../.github/workflows/scholarly-discovery.yml) and [protocol](SCHOLARLY_DISCOVERY.md) | Crossref bibliographic metadata only; no independent paper reading or scientific verdict |
| Qwen over real AI-news excerpts | [Run and preserved failures](REAL_NEWS_QWEN_EVIDENCE_2026-10-13.md); [semantic review protocol](NEWS_SEMANTIC_REVIEW_PROTOCOL.md) | Quality gate failed; quotes alone do not validate claims; independent human gold labels missing |
| Frozen experimental baseline | [v0.1.0-experimental prerelease](https://github.com/AMMARICA1791/ai-research-agents/releases/tag/v0.1.0-experimental) | A historical research baseline, not a certification of the latest main branch |

See the complete [scope](PROJECT_SCOPE.md), [architecture](../ARCHITECTURE.md), [roadmap](../ROADMAP.md), [failure register](../FAILURES.md), [security policy](../SECURITY.md), and [contribution guide](../CONTRIBUTING.md) before drawing broader conclusions.

## A quick tour for visitors

**Path A — no installation and mobile friendly (about the report, not a live model):**

1. Open the [Public Proof Tour workflow](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml).
2. Pick a *completed, successful* run and read its **Summary**. Inspect what is synthetic versus historical.
3. Review [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17) and ask whether the proof supports only its narrow claim.
4. Leave a concrete critique in [Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54). Viewing is public; commenting generally requires a GitHub account.

**Path B — reproduce locally (Python 3.11+, no model keys or paid APIs for these commands):**

```sh
git clone https://github.com/AMMARICA1791/ai-research-agents.git
cd ai-research-agents
python -m lab.public_demo --repo . --out results/public-demo
python -m lab.benchmark
python -m lab.autorepair
```

Record the exact commit SHA and environment for a reproducibility report; copy only non-sensitive output. These commands use bundled inputs and do **not** prove live Qwen reasoning or scientific truth.

## Questions on which outside perspectives would be particularly valuable

1. Does the architecture support the *research-center vision*, or should we simplify/reorganize before adding more modules?
2. What independent experiment would convincingly distinguish true LLM reasoning from a deterministic pipeline?
3. Which current claims or demonstrations are overbroad, unverifiable or misleading?
4. How should we evaluate source-quotation entailment, generalization across publishers and the trustworthiness of scientific literature reviews?
5. What improvements would make onboarding, safety, test reproducibility, internationalization and ongoing maintenance easier?
6. Which of the current open tasks should be solved first, and which should be explicitly deferred?

## Prioritized work before a future stronger release

| Priority | Status on 2026-10-14 | Acceptance evidence |
| --- | --- | --- |
| **P0 — present an honest public evidence tour** | Public demo + prerelease exist; external critique invitation is now open | Visitor can find scope, limits, real run/PR, demo, and leave review with no hidden dependencies |
| **P1 — external reproducibility and semantic review** | No externally reproduced outcome or independently labeled Qwen cases reported yet | Repro steps, failures, actual reviewer decisions and adjudication in public record, with permissioned data |
| **P2 — controlled comparable model research** | Proposed, not proven in a live matched trial | Same tasks/budget, pinned versions, real results with failures and source fingerprints |
| **P3 — wider research platform / agents** | Aspirational; not product-ready | Documented independent contribution from actual model/tool invocations plus repeatable cross-topic validation |

**Do not claim a finished system or automatic publication.** Open issues deliberately remain open where the required evidence is missing.

## Contributing without writing code

- **Ideas or critiques:** [Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54); suggestions in English, Arabic, Portuguese, Spanish or French.
- **Reproducibility:** [Issue #22](https://github.com/AMMARICA1791/ai-research-agents/issues/22).
- **Independent manual review of 15 news excerpts:** [Issue #52](https://github.com/AMMARICA1791/ai-research-agents/issues/52).
- **Structured testable research proposal:** [GitHub issue forms](https://github.com/AMMARICA1791/ai-research-agents/issues/new/choose).

No paid keys or private account credentials should be supplied. Public research discussion is not a channel for disclosing sensitive vulnerabilities; see [SECURITY.md](../SECURITY.md).

---

## الملخص العربي — دعوة مفتوحة لتقييم المشروع

**هذا مختبر أبحاث ذكاء اصطناعي تجريبي ومفتوح المصدر، وليس مركزاً مستقلاً مكتملاً.** نبحث عن باحثين ومطورين وطلاب ومهتمين لاختبار ما نعرضه ونقده واقتراح تجربة صغيرة قابلة لإعادة التنفيذ تُثبت أو تدحض إحدى قدراته. توجد أدوات فعلية لفحص شيفرة Python، وعرض إثبات تجريبي، وتجارب Qwen محلية، وسجل للإخفاقات؛ لكن استقلال الوكلاء والدقة البحثية العامة لم يثبتا.

- **لإبداء رأيك حول المشروع ككل:** [نقاش ومقترحات المجتمع — Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54)
- **لمراجعة تجربة قابلة للتكرار:** [Issue #22](https://github.com/AMMARICA1791/ai-research-agents/issues/22)
- **للتطوع في مراجعة 15 إجابة إخبارية:** [Issue #52](https://github.com/AMMARICA1791/ai-research-agents/issues/52)
- **لعرض التجربة مباشرة دون برمجة:** [Public Proof Tour](https://github.com/AMMARICA1791/ai-research-agents/actions/workflows/public-demo.yml)

كل نقد مبني على دليل أو تجربة قابلة للتكرار مرحب به، ولا يشترط وجود خبرة برمجية للمشاركة بالرأي.

**Português:** Laboratório experimental aberto à avaliação de terceiros. Leia as evidências, teste a demonstração e publique críticas ou propostas na [Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54). Não se trata de um centro autônomo já validado.

**Español:** Prototipo experimental abierto a revisión externa. Se agradecen pruebas reproducibles, críticas y sugerencias en la [Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54); no afirmamos que el sistema autónomo esté terminado.

**Français:** Prototype de laboratoire expérimental ouvert à l'évaluation externe. Proposez des tests, critiques ou idées dans l'[Issue #54](https://github.com/AMMARICA1791/ai-research-agents/issues/54). Il ne s'agit pas d'un centre autonome entièrement validé.
