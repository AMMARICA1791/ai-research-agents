# Phase 4: verifiable research, measured improvement, no API fees

This is a **bounded laboratory experiment**, not autonomous general-purpose
software engineering and not a claim of being world-first.

## What we can prove
1. The existing AST inspection is run on eight synthetic, known-label
   Python cases. Confusion-matrix metrics measure true/false positives and
   false negatives. Good results do NOT establish accuracy on unseen repos.
2. A deterministic code-change agent finds exactly one typed exception handler
   whose entire body is pass. It proposes replacing pass with a bare raise.
3. An isolated **bundled synthetic fixture** is executed in a new temporary
   directory with Python -I. It demonstrably fails the desired test first
   (red) and then passes after the candidate change (green).
4. The experiment records the candidate's unified diff, behavior,
   implementation category, and non-execution/security boundaries as
   downloadable GitHub Actions artifacts.
5. An independently testable suite verifies refusal on ambiguous changes,
   traversal-like output names, and preservation of repository files.

## Current limitations and safety
- Reraising changes application behavior; this is not a universal fix.
- The patch generator is AST-guided deterministic logic, **not Qwen writing code**.
- The only code executed in the experiment is a constant, synthetic fixture
  bundled with the trusted repository; no code from inspected repositories
  is run, and no generated patch is applied to main.
- The workflow has contents:read; no GitHub-token PR creation rights.
- No project code is automatically changed, committed, merged or uploaded.
- Model reasoning quality and real-world detection accuracy remain unmeasured.
- Public standard GitHub Actions runners are free subject to GitHub policies;
  storage and abusive use still have limits.

## From an Android tablet
Open Actions > Research Evidence & Bounded Repair > Run workflow.
Review the logs and the downloadable research-evidence artifact.
A successful run shows BOUNDED_REPAIR_RED_TO_GREEN_CONFIRMED
and SYNTHETIC_SCANNER_CASES_PASSED=8.

## Next threshold
To claim genuine autonomous coding we must demonstrate an open model
generating a novel source patch on an unseen task, tests rejecting bad
candidates, and a reviewable PR created without the assistant writing the
fix by hand. This phase does not claim that milestone.
