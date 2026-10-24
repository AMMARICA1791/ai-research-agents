#!/usr/bin/env python3
"""Idempotently publish existing radar islands as standalone public repositories.

Requires a credential allowed to create public repositories in OWNER's account.
Never deletes source directories or force-pushes existing repositories.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def run(args, *, cwd=None, check=True, env=None):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=check, env=env)


def api(*args):
    result = run(["gh", "api", *args], check=False)
    if result.returncode:
        raise RuntimeError(f"GitHub API request failed (status {result.returncode}): {result.stderr[-600:]}")
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    owner = os.environ["OWNER"]
    if not re.fullmatch(r"[A-Za-z0-9-]+", owner):
        raise ValueError("Unexpected GitHub owner")
    root = Path("projects/incubator")
    if not root.is_dir():
        print("No incubator directory")
        return
    done = 0
    attempted = set()
    for island in sorted(root.iterdir()):
        if done >= args.limit:
            break
        if not island.is_dir() or not re.fullmatch(r"[a-zA-Z0-9_-]+", island.name):
            continue
        # Publish one discoverable public repository per project family.
        # Signal hashes are provenance identifiers, not public project names.
        family = re.sub(r"-[0-9a-f]{16}$", "", island.name)
        titles = {
            "agent_security": "authorization-trust-gate",
            "source_claim": "source-claim-traceability",
            "web_protocols": "web-protocol-experiments",
            "privacy": "privacy-checks",
            "provenance": "evidence-provenance",
        }
        name = titles.get(family)
        if not name:
            print(f"SKIP {island.name}: unknown family needs a descriptive title")
            continue
        name = "radar-" + name
        if name in attempted:
            continue
        attempted.add(name)
        if not (island / "prototype.py").is_file() or not (island / "test_prototype.py").is_file():
            print(f"SKIP {island.name}: no executable prototype and test")
            continue
        gate = run(["python", "scripts/island_release_gate.py", str(island)], check=False)
        if gate.returncode:
            print(f"SKIP {island.name}: {gate.stdout.strip()}")
            continue
        check = run(["python", "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py", "-v"], cwd=island, check=False)
        if check.returncode:
            print(f"SKIP {island.name}: tests failed: {check.stderr[-350:]}")
            continue
        result = run(["gh", "api", f"repos/{owner}/{name}"], check=False)
        if result.returncode == 0:
            existing = json.loads(result.stdout)
            if existing.get("private") or existing.get("owner", {}).get("login", "").lower() != owner.lower():
                print(f"SKIP {name}: existing repository is not owned public island")
                continue
            print(f"EXISTS https://github.com/{owner}/{name} (never overwrite)")
            continue
        if "HTTP 404" not in result.stderr and "Not Found" not in result.stderr:
            print(f"ERROR lookup {name}: {result.stderr[-400:]}")
            continue
        print(f"CREATING public island: {owner}/{name}", flush=True)
        try:
            created = api("-X", "POST", "user/repos", "-f", f"name={name}",
                          "-f", "description=Open radar-generated prototype: tests, failures, and community fixes welcome.",
                          "-F", "private=false", "-F", "has_issues=true", "-F", "has_wiki=false")
        except RuntimeError as error:
            print(f"ERROR creating {name}: {error}")
            continue
        if created.get("private") is not False or created.get("full_name", "").lower() != f"{owner}/{name}".lower():
            print(f"ERROR unexpected repository result for {name}; will not push")
            continue
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            for file in island.iterdir():
                if file.is_file() and file.name not in {".tests-passed"} and not file.name.startswith(".env"):
                    (dest / file.name).write_bytes(file.read_bytes())
            (dest / "CONTRIBUTING.md").write_text(
                "# Contributing to this island\n\n"
                "This is an experimental, unvalidated radar prototype. Reproduce problems with "
                "`python -m unittest discover -s . -p 'test_*.py' -v`. "
                "Open an issue describing expected versus actual results, or propose a pull request "
                "with regression tests. Never include secrets or personal data.\n")
            (dest / ".gitignore").write_text("__pycache__/\n*.pyc\n.env\n")
            for command in [["git", "init", "-b", "main"], ["git", "config", "user.name", "github-actions[bot]"],
                            ["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"],
                            ["git", "add", "."], ["git", "commit", "-m", "Publish independent radar island"]]:
                run(command, cwd=dest)
            # Token is supplied via environment, not written into remote URL or process arguments.
            askpass = dest / "git-askpass.sh"
            askpass.write_text('#!/bin/sh\ncase "$1" in *Username*) echo "x-access-token";; *) echo "$GH_TOKEN";; esac\n')
            askpass.chmod(0o700)
            git_env = dict(os.environ, GIT_ASKPASS=str(askpass), GIT_TERMINAL_PROMPT="0")
            run(["git", "remote", "add", "origin", f"https://github.com/{owner}/{name}.git"], cwd=dest)
            try:
                run(["git", "push", "-u", "origin", "main"], cwd=dest, env=git_env)
            except subprocess.CalledProcessError as error:
                print(f"ERROR pushing {name}: {error.stderr[-500:]}")
                continue
            finally:
                askpass.unlink(missing_ok=True)
        done += 1
        print(f"PUBLISHED https://github.com/{owner}/{name}", flush=True)
    print(f"New public islands published this run: {done}")


if __name__ == "__main__":
    main()
