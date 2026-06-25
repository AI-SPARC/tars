# Development

## Backend

```bash
cd backend
uv sync --all-extras --dev
uv run pytest -q
uv run ruff check .
```

## Frontend

```bash
cd frontend
npm install
npm test -- --run
npm run build
```

## Docker

```bash
docker compose config
docker compose up --build
```
