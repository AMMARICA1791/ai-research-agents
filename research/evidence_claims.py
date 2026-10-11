"""Conservative, evidence-linked claim registry and deterministic conflict candidates.

A contradiction candidate is NOT a verified scientific contradiction.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DOI = re.compile(r"^10\.[0-9]{4,9}/[^\s]{1,160}$")
STANCES = {"supports", "refutes", "unclear"}
STATES = {"unreviewed", "human_reviewed"}


def canonical_digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()


def validate_claims(payload: dict) -> dict:
    """Validate explicit claims against a stored evidence ledger; fail closed."""
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError("Unsupported claims schema")
    ledger = payload.get("ledger")
    if not isinstance(ledger, dict):
        raise ValueError("Missing evidence ledger")
    declared = ledger.get("ledger_sha256")
    if not isinstance(declared, str) or declared != canonical_digest(
        {k: v for k, v in ledger.items() if k != "ledger_sha256"}
    ):
        raise ValueError("Evidence ledger digest mismatch")
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Missing evidence entries")
    known = {e.get("doi") for e in entries if isinstance(e, dict)}
    if not known or any(not isinstance(d, str) or not DOI.fullmatch(d) for d in known):
        raise ValueError("Invalid evidence entries")
    claims = payload.get("claims")
    if not isinstance(claims, list) or len(claims) > 100:
        raise ValueError("Invalid claims collection")
    ids = set()
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("Invalid claim")
        cid, proposition, scope = (claim.get(k) for k in ("id", "proposition", "scope"))
        if not isinstance(cid, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", cid) or cid in ids:
            raise ValueError("Duplicate or invalid claim id")
        ids.add(cid)
        if not isinstance(proposition, str) or not proposition.strip() or len(proposition) > 1000:
            raise ValueError("Invalid proposition")
        if not isinstance(scope, str) or not scope.strip() or len(scope) > 250:
            raise ValueError("Invalid comparison scope")
        if claim.get("review_status") not in STATES:
            raise ValueError("Invalid review status")
        evidence = claim.get("evidence")
        if not isinstance(evidence, list) or not evidence or len(evidence) > 20:
            raise ValueError("Claims require source-linked evidence")
        for link in evidence:
            if not isinstance(link, dict) or link.get("doi") not in known or link.get("stance") not in STANCES:
                raise ValueError("Unknown source or evidence stance")
            if not isinstance(link.get("locator"), str) or not link["locator"].strip():
                raise ValueError("Missing evidence locator")
            if len(link["locator"]) > 300:
                raise ValueError("Evidence locator too long")
    return payload


def assess_conflicts(payload: dict) -> dict:
    """Flag explicit opposing stances on an identical proposition and scope.

    This only detects candidates. No semantic entailment, replication, or scientific
    contradiction verification is performed.
    """
    validate_claims(payload)
    grouped = {}
    for claim in payload["claims"]:
        key = (claim["proposition"].strip().casefold(), claim["scope"].strip().casefold())
        for link in claim["evidence"]:
            if link["stance"] != "unclear":
                grouped.setdefault(key, []).append((claim, link))
    candidates = []
    for (proposition, scope), links in sorted(grouped.items()):
        supports = [(c, l) for c, l in links if l["stance"] == "supports"]
        refutes = [(c, l) for c, l in links if l["stance"] == "refutes"]
        if supports and refutes:
            candidates.append({
                "proposition": proposition,
                "scope": scope,
                "classification": "potential_evidence_conflict_requires_human_review",
                "supports": [{"claim_id": c["id"], "doi": l["doi"], "locator": l["locator"]}
                             for c, l in supports],
                "refutes": [{"claim_id": c["id"], "doi": l["doi"], "locator": l["locator"]}
                            for c, l in refutes],
                "scientific_contradiction_verified": False,
            })
    return {"status": "unreviewed_conflict_screening", "candidates": candidates,
            "candidate_count": len(candidates), "scientific_contradiction_verified": False}


def analyze_file(source: str | Path, destination: str | Path) -> dict:
    payload = json.loads(Path(source).read_text(encoding="utf-8"))
    result = assess_conflicts(payload)
    output = Path(destination)
    if output.exists():
        raise FileExistsError("Refusing to overwrite existing conflict report")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
    return result


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description="Screen explicitly linked research claims")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    result = analyze_file(args.input, args.output)
    print(json.dumps({"candidate_count": result["candidate_count"],
                      "scientific_contradiction_verified": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
