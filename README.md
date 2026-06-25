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

## Status

Early rewrite in progress. The initial deliverable is a Dockerized MVP foundation with VDA 5050 schema validation and MQTT-ready architecture.
