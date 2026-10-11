# Quick Start Guide

## Installation & Setup

### Prerequisites
- Python 3.9+
- pip or conda
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/AMMARICA1791/ai-research-agents.git
cd ai-research-agents
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Server
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn web.app:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Access the Web Interface
Open your browser and navigate to:
```
http://localhost:8000
```

## Using the MVP

### Analyze a Repository
1. **Default Analysis**: Click "Analyze" with "." to analyze the current project
2. **Custom Path**: Enter any local path to analyze
3. **Results**: View comprehensive analysis in JSON format

### What the Analysis Shows
- **Repository Summary**: Files, modules, languages used
- **File Structure**: Complete directory and file listing
- **Python Modules**: Classes, functions, imports extracted
- **Relationship Graph**: Connections between files and components
- **Statistics**: Line counts, file types, complexity metrics

## API Endpoints

### GET /
Web interface homepage

### GET /health
Health check endpoint
```bash
curl http://localhost:8000/health
```

### GET /api/demo
Demo analysis (analyzes current project)
```bash
curl http://localhost:8000/api/demo
```

### POST /api/analyze
Analyze a specific repository
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "repo_path=/path/to/repo"
```

## Example Output

```json
{
  "status": "ok",
  "summary": {
    "repo_name": "ai-research-agents",
    "total_files": 45,
    "python_files": 28,
    "total_lines": 8923,
    "top_level_directories": ["agents", "research", "web", "docs"]
  },
  "files": [...],
  "modules": [...],
  "graph": {"nodes": [...], "edges": [...]}
}
```

## Troubleshooting

### Port Already in Use
```bash
uvicorn web.app:app --host 0.0.0.0 --port 8001
```

### Permission Denied
```bash
chmod +x main.py
```

### Module Not Found
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Next Steps

- Explore the analysis results
- Analyze different repositories
- Integrate with your workflow
- Contribute improvements

## Support

For issues or questions:
- GitHub Issues: https://github.com/AMMARICA1791/ai-research-agents/issues
- Email: enterprise@ai-research-agents.io

---

**The platform is now running. Start analyzing.**
