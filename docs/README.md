# Getting Started

## Environment setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run the demo

```bash
python main.py --demo
```

## Example research project

```python
from research.project import ResearchProject

project = ResearchProject(
    title="AI Tool Comparison",
    description="Compare open-source AI tooling options.",
    owner="research-team",
    tags=["ai", "tools", "benchmark"],
)

print(project.to_dict())
```

## Next steps

- expand agents with real model integrations
- add a SQLite or DuckDB layer
- add CLI commands for project creation
- build an API layer with FastAPI
