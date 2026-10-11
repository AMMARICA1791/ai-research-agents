"""Optional real LLM reviewer via OpenAI-compatible HTTPS chat completion provider.

No GitHub Models dependency. It was retired in 2026. Provider is OFF without
three explicitly configured variables and explicit workflow opt-in.
"""
from __future__ import annotations

import os
from collections import Counter
from urllib.parse import urlparse

import requests


class OptionalModel:
    def __init__(self, endpoint=None, api_key=None, model=None):
        self.endpoint = endpoint if endpoint is not None else os.getenv("LAB_LLM_ENDPOINT", "")
        self.api_key = api_key if api_key is not None else os.getenv("LAB_LLM_API_KEY", "")
        self.model = model if model is not None else os.getenv("LAB_LLM_MODEL", "")

    @property
    def configured(self) -> bool:
        return bool(self.endpoint and self.api_key and self.model)

    def summarize(self, goal: str, evidence: list[dict]) -> dict:
        if not self.configured:
            return {"mode": "not_configured", "narrative": None}
        parsed = urlparse(self.endpoint)
        if not (parsed.scheme == "https" and parsed.hostname and not parsed.username
                and not parsed.password and not parsed.fragment):
            return {"mode": "invalid_endpoint", "narrative": None}
        # Aggregate ONLY: no goal, source code, file paths, free-text findings,
        # previous missions, secrets or user prompts are transferred.
        counts = dict(sorted(Counter(f.get("rule", "unknown") for f in evidence[:100]).items()))
        payload = {"finding_count": min(len(evidence), 100), "rule_counts": counts}
        reviewers = [
            ("research_analyst", "Act as a rigorous software research analyst. Explain only these measured category counts. State uncertainty."),
            ("critical_reviewer", "Act as a skeptical quality reviewer. Challenge unsupported interpretations. Suggest at most two tests; never claim a test ran."),
        ]
        reviews = []
        try:
            for role, system in reviewers:
                response = requests.post(
                    self.endpoint,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"model": self.model,
                          "messages": [
                              {"role": "system", "content": system + " No code execution or instructions to modify files."},
                              {"role": "user", "content": "Static analysis aggregates (no source text): " + str(payload)},
                          ], "temperature": 0.1, "max_tokens": 250},
                    timeout=18, allow_redirects=False,
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                reviews.append({"role": role, "text": str(content)[:1500]})
            return {"mode": "remote_model", "narrative": reviews[0]["text"],
                    "reviews": reviews, "source": "aggregated_counts_only"}
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
            return {"mode": "provider_error", "narrative": None,
                    "reviews": reviews, "source": "aggregated_counts_only"}
