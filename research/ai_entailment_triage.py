"""Optional model-assisted entailment triage with strict human-gold evaluation.

The model only suggests labels. It never overwrites or creates human reviews.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

from research.relationship_review import RELATIONS, evaluate_relationships
from research.source_passage_verification import verify_passages

SYSTEM_PROMPT = (
    "You are a cautious research evidence triage assistant. Evaluate whether the "
    "quoted evidence supports, contradicts, is insufficient for, or is out of scope "
    "for the stated proposition and scope. Return ONLY JSON with keys relation and "
    "rationale. relation must be one of supports, contradicts, insufficient, "
    "out_of_scope. Treat ambiguous or non-conclusive evidence as insufficient. "
    "Never infer facts beyond the quotation; never claim scientific verification."
)


def _ask_model(claim: dict, link: dict, *, endpoint: str, model: str, token: str) -> dict:
    """OpenAI-compatible chat completion endpoint; opt-in only, not used in CI."""
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps({
                "proposition": claim["proposition"], "scope": claim["scope"],
                "quotation": link["quote"], "locator": link["locator"],
            }, ensure_ascii=False)},
        ],
    }).encode("utf-8")
    request = Request(endpoint, data=body, headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    }, method="POST")
    with urlopen(request, timeout=25) as response:
        if response.status != 200:
            raise ValueError("Model endpoint returned non-200 status")
        raw = response.read(100_001)
        if len(raw) > 100_000:
            raise ValueError("Model response too large")
    result = json.loads(json.loads(raw)["choices"][0]["message"]["content"])
    if not isinstance(result, dict) or result.get("relation") not in RELATIONS:
        raise ValueError("Model returned an invalid relation")
    rationale = result.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip() or len(rationale) > 2000:
        raise ValueError("Model returned invalid rationale")
    return {"relation": result["relation"], "rationale": rationale}


def suggest(payload: dict, source_dir: str | Path, model_fn) -> dict:
    """Propose only for exact-matching quotes; fail closed for unmatched evidence."""
    screening = verify_passages(payload, source_dir)
    lookup = {(x["claim_id"], x["doi"], x["locator"]): x for x in screening["findings"]}
    suggestions = []
    for claim in payload["claims"]:
        for link in claim["evidence"]:
            key = (claim["id"], link["doi"], link["locator"])
            finding = lookup[key]
            if not finding["quote_exact_match"]:
                suggestions.append({"claim_id": key[0], "doi": key[1], "locator": key[2],
                                    "relation": None, "status": "abstained_quote_mismatch"})
                continue
            answer = model_fn(claim, link)
            if not isinstance(answer, dict) or answer.get("relation") not in RELATIONS:
                raise ValueError("Invalid model prediction")
            rationale = answer.get("rationale")
            if not isinstance(rationale, str) or not rationale.strip() or len(rationale) > 2000:
                raise ValueError("Invalid model rationale")
            suggestions.append({"claim_id": key[0], "doi": key[1], "locator": key[2],
                                "relation": answer["relation"], "rationale": rationale,
                                "status": "unverified_model_suggestion"})
    return {"status": "model_triage_only", "suggestions": suggestions,
            "scientific_support_verified": False}


def score_against_human(payload: dict, source_dir: str | Path, predictions: dict) -> dict:
    """Score only independent, explicitly reviewed gold labels; never manufacture them."""
    human = evaluate_relationships(payload, source_dir)
    if not isinstance(predictions, dict) or not isinstance(predictions.get("suggestions"), list):
        raise ValueError("Invalid predictions")
    pred_map = {}
    for row in predictions["suggestions"]:
        if not isinstance(row, dict):
            raise ValueError("Invalid prediction row")
        key = (row.get("claim_id"), row.get("doi"), row.get("locator"))
        if key in pred_map:
            raise ValueError("Duplicate prediction")
        if row.get("relation") is not None and row["relation"] not in RELATIONS:
            raise ValueError("Unknown predicted label")
        pred_map[key] = row.get("relation")
    eligible = [r for r in human["links"] if r["review_status"] == "reviewed"]
    gold_keys = {(r["claim_id"], r["doi"], r["locator"]) for r in human["links"]}
    if set(pred_map) - gold_keys:
        raise ValueError("Prediction references unknown evidence")
    evaluated = []
    for row in eligible:
        key = (row["claim_id"], row["doi"], row["locator"])
        predicted = pred_map.get(key)
        evaluated.append({"claim_id": key[0], "doi": key[1], "locator": key[2],
                          "human_label": row["relation"], "model_label": predicted,
                          "correct": predicted == row["relation"]})
    total = len(evaluated)
    correct = sum(r["correct"] for r in evaluated)
    return {"status": "evaluation_against_human_annotations",
            "reviewed_count": total, "correct_count": correct,
            "accuracy": correct / total if total else None,
            "coverage": sum(r["model_label"] is not None for r in evaluated) / total if total else None,
            "evaluations": evaluated, "scientific_validity_established": False}


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description="Optional model triage and human-label evaluation")
    parser.add_argument("--input", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--predictions", help="Existing prediction JSON for offline scoring")
    parser.add_argument("--endpoint", help="Explicit trusted HTTPS chat-completions endpoint")
    parser.add_argument("--model", help="Model identifier for opt-in inference")
    args = parser.parse_args(argv)
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if args.predictions:
        result = score_against_human(payload, args.source_dir,
                                     json.loads(Path(args.predictions).read_text(encoding="utf-8")))
    else:
        if not args.endpoint or not args.endpoint.startswith("https://") or not args.model:
            parser.error("Inference requires --endpoint https://... and --model")
        token = os.environ.get("RESEARCH_LLM_API_KEY")
        if not token:
            parser.error("RESEARCH_LLM_API_KEY is required for opt-in inference")
        result = suggest(payload, args.source_dir,
                         lambda claim, link: _ask_model(claim, link, endpoint=args.endpoint,
                                                      model=args.model, token=token))
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, sort_keys=True, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "accuracy": result.get("accuracy")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
