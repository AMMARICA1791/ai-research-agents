"""Deterministic pre-event hypothesis and runnable prototype generator.

This is a deliberately bounded seed factory, not a claim of autonomous invention.
All source text is treated as untrusted data, never code or instructions.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

SCENARIOS = {
    "agent_security": ("Agents increasingly perform consequential actions",
        "Can a minimal authorization gate prevent unapproved actions?",
        "A deterministic gate denies actions without trusted user approval."),
    "provenance": ("Generated claims proliferate faster than evidence reviews",
        "Can source snapshots reveal when quoted support disappears?",
        "A source change triggers a quote-presence recheck."),
    "web_protocols": ("Browser-agent protocols diversify",
        "Can an adapter reject unknown action schemas before execution?",
        "Unknown action types fail closed."),
    "privacy": ("More workflows process sensitive information",
        "Can a local redaction stage prevent obvious secret leakage?",
        "Matching secret patterns are replaced before export."),
}
def hypotheses(signal):
    if not isinstance(signal,dict):
        raise ValueError("signal must be object")
    topics=signal.get("signal",{}).get("topics",{})
    if not isinstance(topics,dict):
        raise ValueError("topics must be object")
    result=[]
    for topic in sorted(set(topics)&set(SCENARIOS)):
        trend,question,prediction=SCENARIOS[topic]
        result.append({"topic":topic,"trend_hypothesis":trend,
                       "research_question":question,"falsifiable_prediction":prediction,
                       "market_validated":False,"novelty_verified":False})
    return result

def scaffold(hypothesis, root):
    topic=hypothesis["topic"]
    if topic not in SCENARIOS:
        raise ValueError("unknown template")
    root=Path(root)
    project=root/topic
    project.mkdir(parents=True,exist_ok=True)
    # Code is from a trusted fixed template, never generated from feed text.
    code='''"""Minimal runnable proof-of-concept for an anticipated need."""
def evaluate(value):
    if not isinstance(value, dict):
        return False
    return bool(value.get("explicit_approval") is True and
                value.get("trusted_origin") == "user")
'''
    test='''import unittest
from prototype import evaluate
class PrototypeTests(unittest.TestCase):
    def test_denies_unapproved(self):
        self.assertFalse(evaluate({"explicit_approval": False, "trusted_origin": "user"}))
    def test_allows_approved(self):
        self.assertTrue(evaluate({"explicit_approval": True, "trusted_origin": "user"}))
if __name__ == "__main__":
    unittest.main()
'''
    # A generic gate template is a scaffolding exercise, not a topic-specific invention.
    (project/"prototype.py").write_text(code,encoding="utf-8")
    (project/"test_prototype.py").write_text(test,encoding="utf-8")
    (project/"hypothesis.json").write_text(json.dumps(hypothesis,indent=2)+"\n",encoding="utf-8")
    (project/"README.md").write_text(
        "# Anticipatory prototype: "+topic+"\n\n"
        "Experimental hypothesis only; generic authorization-gate scaffold. "
        "Not a validated solution to this topic.\n\n"
        "Run: `python -m unittest discover -s . -p 'test_*.py'`\n",encoding="utf-8")
    return str(project)

def generate(report, root):
    if not isinstance(report,dict) or not isinstance(report.get("signals"),list):
        raise ValueError("invalid radar report")
    output=[]
    seen=set()
    for signal in report["signals"]:
        for hypothesis in hypotheses(signal):
            topic=hypothesis["topic"]
            if topic in seen:
                continue
            seen.add(topic)
            output.append({"topic":topic,"path":scaffold(hypothesis,root),
                           "source_id":signal.get("id"),"status":"template_prototype"})
    return output

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",required=True)
    parser.add_argument("--output-dir",required=True)
    args=parser.parse_args()
    with open(args.report,encoding="utf-8") as file:
        report=json.load(file)
    result=generate(report,args.output_dir)
    print(json.dumps(result,indent=2))
