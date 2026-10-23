SOURCE_EXCERPT = 'arXiv:2608.14590v3 Announce Type: replace Abstract: Large Language Model (LLM) agents take irreversible real-world actions, yet no system gives formally grounded, task-level safety guarantees for their plans. In a PRISMA 2020 systematic review, we searched six databases (20-29 May 2026) for work on LLM agent specification, verification, and enforcement published in 2022-2026. We narratively synthesized 38 studies, assessed risk of bias per study,'
def evidence_matches(text):
    return isinstance(text, str) and bool(SOURCE_EXCERPT) and SOURCE_EXCERPT in text
