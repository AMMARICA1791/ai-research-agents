"""Key-free local model reviewer running against Ollama on loopback only.

Genuine open-weight inference requires an Ollama server/model installed on the
runner; unit tests with a mock do not count as real model execution.
"""
from __future__ import annotations

from collections import Counter
import requests

from .knowledge import ALLOWED_RULES


class LocalOllamaModel:
    """Two bounded critiques from an ungated open model, no API keys."""

    endpoint = "http://127.0.0.1:11434/api/chat"

    def __init__(self, model: str = "qwen2.5:0.5b"):
        # Fix both model and endpoint to avoid inadvertent external fetches.
        if model != "qwen2.5:0.5b":
            raise ValueError("This bounded free-tier runner supports qwen2.5:0.5b only")
        self.model = model

    @property
    def configured(self) -> bool:
        # Enabled intentionally; availability is checked by real HTTP responses.
        return True

    def summarize(self, goal: str, evidence: list[dict], history: dict | None = None) -> dict:
        rules = dict(sorted(Counter(x.get("rule") if x.get("rule") in ALLOWED_RULES else "unknown"
                                    for x in evidence[:100]).items()))
        # Do not transmit goal, source content, filenames, file paths, secrets
        # or prior research. The model sees aggregate counts only.
        # The continuity context is tightly allowlisted, even for untrusted
        # callers. Never include raw history, model narratives or file paths.
        h = history if isinstance(history, dict) else {}
        past = h.get("previous_rule_counts", {})
        past = past if isinstance(past, dict) else {}
        old_counts = {
            key: min(max(int(value), 0), 100)
            for key, value in past.items()
            if key in ALLOWED_RULES and type(value) is int
        }
        raw_lessons = h.get("lessons", [])
        lessons = []
        if isinstance(raw_lessons, list):
            for item in raw_lessons[:7]:
                if not isinstance(item, dict):
                    continue
                key = item.get("rule")
                streak = item.get("consecutive_runs")
                if key in ALLOWED_RULES and type(streak) is int:
                    lessons.append({"rule": key, "consecutive_runs": min(max(streak, 0), 120)})
        runs = h.get("previous_runs", 0)
        runs = min(max(runs, 0), 120) if type(runs) is int else 0
        data = {
            "finding_count": min(len(evidence), 100),
            "rule_counts": rules,
            "previous_runs": runs,
            "previous_rule_counts": dict(sorted(old_counts.items())),
            "recurring_observations": lessons,
        }
        roles = [
            ("research_analyst",
             "You are a research analyst. Compare current and previous rule counts only. "
             "Give a cautious, grounded insight in at most 70 words."),
            ("critical_reviewer",
             "You are a skeptical peer reviewer. Critique possible trends and uncertainty in the "
             "observed counts and suggest one check. At most 70 words."),
        ]
        reviews: list[dict] = []
        try:
            for role, instructions in roles:
                response = requests.post(
                    self.endpoint,
                    json={
                        "model": self.model,
                        "stream": False,
                        "keep_alive": "0s",
                        "messages": [
                            {"role": "system", "content": instructions +
                             " Do not claim tests ran, infer security, or order code execution."},
                            {"role": "user", "content": "Static analysis aggregate counts: " + str(data)},
                        ],
                        "options": {"temperature": 0.1, "num_predict": 110, "num_ctx": 1024},
                    },
                    timeout=(5, 100),
                    allow_redirects=False,
                )
                response.raise_for_status()
                content = response.json().get("message", {}).get("content", "")
                if not isinstance(content, str) or not content.strip():
                    raise ValueError("Model returned an empty answer")
                reviews.append({"role": role, "text": content.strip()[:900]})
            return {
                "mode": "local_model", "model": self.model,
                "narrative": reviews[0]["text"],
                "reviews": reviews, "source": "aggregated_counts_loopback_only",
            }
        except (requests.RequestException, ValueError, TypeError, KeyError):
            return {
                "mode": "local_model_unavailable", "model": self.model,
                "narrative": None, "reviews": reviews,
                "source": "aggregated_counts_loopback_only",
            }
