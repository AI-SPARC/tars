# VDA 5050 v3.0.0 Compliance Matrix

| Requirement | Source | Status | Implementation | Tests |
| --- | --- | --- | --- | --- |
| MQTT 3.1.1+ JSON transport | PDF §4 | In progress | Mosquitto + inbound worker + outbound publisher | Unit tests; broker E2E pending |
| Topic structure `vda5050/v3/{manufacturer}/{serialNumber}/{topic}` | PDF §4.2 | Implemented | `app.vda5050.topics` | `test_topics.py` |
| QoS 0 for order/instantActions/state/factsheet/zoneSet/responses/visualization | PDF §4.1 | Partial | Order and instantActions publishers plus wildcard inbound subscription | Dispatch/action/inbound tests; remaining publishers pending |
| QoS 1 for connection | PDF §4.1 | Partial | Inbound worker preserves received QoS; simulator publishes connection at QoS 1 | Broker E2E pending |
| JSON Schema validation for all v3.0.0 schemas | GitHub tag 3.0.0 | Implemented | `app.vda5050.validator` | `test_validator.py` |
| Order graph constraints | PDF §6.1 | Implemented for new MVP orders | Graph route + `app.vda5050.order_builder` | Builder and mission dispatch tests |
| Incremental order `headerId` per robot/topic | PDF §5 | Implemented for `order` | Persisted `mission_orders` history | Mission dispatch tests |
| `cancelOrder` instant action | PDF §7 | Implemented | Robot instant-actions API, MQTT publisher, and simulator | Service, API, and simulator tests |
| State/factsheet/connection ingestion | PDF §6–8 | Implemented | MQTT inbound service + robot registry | Inbound service tests; broker E2E pending |
