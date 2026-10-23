# Threat model and evaluation boundaries

## Assets and trust boundaries
User-approved action scope and target scope are authoritative only if recorded
by the trusted host; web pages, social posts, search results, MCP tool metadata,
and agent-generated text are untrusted. Approval is an explicit host-verified
event, not a phrase found in a document.

## Threats
Indirect prompt injection, origin spoofing, permission laundering through
tool descriptions, cross-origin data access, and unapproved consequential calls.
No live action execution is implemented.

## Current limitations
The reference Request object is a simplified *trusted-input abstraction*.
It does not authenticate origin or user consent. A malicious upstream component
could falsely populate origin='user' or explicit_approval=True. This benchmark
therefore does NOT demonstrate end-to-end safety, nor agent resistance to attacks.
The simplistic always-ALLOW baseline is a sanity check, not state of the art.

## Independent next experiment
1. Use a real browser or agent harness with source provenance supplied by the host.
2. Replay benign and adversarial tasks with blinded ground truth.
3. Compare against a scoped-allowlist baseline, AgentDojo, and equivalent
   permission gates under the same task conditions.
4. Record attack success rate, task completion, false refusals, latency,
   and permission bypasses with full reproducible traces.
5. Hold deployment and novelty claims until external review.

## References
- https://webmachinelearning.github.io/webmcp/ (draft, 2026-10-20)
- https://github.com/ethz-spylab/agentdojo
- https://github.com/promptfoo/promptfoo
- https://github.com/browser-use/browser-use
