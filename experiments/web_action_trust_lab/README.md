# Web Action Trust Lab — independent research experiment

## Research question
Can a deterministic, least-privilege policy gate prevent web/social content
from being promoted into authority to execute tools, without blocking legitimate
user-authorized tasks?

## Status
Hypothesis and offline test design only. No measured security advantage, no
claim of global novelty, and no live integrations.

## Precedents to compare
- https://github.com/ethz-spylab/agentdojo — prompt-injection benchmark
- https://github.com/promptfoo/promptfoo — security evaluation
- https://github.com/browser-use/browser-use — browser automation
- https://github.com/w3c-cg/ai-agent-protocol/blob/main/meetings/2026-10-21.md — recent agent authorization discussion
- https://github.com/a2aproject/A2A — interoperability standard

## Testable hypothesis
Across *the same* blinded adversarial task fixtures, explicit provenance,
scoped action permission, and a user-consent gate reduce unauthorized actions
compared with a naive content-following agent. Report false refusals as well.

## First controlled experiment
Inputs: a user request, untrusted webpage or social-post text, and proposed
tool calls. Distinguish READ from WRITE/POST/TRANSFER/DELETE. Reject tool
instructions originating only in untrusted text; require direct user approval
for consequential actions. Never execute proposed calls in this benchmark.

Record: fixture hash, provenance, policy decision, expected decision,
TP/FP/FN/TN, false blocks, and missed unauthorized actions. Compare to a
simple allowlist baseline on the identical fixtures.

## Isolation and safety
No social account tokens, browser sessions, payments, live posting, or external
side effects. Do not treat social content as instructions. GitHub workflow
permissions should remain read-only. Do not merge into main before independently
reviewed real-world cases and baseline comparison.

## Relationship to Claim Stress Lab
This is a separate experiment with separate tests, metrics, and decision gate.
The existing Claim Stress Lab branch and PR #57 remain unchanged.
