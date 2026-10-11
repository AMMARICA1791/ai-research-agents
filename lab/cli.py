"""Human-controlled entrypoint. No automatic Git pushes or source modification."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .memory import LabMemory
from .pipeline import LabOrchestrator

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Independent AI R&D lab")
    parser.add_argument("--db", default=".data/lab.sqlite", help="SQLite history path")
    sub = parser.add_subparsers(dest="command", required=True)
    mission = sub.add_parser("mission", help="Run read-only multi-agent self-research")
    mission.add_argument("--repo", default=".")
    mission.add_argument("--goal", required=True)
    mission.add_argument("--output", default="", help="Optional JSON report destination")
    mission.add_argument("--knowledge", default="", help="Optional sanitized cross-run JSON journal")
    sub.add_parser("history", help="List completed missions")
    sub.add_parser("proposals", help="List human-review proposals")
    review = sub.add_parser("review", help="Record human review; never executes changes")
    review.add_argument("--proposal", required=True)
    decisions = review.add_mutually_exclusive_group(required=True)
    decisions.add_argument("--approve", action="store_true")
    decisions.add_argument("--reject", action="store_true")
    args = parser.parse_args(argv)
    store = LabMemory(args.db)
    if args.command == "mission":
        result = LabOrchestrator(store, knowledge_path=args.knowledge or None).run(Path(args.repo), args.goal)
        if args.output:
            path = Path(args.output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "history":
        print(json.dumps(store.list_missions(), ensure_ascii=False, indent=2))
    elif args.command == "proposals":
        print(json.dumps(store.list_proposals(), ensure_ascii=False, indent=2))
    elif args.command == "review":
        if not store.decide(args.proposal, approve=args.approve):
            parser.error("Proposal does not exist or was already reviewed")
        print(json.dumps({"proposal": args.proposal, "decision": "approved" if args.approve else "rejected",
                          "source_changed": False}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
