# TARS Python Robot Simulator

A small VDA 5050 v3.0.0 mobile robot simulator for local research and integration tests.

It publishes:

- `connection` with QoS 1 and retained flag;
- `factsheet` once at startup;
- `state` once or periodically.

It subscribes to:

- `order`;
- `instantActions`.

## Run locally

```bash
uv sync --dev
uv run tars-robot-sim --mqtt-host localhost --serial-number RB-SIM-001 --once
```

For continuous state publishing:

```bash
uv run tars-robot-sim --mqtt-host localhost --serial-number RB-SIM-001 --state-interval 2
```

## Run with Docker Compose

From the repository root:

```bash
docker compose --profile simulator up --build robot-simulator
```
