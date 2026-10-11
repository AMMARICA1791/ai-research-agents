"""Key-free local model reviewer running against Ollama on loopback only.

Genuine open-weight inference requires an Ollama server/model installed on the
runner; unit tests with a mock do not count as real model execution.
"""
from __future__ import annotations

from collections import Counter
import requests


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

    def summarize(self, goal: str, evidence: list[dict]) -> dict:
        rules = dict(sorted(Counter(str(x.get("rule", "unknown"))[:40]
                                    for x in evidence[:100]).items()))
        # Do not transmit goal, source content, filenames, file paths, secrets
        # or prior research. The model sees aggregate counts only.
        data = {"finding_count": min(len(evidence), 100), "rule_counts": rules}
        roles = [
            ("research_analyst",
             "You are a research analyst. Analyze observed rule counts only. "
             "Give a cautious, grounded insight in at most 70 words."),
            ("critical_reviewer",
             "You are a skeptical peer reviewer. Explain uncertainty in the "
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
