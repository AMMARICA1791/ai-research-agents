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

## Start the web interface

```bash
python run_server.py
```

Then visit:

- http://localhost:8000
- http://localhost:8000/docs

## Example usage

```python
from agents.nlp_specialist import NLPSpecialistAgent

agent = NLPSpecialistAgent()
result = await agent.execute(
    "Compare leading open-source LLMs",
    {"focus": "instruction tuning"},
)
```
