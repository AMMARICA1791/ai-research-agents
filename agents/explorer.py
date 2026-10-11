"""Base agent architecture for the AI Research Agents platform."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class AgentRole(str, Enum):
    EXPLORER = "explorer"
    ANALYST = "analyst"
    BENCHMARKER = "benchmarker"
    SYNTHESIZER = "synthesizer"
    VALIDATOR = "validator"


@dataclass
class AgentConfig:
    name: str
    role: AgentRole
    description: str
    model: str = "distilbert-base-uncased"
    temperature: float = 0.7
    max_tokens: int = 2048
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMessage:
    sender_id: str
    recipient_id: str
    content: str
    message_type: str = "standard"
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "content": self.content,
            "message_type": self.message_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


class BaseAgent(ABC):
    """Abstract base class for all specialized agent implementations."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.id = str(uuid4())
        self.memory: List[AgentMessage] = []
        self.state: Dict[str, Any] = {"status": "idle", "current_task": None}

    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent's primary task."""

    @abstractmethod
    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze the data with specialized logic."""

    async def communicate(self, recipient: "BaseAgent", message: str) -> AgentMessage:
        """Send a message to another agent."""
        msg = AgentMessage(
            sender_id=self.id,
            recipient_id=recipient.id,
            content=message,
            message_type="communication",
        )
        self.memory.append(msg)
        recipient.memory.append(msg)
        return msg

    def get_status(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.config.name,
            "role": self.config.role.value,
            "status": self.state["status"],
            "current_task": self.state["current_task"],
            "memory_size": len(self.memory),
        }

    def save_memory(self, filepath: str) -> None:
        """Persist memory to JSON-like output."""
        with open(filepath, "w", encoding="utf-8") as handle:
            handle.write("[\n")
            for index, message in enumerate(self.memory):
                suffix = "," if index < len(self.memory) - 1 else ""
                handle.write(f"  {message.to_dict()} {suffix}\n")
            handle.write("]\n")
