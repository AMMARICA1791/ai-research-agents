# Multi-agent Research Laboratory

Owner goal → Explorer (source inventory) → Analyst (Python AST findings)
→ Engineer (review proposals) → Validator (evidence check)
→ Synthesizer (report; optional external LLM commentary)
→ SQLite (mission and review history) → Human decision.

All stages read source without altering it. Approval records a decision
but never executes code changes. The legacy agents/ directory remains
for compatibility, with its demonstration examples clearly separated.
The research workflow is manually dispatched, not autonomous background work.
