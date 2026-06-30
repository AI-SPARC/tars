# VDA 5050 v3.0.0 Compliance Matrix

| Requirement | Source | Status | Implementation | Tests |
| --- | --- | --- | --- | --- |
| MQTT 3.1.1+ JSON transport | PDF §4 | Implemented for MVP flows | Mosquitto + inbound worker + outbound publisher | Unit tests + Docker broker E2E |
| Topic structure `vda5050/v3/{manufacturer}/{serialNumber}/{topic}` | PDF §4.2 | Implemented | `app.vda5050.topics` | `test_topics.py` |
| QoS 0 for order/instantActions/state/factsheet/zoneSet/responses/visualization | PDF §4.1 | Partial | Order and instantActions publishers plus wildcard inbound subscription | Dispatch/action/inbound tests; remaining publishers pending |
| QoS 1 for connection | PDF §4.1 | Implemented | Inbound worker preserves received QoS; simulator publishes connection at QoS 1 | Unit tests + Docker broker E2E |
| JSON Schema validation for all v3.0.0 schemas | GitHub tag 3.0.0 | Implemented | `app.vda5050.validator` | `test_validator.py` |
| Order graph constraints | PDF §6.1 | Implemented for new MVP orders | Graph route + `app.vda5050.order_builder` | Builder and mission dispatch tests |
| Incremental order `headerId` per robot/topic | PDF §5 | Implemented for `order` | Persisted `mission_orders` history | Mission dispatch tests |
| Required VDA header fields | PDF §5 | Implemented for emitted MVP messages | Order and instantActions builders | JSON Schema tests + broker E2E |
| Order update constraints | PDF §6.1 | Partial | New orders always use `orderUpdateId=0`; updates are not exposed yet | Order builder tests |
| `cancelOrder` instant action | PDF §7 | Implemented | Robot instant-actions API, MQTT publisher, and simulator | Service, API, and simulator tests |
| State/factsheet/connection ingestion | PDF §6–8 | Implemented | MQTT inbound service + robot registry | Inbound service tests + Docker broker E2E |
| Visualization ingestion | PDF §8 | Partial | Payload validation and MQTT log persistence | Domain position update pending |
