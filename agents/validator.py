"""Synthesizer agent: transforms findings into coherent reports and summaries."""

from __future__ import annotations

from typing import Any, Dict

from .base import AgentConfig, AgentRole, BaseAgent


class SynthesizerAgent(BaseAgent):
    def __init__(self, config: AgentConfig | None = None):
        super().__init__(
            config or AgentConfig(
                name="Synthesizer",
                role=AgentRole.SYNTHESIZER,
                description="Produces research reports and summaries from collected findings.",
                temperature=0.6,
            )
        )

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        self.state["status"] = "running"
        self.state["current_task"] = task

        report = {
            "task": task,
            "title": f"Research Brief: {task}",
            "sections": [
                "Executive Summary",
                "Key Findings",
                "Performance Overview",
                "Recommendations",
            ],
            "context": context,
        }

        self.state["status"] = "completed"
        return report

    async def analyze(self, data: Any) -> Dict[str, Any]:
        return {
            "report_status": "Generated",
            "summary": "Narrative output synthesized successfully.",
            "data": data,
        }
