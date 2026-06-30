# MQTT Topics

Target VDA 5050 version: **3.0.0**.

Suggested local topic shape:

```text
vda5050/v3/{manufacturer}/{serialNumber}/{topic}
```

Examples:

```text
vda5050/v3/ResearchBot/RB001/state
vda5050/v3/ResearchBot/RB001/order
vda5050/v3/ResearchBot/RB001/connection
```

Minimal connection payload:

```json
{
  "headerId": 1,
  "timestamp": "2026-06-25T13:00:00.000Z",
  "version": "3.0.0",
  "manufacturer": "ResearchBot",
  "serialNumber": "RB001",
  "connectionState": "ONLINE"
}
```

Outbound `order` and `instantActions` messages use the same header identity. Orders are built from
the persisted graph with alternating node/edge sequence IDs; instant actions contain one or more
actions with `blockingType: "NONE"`.

QoS:

- QoS 0: `order`, `instantActions`, `state`, `factsheet`, `zoneSet`, `responses`, `visualization`.
- QoS 1: `connection`.

## Backend inbound runtime

When `MQTT_ENABLED=true`, the backend starts an MQTT worker on FastAPI startup and subscribes to:

```text
vda5050/v3/+/+/+
```

Inbound message pipeline:

```text
MQTT message received
  -> parse VDA topic
  -> validate payload against official VDA 5050 v3.0.0 JSON Schema
  -> persist mqtt_message_logs row
  -> get_or_create robot by manufacturer + serialNumber
  -> apply domain update for connection/factsheet/state
```

Currently applied updates:

- `connection`: updates `robots.last_connection_state` and `last_seen_at`.
- `factsheet`: stores raw factsheet and extracts coarse capability fields.
- `state`: stores a `robot_state_snapshots` row and updates `last_seen_at`.

## Backend outbound runtime

Assigned missions can be dispatched through the REST API. The backend resolves the mission's
route on its graph map, validates the generated VDA 5050 `order`, publishes it with QoS 0, and
stores both a `mission_orders` record and an outbound `mqtt_message_logs` record.

Order `headerId` values are monotonic per robot. A successfully published mission transitions
from `assigned` to `sent`.

Persisted inbound and outbound messages can be inspected through `GET /api/v1/mqtt/messages`.
The endpoint supports filters for direction, VDA message type, robot, and schema validity, plus
bounded pagination.

Invalid topics or invalid payloads are persisted in `mqtt_message_logs` with `schema_valid=false` and `validation_errors`, but they are not applied to robot domain tables.
