# Phase 5: genuine AI-generated change to an actual repository

The real web/app.py GitHub URL parser accepts spoofed hosts because it uses
an unanchored regular expression. This workflow asks an open-weight Qwen Coder
1.5B model to generate a fix to that existing source line. It is not an
assistant-written solution. The agent must provide valid JSON with the one
replacement source line, which is treated as untrusted input.

Safety:
- Independent structural AST checker verifies no other source changes and
  requires an exact known-safe anchored URL pattern.
- A behavioral test of only the actual function proves baseline failure and
  proposed fix success against spoofed and legitimate host inputs.
- A separate runner with read-only permissions runs the full pytest suite
  and a new trusted regression test.
- A final publisher job revalidates before writing, without executing
  any AI-generated code in its credentialed environment.
- An isolated branch and human-review PR are created; no auto merge.
- Public GitHub standard runner and open-weight model, no API keys or
  paid LLM subscription. Resource use is subject to GitHub policy.
- Repository administrators may need to enable Actions permission to create
  pull requests. If GitHub rejects automated PR creation, the independently
  validated source branch can be submitted by a maintainer.
- Success proves only a narrowly scoped real repo source edit, not broad
  unsupervised software engineering or world-first research autonomy.
