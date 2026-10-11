"""Narrow real-repository AI patch experiment: github.com host spoofing.

Model suggests ONE source line. An independent structural/behavioral gate
rejects all edits except replacing the vulnerable re.search with a correctly
anchored re.match. No user secrets, tools or model commands are executed.
"""
from __future__ import annotations
import ast
import difflib
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TARGET = Path("web/app.py")
MODEL = "qwen2.5-coder:1.5b"
ENDPOINT = "http://127.0.0.1:11434/api/generate"
SAFE_PATTERN = r"^https://github\.com/([^/]+)/([^/]+)"
REGRESSION = '''"""Regression tests: only canonical HTTPS GitHub URLs may be parsed."""
import pytest
from web.app import _parse_github_url

@pytest.mark.parametrize("url,expected", [
    ("https://github.com/demo/sample", {"owner":"demo","repo":"sample"}),
    ("https://github.com/demo/sample.git", {"owner":"demo","repo":"sample"}),
    ("https://github.com/demo/sample?ref=main", {"owner":"demo","repo":"sample"}),
])
def test_valid_github_urls(url, expected):
    assert _parse_github_url(url) == expected

@pytest.mark.parametrize("url", [
    "https://evilgithub.com/demo/sample",
    "https://example.org/x/github.com/demo/sample",
    "https://github.com.evil.org/demo/sample",
    "https://github.com@evil.org/demo/sample",
    "http://github.com/demo/sample",
])
def test_reject_noncanonical_host_or_scheme(url):
    with pytest.raises(ValueError):
        _parse_github_url(url)
'''
CHECK = '''import json, re, sys
from pathlib import Path
a = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ns = {"re": re, "Dict": dict}
exec(compile(a["function"], "<real_repo_target_only>", "exec"), ns)
f = ns["_parse_github_url"]
for value, expectation in [
    ("https://github.com/demo/sample", ("demo","sample")),
    ("https://github.com/demo/sample.git", ("demo","sample")),
    ("https://github.com/demo/sample?ref=abc", ("demo","sample")),
]:
    assert tuple(f(value).values()) == expectation
for evil in [
    "https://evilgithub.com/demo/sample",
    "https://other.test/redirect/github.com/demo/sample",
    "https://github.com.evil.test/demo/sample",
    "https://github.com@evil.test/demo/sample",
    "http://github.com/demo/sample",
]:
    try:
        f(evil)
    except ValueError:
        continue
    raise AssertionError("spoofed host accepted")
'''


def _target_function(source: str) -> ast.FunctionDef:
    root = ast.parse(source)
    funcs = [n for n in root.body if isinstance(n, ast.FunctionDef)
             and n.name == "_parse_github_url"]
    if len(funcs) != 1:
        raise ValueError("Target function not found exactly once")
    return funcs[0]


def _original_assignment(source: str) -> tuple[int, str]:
    function = _target_function(source)
    matches = [
        x for x in function.body
        if isinstance(x, ast.Assign) and len(x.targets) == 1
        and isinstance(x.targets[0], ast.Name) and x.targets[0].id == "match"
    ]
    if len(matches) != 1:
        raise ValueError("Unexpected target structure")
    match = matches[0]
    expr = match.value
    if (not isinstance(expr, ast.Call) or
        not isinstance(expr.func, ast.Attribute) or
        not isinstance(expr.func.value, ast.Name) or
        expr.func.value.id != "re" or expr.func.attr != "search"):
        raise ValueError("Target no longer contains the vulnerable search")
    return match.lineno, source.splitlines()[match.lineno-1]


def build_candidate(source: str, line: str) -> str:
    if not isinstance(line, str) or len(line) > 200 or "\n" in line or "\r" in line:
        raise ValueError("A single Python line is required")
    tree = ast.parse(line.strip())
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Assign):
        raise ValueError("Only an assignment is allowed")
    assign = tree.body[0]
    if (len(assign.targets) != 1 or not isinstance(assign.targets[0], ast.Name)
        or assign.targets[0].id != "match" or not isinstance(assign.value, ast.Call)):
        raise ValueError("Unexpected assignment")
    call = assign.value
    if (not isinstance(call.func, ast.Attribute) or call.func.attr != "match"
        or not isinstance(call.func.value, ast.Name) or call.func.value.id != "re"
        or call.keywords or len(call.args) != 2
        or not isinstance(call.args[0], ast.Constant)
        or call.args[0].value != SAFE_PATTERN
        or not isinstance(call.args[1], ast.Name) or call.args[1].id != "value"):
        raise ValueError("Unsafe or incorrect regex patch")
    index, original = _original_assignment(source)
    indentation = original[:len(original)-len(original.lstrip())]
    replacement = indentation + line.strip()
    old_lines = source.splitlines(keepends=True)
    suffix = "\r\n" if old_lines[index-1].endswith("\r\n") else "\n"
    old_lines[index-1] = replacement + suffix
    candidate = "".join(old_lines)
    baseline = ast.parse(source)
    verified = ast.parse(candidate)
    old_fn = next(n for n in baseline.body
                  if isinstance(n, ast.FunctionDef) and n.name == "_parse_github_url")
    old_assign = next(n for n in old_fn.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "match" for t in n.targets))
    old_assign.value = assign.value
    if ast.dump(baseline, include_attributes=False) != ast.dump(verified, include_attributes=False):
        raise ValueError("Model changed additional code")
    return candidate


def _check_source(source: str) -> bool:
    fn = _target_function(source)
    lines = source.splitlines(keepends=True)
    only_fn = "".join(lines[fn.lineno - 1:fn.end_lineno])
    with tempfile.TemporaryDirectory(prefix="lab-real-repo-") as d:
        p = Path(d)/"target.json"
        p.write_text(json.dumps({"function": only_fn}), encoding="utf-8")
        t = subprocess.run([sys.executable, "-I", "-c", CHECK, str(p)],
                           capture_output=True, text=True, timeout=15, check=False)
        return t.returncode == 0


