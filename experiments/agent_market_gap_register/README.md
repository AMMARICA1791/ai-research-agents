# Agent Market Gap Register

**Purpose:** rank *research readiness*, not commercial potential, of emerging
agent-web product hypotheses. The input must name the problem, likely buyer,
workaround, measurable test, competitor baseline and linked observations.

## Why this experiment
October 2026 W3C discussions emphasize user consent, delegated authorization,
and provenance in agentic web systems. These are candidate needs, **not proof**
that a buyer will pay or that a proposed solution is novel.

## Source starting points (verify dates and claims independently)
- https://webmachinelearning.github.io/webmcp/
- https://www.w3.org/2026/10/w3c-and-state-of-web-in-ai-era.html
- https://github.com/w3c-cg/ai-agent-protocol/blob/main/meetings/2026-10-21.md
- https://github.com/OWASP/AISVS
- https://github.com/ethz-spylab/agentdojo

## Run
`python -m unittest discover -s experiments/agent_market_gap_register -p 'test_*.py' -v`

`python -m experiments.agent_market_gap_register.lab --input opportunities.json`

Input is a JSON list. Each item needs strings: problem, buyer,
current_workaround, falsifiable_test, success_metric, competitors; plus an
evidence list of objects with https url and observation strings.

## Decision gate
Do not claim product-market fit, novelty, revenue, or customer demand from
public research alone. Require buyer interviews, competitor replication,
and an independently validated benchmark before promotion. This tool does not
crawl sites or publish anything.
