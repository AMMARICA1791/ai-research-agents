"""Read-only historical radar portfolio inventory using public GitHub API.

Never executes branch content. Incomplete inventory is explicitly reported.
"""
import argparse
import json
import os
import urllib.request
from pathlib import Path

def fetch_inventory(repo, token=None, max_pages=10):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "radar-council-inventory"}
    if token:
        headers["Authorization"] = "Bearer " + token
    entries = []
    seen = set()
    errors = []
    for page in range(1, max_pages + 1):
        url = "https://api.github.com/repos/" + repo + "/branches?per_page=100&page=" + str(page)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                branches = json.load(response)
            if not isinstance(branches, list):
                raise ValueError("unexpected branch response")
        except (OSError, ValueError) as exc:
            errors.append("branch_page_" + str(page) + ":" + type(exc).__name__)
            break
        for branch in branches:
            name = branch.get("name", "")
            if not name.startswith("radar/incubator-") or name in seen:
                continue
            seen.add(name)
            project_id = name[len("radar/incubator-"):]
            raw_url = "https://raw.githubusercontent.com/" + repo + "/refs/heads/" + name + "/projects/incubator/" + project_id + "/hypothesis.json"
            try:
                req = urllib.request.Request(raw_url, headers={"User-Agent": "radar-council-inventory"})
                with urllib.request.urlopen(req, timeout=12) as response:
                    raw = response.read(120001)
                if len(raw) > 120000:
                    raise ValueError("hypothesis_too_large")
                data = json.loads(raw.decode("utf-8"))
                if not isinstance(data, dict):
                    raise ValueError("invalid_hypothesis")
                entries.append({"branch": name, "project_id": project_id, "hypothesis": data})
            except (OSError, ValueError, UnicodeError) as exc:
                errors.append(project_id + ":" + type(exc).__name__)
                entries.append({"branch": name, "project_id": project_id, "hypothesis": {"topic": project_id.split("-")[0], "source_title": project_id, "source_id": project_id}, "metadata_only": True})
        if len(branches) < 100:
            break
    else:
        errors.append("branch_pagination_limit_reached")
    return {"repository": repo, "projects": entries, "complete": not errors, "errors": errors,
            "scope": "radar_incubator_branches_only", "retrieved_count": len(entries)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = fetch_inventory(args.repo, os.environ.get("GH_TOKEN"))
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"retrieved_count": result["retrieved_count"], "complete": result["complete"], "errors": result["errors"][:8]}))
