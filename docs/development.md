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

Additional frontend quality commands:

```bash
npm run lint
npx playwright install chromium
npm run test:e2e
```

The frontend reads these optional environment variables:

```text
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/api/v1/events/ws
```

When omitted, the same local URLs are used as defaults. Docker Compose injects them explicitly.

## Robot simulator

```bash
cd clients/python-simulator
uv sync --dev
uv run pytest -q
uv run ruff check .
uv run tars-robot-sim --mqtt-host localhost --serial-number RB-SIM-001 --once
```

## Docker

```bash
docker compose config
docker compose up --build
```

The backend container applies all Alembic migrations before starting Uvicorn. To reproduce the
clean-stack verification used by CI:

```bash
docker compose -p tars-e2e --profile simulator up --build --wait -d
python scripts/e2e_order_flow.py
cd frontend
npm run test:e2e
cd ..
docker compose -p tars-e2e --profile simulator down -v
```

The Python smoke script verifies a complete graph/mission/order cycle through the real broker and
waits until the simulator returns the dispatched `orderId` in its state.

Optional simulator profile:

```bash
docker compose --profile simulator up --build robot-simulator
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

Or use the simulator client:

```bash
docker compose --profile simulator run --rm robot-simulator \
  uv run tars-robot-sim --mqtt-host mosquitto --serial-number RB-SIM-001 --once
```

Then check the API:

```bash
curl http://localhost:8000/api/v1/robots
```
