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
# Fixed, audited, topic-specific offline demonstrations. No feed text becomes code.
PROTOTYPES = {
    "agent_security": ("def evaluate(value):\n    return isinstance(value, dict) and value.get(\"explicit_approval\") is True and value.get(\"trusted_origin\") == \"user\"\n", "import unittest\nfrom prototype import evaluate\nclass Tests(unittest.TestCase):\n    def test_denies_untrusted(self):\n        self.assertFalse(evaluate({\"explicit_approval\": True, \"trusted_origin\": \"web\"}))\n    def test_allows_approved(self):\n        self.assertTrue(evaluate({\"explicit_approval\": True, \"trusted_origin\": \"user\"}))\n"),
    "provenance": ("import hashlib\ndef snapshot(text, quotation):\n    if not isinstance(text, str) or not isinstance(quotation, str):\n        raise ValueError(\"text and quotation must be strings\")\n    return {\"sha256\": hashlib.sha256(text.encode(\"utf-8\")).hexdigest(), \"quote_present\": bool(quotation) and quotation in text}\ndef drift(previous, text, quotation):\n    current = snapshot(text, quotation)\n    return {\"content_changed\": current[\"sha256\"] != previous[\"sha256\"], \"quote_disappeared\": bool(previous[\"quote_present\"]) and not current[\"quote_present\"]}\n", "import unittest\nfrom prototype import snapshot, drift\nclass Tests(unittest.TestCase):\n    def test_quote_disappears(self):\n        old = snapshot(\"Research supports claim\", \"supports claim\")\n        self.assertTrue(drift(old, \"Research updated\", \"supports claim\")[\"quote_disappeared\"])\n    def test_no_change(self):\n        old = snapshot(\"stable\", \"stable\")\n        self.assertFalse(drift(old, \"stable\", \"stable\")[\"content_changed\"])\n"),
    "web_protocols": ("ALLOWED = {\"read_page\": {\"url\"}, \"summarize\": {\"text\"}}\ndef validate(action):\n    if not isinstance(action, dict) or set(action) != {\"type\", \"params\"}:\n        return False\n    kind, params = action[\"type\"], action[\"params\"]\n    return kind in ALLOWED and isinstance(params, dict) and set(params) == ALLOWED[kind] and all(isinstance(v, str) and bool(v.strip()) for v in params.values())\n", "import unittest\nfrom prototype import validate\nclass Tests(unittest.TestCase):\n    def test_unknown_rejected(self):\n        self.assertFalse(validate({\"type\":\"run_shell\",\"params\":{\"cmd\":\"echo hi\"}}))\n    def test_known_accepted(self):\n        self.assertTrue(validate({\"type\":\"summarize\",\"params\":{\"text\":\"hello\"}}))\n"),
    "privacy": ("import re\nPATTERNS = [re.compile(r\"(?i)(?:api[_-]?key|token|secret)[ ]*[:=][ ]*[A-Za-z0-9_-]{8,}\"), re.compile(r\"[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}\")]\ndef redact(text):\n    if not isinstance(text, str):\n        raise ValueError(\"text must be a string\")\n    for pattern in PATTERNS:\n        text = pattern.sub(\"[REDACTED]\", text)\n    return text\n", "import unittest\nfrom prototype import redact\nclass Tests(unittest.TestCase):\n    def test_secret(self):\n        self.assertNotIn(\"abcd123456\", redact(\"token=abcd123456\"))\n    def test_email(self):\n        self.assertEqual(redact(\"hello me@example.org\"), \"hello [REDACTED]\")\n"),
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

def scaffold(hypothesis, root, project_id=None):
    topic=hypothesis["topic"]
    if topic not in SCENARIOS:
        raise ValueError("unknown template")
    root=Path(root)
    project=root/(project_id or topic)
    project.mkdir(parents=True,exist_ok=True)
    # Topic-specific code comes only from the trusted PROTOTYPES map.
    code, test = PROTOTYPES[topic]
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
        source_id=signal.get("id")
        if not isinstance(source_id,str) or not re.fullmatch(r"[a-fA-F0-9]{16,64}",source_id):
            # Older synthetic tests can use a short stable identifier.
            if not isinstance(source_id,str) or not source_id or len(source_id)>128:
                continue
            source_id=hashlib.sha256(source_id.encode()).hexdigest()[:16]
        source_id=source_id[:16].lower()
        for hypothesis in hypotheses(signal):
            topic=hypothesis["topic"]
            project_id=f"{topic}-{source_id}"
            if project_id in seen:
                continue
            seen.add(project_id)
            hypothesis["source_id"]=source_id
            hypothesis["source_title"]=str(signal.get("title",""))[:300]
            hypothesis["source_url"]=str(signal.get("url",""))[:500]
            output.append({"topic":topic,"project_id":project_id,
                           "path":scaffold(hypothesis,root,project_id),
                           "source_id":source_id,"status":"signal_specific_prototype"})

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
