# Advanced Architecture

## Multi-tier system

The platform is structured as a layered ecosystem:

### Core agents
- Explorer
- Analyst
- Benchmarker
- Synthesizer
- Validator

### Specialist agents
- NLP Specialist
- Vision Specialist
- Performance Engineer
- Data Engineer
- Research Synthesizer

## Data flow

```text
Goal -> Explorer -> Specialist analysis -> Benchmarking -> Synthesis -> Validation
```

## Knowledge layer

The research layer stores metadata and benchmark definitions to support comparisons and reasoning.

## Web layer

FastAPI exposes REST endpoints to interact with agent execution and monitoring.
