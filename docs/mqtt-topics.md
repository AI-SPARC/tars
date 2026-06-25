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

Invalid topics or invalid payloads are persisted in `mqtt_message_logs` with `schema_valid=false` and `validation_errors`, but they are not applied to robot domain tables.
