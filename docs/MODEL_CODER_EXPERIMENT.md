# Phase 4B: actual free local coding-model patch generation

Experimental and bounded by design.

The manual workflow Real Qwen Coder Patch Trial downloads open-weight
qwen2.5-coder:1.5b (~986 MB) into a standard public GitHub Actions runner.
No API key, paid LLM service or larger runner is configured.

The model sees **only one bundled synthetic sample** containing a single
silent typed-exception handler and a behavior requirement. The model must
generate full replacement Python source, which is treated as UNTRUSTED data.

Strict independent gates:
- Candidate length and UTF-8 validity are checked.
- AST shape must match exactly the sole known-safe fail-closed repair.
  The validator rejects any new import, function, side effect, additional
  statements, arbitrary code, or mismatched control flow.
- No candidate code executes until after AST validation.
- An isolated red/green behavioral check on the bundled synthetic fixture
  must fail before the repair and pass after it.
- The workflow has read-only permissions, no automatic repository edits,
  no PR creation or automatic main merge. Candidate rejected => failing job.
- Failure reports intentionally exclude untrusted model output.

**This proves narrowly scoped AI-generated code only when the real GitHub
workflow logs say REAL_QWEN_CODER_PATCH_GENERATED_AND_VERIFIED.**
Unit test mocks and the deterministic AST repair do not prove model authorship.
Even success does not establish ability on unseen production code or safe
general autonomous software development.