def _write_report(report: dict, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    (output/"real-repo-report.json").write_text(json.dumps(report, indent=2)+"\n")


def generate(repo: Path, output: Path) -> int:
    import requests
    source = (repo/TARGET).read_text(encoding="utf-8")
    lineno, old_line = _original_assignment(source)
    if _check_source(source):
        raise ValueError("Target no longer fails the regression test")
    report = {
        "model": MODEL, "target": str(TARGET),
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "baseline_test": "FAIL", "candidate_test": "NOT_RUN",
        "status": "rejected", "attempts": 0, "human_merge_required": True,
        "rejection_reasons": [],
    }
    function = _target_function(source)
    lines = source.splitlines()
    fragment = "\n".join(lines[function.lineno-1:function.end_lineno])
    base_prompt = (
        "Fix a REAL Python repository defect, not a tutorial exercise. "
        "The function accepts spoofed GitHub URLs because re.search finds "
        "'github.com' anywhere in an input string. Change ONLY the assignment "
        "to variable match. Use re.match and a regex anchored at the BEGINNING "
        "to literal https://github.com/; preserve the two capture groups "
        "for owner and repository. Keep every other source line unchanged. "
        "Use EXACTLY this regex pattern literal: "
        "r'^https://github\\.com/([^/]+)/([^/]+)' with re.match and value.\n"
        "Real existing function:\n" + fragment + "\n"
        "Return JSON with ONE field 'line': the single replacement Python "
        "assignment statement (match = ...). No explanations."
    )
    for attempt in range(2):
        report["attempts"] = attempt+1
        prompt = base_prompt + (
            "" if not attempt else "\nYour previous response failed independent "
            "source validation. Return only the new single assignment, no "
            "markdown or function definition."
        )
        try:
            r = requests.post(ENDPOINT, json={
                "model": MODEL, "prompt": prompt, "stream": False,
                "format": {"type": "object", "properties": {"line": {"type": "string"}},
                           "required": ["line"], "additionalProperties": False},
                "options": {"temperature": 0, "seed": 75+attempt,
                            "num_predict": 120, "num_ctx": 1536},
                "keep_alive": "0s",
            }, timeout=(5, 100), allow_redirects=False)
            r.raise_for_status()
            payload = r.json().get("response", "")
            proposal = json.loads(payload)
            candidate = build_candidate(source, proposal["line"])
            if not _check_source(candidate):
                report["rejection_reasons"].append("behavioral_test_failed")
                continue
            output.mkdir(parents=True, exist_ok=True)
            (output/"proposed-app.py").write_text(candidate, encoding="utf-8")
            (output/"trusted-url-regression.py").write_text(REGRESSION, encoding="utf-8")
            patch = "".join(difflib.unified_diff(source.splitlines(keepends=True),
                candidate.splitlines(keepends=True), fromfile="a/web/app.py",
                tofile="b/web/app.py"))
            (output/"model-proposed.patch").write_text(patch, encoding="utf-8")
            report.update({
                "status": "model_generated_real_repo_patch_verified",
                "candidate_test": "PASS",
                "candidate_sha256": hashlib.sha256(candidate.encode()).hexdigest(),
                "changed_line": lineno,
                "files_changed_by_model": ["web/app.py"],
                "trusted_regression_test_file": "tests/test_github_url_safety.py",
                "source_modified_in_repository": False,
            })
            _write_report(report, output)
            return 0
        except requests.RequestException:
            report["rejection_reasons"].append("local_model_http_error")
        except json.JSONDecodeError:
            report["rejection_reasons"].append("model_json_invalid")
        except KeyError:
            report["rejection_reasons"].append("model_json_missing_line")
        except (ValueError, SyntaxError, TypeError) as exc:
            # Emit fixed diagnostic codes only. Do not retain untrusted text.
            reason = str(exc)
            if reason == "Unsafe or incorrect regex patch":
                reason = "regex_outside_exact_allowlist"
            elif reason == "Model changed additional code":
                reason = "unexpected_additional_ast_edit"
            elif reason == "Only an assignment is allowed":
                reason = "not_a_single_assignment"
            else:
                reason = "invalid_candidate_structure_or_test"
            report["rejection_reasons"].append(reason)
    _write_report(report, output)
    return 2


def verify(repo: Path, output: Path) -> None:
    report = json.loads((output/"real-repo-report.json").read_text())
    original = (repo/TARGET).read_text(encoding="utf-8")
    candidate = (output/"proposed-app.py").read_text(encoding="utf-8")
    if hashlib.sha256(original.encode()).hexdigest() != report["source_sha256"]:
        raise ValueError("Original repository changed since challenge")
    if hashlib.sha256(candidate.encode()).hexdigest() != report["candidate_sha256"]:
        raise ValueError("Untrusted artifact checksum changed")
    _, line = _original_assignment(original)
    index = report["changed_line"]-1
    line = candidate.splitlines()[index]
    if build_candidate(original, line) != candidate or not _check_source(candidate):
        raise ValueError("Candidate failed structural/behavioral revalidation")
    if (output/"trusted-url-regression.py").read_text(encoding="utf-8") != REGRESSION:
        raise ValueError("Regression tests were tampered with")


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["generate", "verify"])
    parser.add_argument("--repo", default=".")
    parser.add_argument("--out", default="results/real-repo")
    args = parser.parse_args()
    if args.action == "generate":
        return generate(Path(args.repo), Path(args.out))
    verify(Path(args.repo), Path(args.out))
    print("REAL_REPOSITORY_CANDIDATE_REVALIDATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
