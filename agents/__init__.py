"""Entry point for the AI Research Agents platform."""

import argparse
import asyncio
import logging
from typing import Any, Dict

from agents import (
    AnalystAgent,
    BenchmarkerAgent,
    ExplorerAgent,
    SynthesizerAgent,
    ValidatorAgent,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def initialize_agents() -> Dict[str, Any]:
    """Create and return all agent instances."""
    return {
        "explorer": ExplorerAgent(),
        "analyst": AnalystAgent(),
        "benchmarker": BenchmarkerAgent(),
        "synthesizer": SynthesizerAgent(),
        "validator": ValidatorAgent(),
    }


async def run_demo() -> None:
    """Run a simple demo workflow for the platform."""
    agents = await initialize_agents()

    task = "Compare leading open-source AI research tools"
    context = {"domain": "AI research", "scope": "tools and benchmarking"}

    overview = await agents["explorer"].execute(task, context)
    analysis = await agents["analyst"].execute(task, {"results": overview})
    benchmark = await agents["benchmarker"].execute(task, {"analysis": analysis})
    synthesis = await agents["synthesizer"].execute(task, {"benchmark": benchmark})
    validation = await agents["validator"].execute(task, {"report": synthesis})

    logger.info("Explorer result: %s", overview)
    logger.info("Analyst result: %s", analysis)
    logger.info("Benchmarker result: %s", benchmark)
    logger.info("Synthesizer result: %s", synthesis)
    logger.info("Validator result: %s", validation)

    print("\nAI Research Agents Platform Demo Completed.")
    print("Agents used:", list(agents.keys()))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Research Agents platform")
    parser.add_argument("--demo", action="store_true", help="Run the research workflow demo")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.demo:
        asyncio.run(run_demo())
    else:
        print("AI Research Agents Platform")
        print("Usage: python main.py --demo")
