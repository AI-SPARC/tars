# TARS — VDA 5050 Open-Source Fleet Manager

TARS is an open-source research-oriented fleet manager for heterogeneous mobile robot fleets, targeting **VDA 5050 v3.0.0**.

The project is intentionally built as a web application with a reproducible Docker setup and no user login in the MVP, so it can be used in laboratories, teaching, simulations, and algorithm research.

## Scope

- Fleet control for VDA 5050 v3.0.0 mobile robots.
- MQTT communication through Mosquitto.
- JSON Schema validation using the official VDA 5050 v3.0.0 schemas.
- FastAPI backend, PostgreSQL persistence, React/TypeScript frontend.
- Research-friendly observability: MQTT logs, state snapshots, mission history, map graph and routing.

## Quickstart

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Backend API: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs
- Frontend: http://localhost:5173
- MQTT broker: localhost:1883
- PostgreSQL: localhost:5432

Optional robot simulator:

```bash
docker compose --profile simulator run --rm robot-simulator uv run tars-robot-sim --mqtt-host mosquitto --serial-number RB-SIM-001 --once
```



## VDA 5050 target

This repository targets VDA 5050 **v3.0.0**.

Suggested local MQTT topic structure:

```text
vda5050/v3/{manufacturer}/{serialNumber}/{topic}
```

Relevant topics:

- `order`
- `instantActions`
- `state`
- `connection`
- `factsheet`
- `visualization`
- `zoneSet`
- `responses`

## Development

See:

- `docs/architecture.md`
- `docs/development.md`
- `docs/vda5050-compliance.md`
- `docs/mqtt-topics.md`
- `docs/roadmap.md`

## Status

MVP rewrite in progress. Robot discovery and telemetry ingestion, graph maps and routing, mission
creation, VDA 5050 order dispatch, persistence, MQTT log inspection, real-time WebSocket events,
a live operations dashboard, fleet/robot detail pages, and a basic simulator are implemented.
A graph map editor/viewer and mission builder/dispatcher are also available. The protocol-log
operator page and full Docker broker E2E remain in progress.
