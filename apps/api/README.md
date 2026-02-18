# Cipher (API)

FastAPI backend for the Cipher project.

## Setup

```bash
cd apps/api
py -m venv .venv
```

```bash
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # macOS/Linux
```

```bash
pip install -r requirements.txt
```

## Development

```bash
turbo dev
```

Or from the monorepo root:

```bash
turbo dev -F api
```

## Production

```bash
turbo start
```

Or from the monorepo root:

```bash
turbo start -F api
```

## Usage

The API runs at [http://localhost:8000](http://localhost:8000).  
Interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).
