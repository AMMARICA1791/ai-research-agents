"""Experiment definition and tracking."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4


@dataclass
class Experiment:
    name: str
    description: str
    template: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "queued"
    parameters: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "template": self.template,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "parameters": self.parameters,
            "results": self.results,
            "logs": self.logs,
        }
