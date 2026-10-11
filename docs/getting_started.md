"""FastAPI web application for the AI Research Agents Platform."""

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import (
    AnalystAgent,
    BenchmarkerAgent,
    ExplorerAgent,
    SynthesizerAgent,
    ValidatorAgent,
)
from agents.data_engineer import DataEngineerAgent
from agents.nlp_specialist import NLPSpecialistAgent
from agents.performance_engineer import PerformanceEngineerAgent
from agents.research_synthesizer import ResearchSynthesizerAgent
from agents.vision_specialist import VisionSpecialistAgent

app = FastAPI(
    title="AI Research Agents Platform",
    description="Multi-agent AI research platform for discovering and analyzing AI tools",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    task: str
    domain: str = "ai_tools"
    scope: str = "comprehensive"


class PipelineRequest(BaseModel):
    task: str
    agents: List[str] = ["explorer", "analyst", "benchmarker", "synthesizer", "validator"]


agents_map = {
    "explorer": ExplorerAgent(),
    "analyst": AnalystAgent(),
    "benchmarker": BenchmarkerAgent(),
    "synthesizer": SynthesizerAgent(),
    "validator": ValidatorAgent(),
    "nlp_specialist": NLPSpecialistAgent(),
    "vision_specialist": VisionSpecialistAgent(),
    "performance_engineer": PerformanceEngineerAgent(),
    "research_synthesizer": ResearchSynthesizerAgent(),
    "data_engineer": DataEngineerAgent(),
}


@app.get("/api/agents")
async def get_agents() -> Dict[str, Any]:
    return {
        "agents": [
            {"name": name, "status": "active", "role": agent.config.role.value}
            for name, agent in agents_map.items()
        ],
        "total": len(agents_map),
    }


@app.get("/api/agents/{agent_name}")
async def get_agent_status(agent_name: str) -> Dict[str, Any]:
    if agent_name not in agents_map:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return agents_map[agent_name].get_status()


@app.post("/api/research/execute")
async def execute_research(request: ResearchRequest) -> Dict[str, Any]:
    agent = agents_map.get("explorer")
    result = await agent.execute(request.task, {"domain": request.domain, "scope": request.scope})
    return {"task": request.task, "result": result}


@app.post("/api/research/pipeline")
async def execute_pipeline(request: PipelineRequest) -> Dict[str, Any]:
    if not request.agents:
        raise HTTPException(status_code=400, detail="At least one agent must be selected")

    pipeline_results = {}
    context = {"task": request.task}

    for agent_name in request.agents:
        if agent_name not in agents_map:
            continue
        agent = agents_map[agent_name]
        result = await agent.execute(request.task, context)
        pipeline_results[agent_name] = result
        context[f"{agent_name}_result"] = result

    return {
        "task": request.task,
        "agents_executed": request.agents,
        "results": pipeline_results,
        "status": "completed",
    }


@app.get("/api/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "agents": str(len(agents_map))}


@app.get("/")
async def root() -> str:
    return """
    <html>
    <head><title>AI Research Agents Platform</title></head>
    <body>
        <h1>AI Research Agents Platform</h1>
        <p>Multi-agent AI research dashboard and execution engine</p>
        <p>Open /docs to inspect the API.</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
