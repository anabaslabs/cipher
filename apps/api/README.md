# CNS Solver API

FastAPI backend for the CNS Solver project.

## Setup

```bash
cd apps/api
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
```

## Development

```bash
uvicorn app.main:app --reload
```

Or from the monorepo root:

```bash
turbo dev --filter=api
```

The API runs at [http://localhost:8000](http://localhost:8000).  
Interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).
