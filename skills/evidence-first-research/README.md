# Evidence-First Research — Community Edition

Experimental, English-first AI agent skill for source-linked research and explicit uncertainty.

## Install
Copy `SKILL.md` into the skills directory supported by your agent platform, following that platform's current instructions. Compatibility with individual agents is **not yet verified**.

## Use
Ask the agent to evaluate a claim with primary evidence, counterevidence, a claim-evidence matrix, and a reproducibility plan. Provide source documents or enable a browsing/retrieval tool. Without source access, outputs must mark claims unverified.

## Evaluation plan (not yet executed)
Run each prompt twice using the same model, tools, and source set: once without the skill, once with it. Blindly score the resulting outputs using EVALUATION.md. Publish raw outputs, tool versions, and failures. Do not claim a performance improvement before the evaluation.

## Limitations
This is a procedural prompt, not a search engine, automatic verifier, or scientific discovery. Human review is mandatory. Do not enter private data.

Upstream methodology: https://github.com/AMMARICA1791/ai-research-agents (Apache-2.0). See repository LICENSE and NOTICE for relevant attribution.
