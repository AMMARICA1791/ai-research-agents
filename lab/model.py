"""Optional language-model reasoning over metadata only; disabled without explicit settings."""
from __future__ import annotations

import os
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
        if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1"}):
            return {"mode": "invalid_endpoint", "narrative": None}
        # Never upload source content, environment variables, secrets, or SQLite memory.
        facts = [{"rule": x["rule"], "severity": x["severity"], "evidence": x["evidence"]} for x in evidence[:15]]
        try:
            response = requests.post(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model,
                      "messages": [
                          {"role": "system", "content": "You are a cautious research reviewer. Explain the given evidence; do not invent findings, measurements or successful tests. Propose only human-reviewed changes."},
                          {"role": "user", "content": "Goal: " + goal[:500] + "\nEvidence metadata: " + str(facts)},
                      ],
                      "temperature": 0.1, "max_tokens": 500},
                timeout=20)
            response.raise_for_status()
            value = response.json()["choices"][0]["message"]["content"]
            return {"mode": "remote_model", "narrative": str(value)[:4000]}
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
            return {"mode": "provider_error", "narrative": None}
