# Architecture

TARS is a monorepo with four main runtime components:

1. **Frontend** — React/TypeScript operator UI.
2. **Backend** — FastAPI fleet control API and VDA 5050 orchestration services.
3. **PostgreSQL** — persistent storage for robots, states, maps, missions, and MQTT logs.
4. **Mosquitto** — MQTT broker for VDA 5050 topics.

The backend acts as the VDA 5050 **fleet control**. It publishes `order`, `instantActions`, `zoneSet`, and `responses`, and consumes `state`, `connection`, `factsheet`, and `visualization`.

## Runtime events

Backend domain services publish process-local events after database commits. Web clients consume
them through `/api/v1/events/ws`. Subscriber queues are isolated and bounded so a slow dashboard
does not apply backpressure to MQTT ingestion or mission dispatch. A distributed event backend is
outside the MVP scope and will be needed before running multiple backend replicas.

## Frontend data layer

The React application uses a typed Fetch API client and TanStack Query. Robots, maps, missions,
robot state, and MQTT logs have stable cache keys. The WebSocket event stream writes live robot
state directly into its cache entry and invalidates related fleet, mission, and MQTT queries.

Runtime endpoints are configured with `VITE_API_BASE_URL` and `VITE_WS_URL`. Defaults target the
local backend at `http://localhost:8000/api/v1` and `ws://localhost:8000/api/v1/events/ws`.

The dashboard composes independently cached robot, map, mission, recent MQTT, and invalid-message
queries. Partial API failures are surfaced without hiding successfully loaded operational data.

The mission workspace uses the same persisted graph for route preview and backend dispatch. The
operator selects a robot and graph endpoints, creates an assigned mission, then receives the exact
validated VDA 5050 order payload after MQTT publication.

The MQTT/VDA workspace reads the paginated persistence API with filters encoded in its query key.
WebSocket message events invalidate the MQTT cache prefix, preserving the active filters while
refreshing the current page. Payloads and schema validation errors remain inspectable side by side.
