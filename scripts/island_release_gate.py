#!/usr/bin/env python3
"""Conservative public-release gate: passing scaffold tests != validated hypothesis."""
import ast
import json
import sys
from pathlib import Path

REQUIRED = {
    "agent_security": {"evaluate"},
    "privacy": {"redact"},
    "provenance": {"snapshot", "drift"},
    "web_protocols": {"validate"},
}

def assess(folder):
    folder = Path(folder)
    try:
        h = json.loads((folder / "hypothesis.json").read_text(encoding="utf-8"))
        topic = h["topic"]
        tree = ast.parse((folder / "prototype.py").read_text(encoding="utf-8"))
        tests = ast.parse((folder / "test_prototype.py").read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, SyntaxError, TypeError) as exc:
        return False, "missing or malformed evidence: " + str(exc)
    if topic not in REQUIRED:
        return False, "no domain-specific validation protocol for " + str(topic)
    defined = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    missing = REQUIRED[topic] - defined
    if missing:
        return False, "topic implementation missing: " + ", ".join(sorted(missing))
    if not any(isinstance(n, ast.FunctionDef) and n.name.startswith("test_") for n in ast.walk(tests)):
        return False, "no runnable unit test cases"
    # Public experimental projects invite collaboration; independent validation is
    # not a prerequisite for publication. Never imply scientific verification.
    return True, "topic-specific prototype and runnable test present; scientific hypothesis unverified"

if __name__ == "__main__":
    ok, reason = assess(sys.argv[1])
    print(("ELIGIBLE: " if ok else "BLOCKED: ") + reason)
    sys.exit(0 if ok else 1)
