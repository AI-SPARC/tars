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

## Database migrations

```bash
docker compose up -d postgres
cd backend
DATABASE_URL='postgresql+asyncpg://tars:tars@localhost:5432/tars' uv run alembic upgrade head
```

## MQTT smoke test

Start the stack with MQTT enabled:

```bash
docker compose up --build
```

Publish a VDA 5050 v3.0.0 connection message:

```bash
docker compose exec mosquitto mosquitto_pub \
  -t 'vda5050/v3/ResearchBot/RB001/connection' \
  -q 1 \
  -m '{"headerId":1,"timestamp":"2026-06-25T13:00:00.000Z","version":"3.0.0","manufacturer":"ResearchBot","serialNumber":"RB001","connectionState":"ONLINE"}'
```

Then check the API:

```bash
curl http://localhost:8000/api/v1/robots
```
