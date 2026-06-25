# Architecture

TARS is a monorepo with four main runtime components:

1. **Frontend** — React/TypeScript operator UI.
2. **Backend** — FastAPI fleet control API and VDA 5050 orchestration services.
3. **PostgreSQL** — persistent storage for robots, states, maps, missions, and MQTT logs.
4. **Mosquitto** — MQTT broker for VDA 5050 topics.

The backend acts as the VDA 5050 **fleet control**. It publishes `order`, `instantActions`, `zoneSet`, and `responses`, and consumes `state`, `connection`, `factsheet`, and `visualization`.
