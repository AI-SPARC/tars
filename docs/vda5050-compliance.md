# VDA 5050 v3.0.0 Compliance Matrix

| Requirement | Source | Status | Implementation | Tests |
| --- | --- | --- | --- | --- |
| MQTT 3.1.1+ JSON transport | PDF §4 | Planned | Mosquitto + backend MQTT adapter | Integration MQTT tests |
| Topic structure `vda5050/v3/{manufacturer}/{serialNumber}/{topic}` | PDF §4.2 | In progress | `app.vda5050.topics` | `test_topics.py` |
| QoS 0 for order/instantActions/state/factsheet/zoneSet/responses/visualization | PDF §4.1 | Planned | MQTT publisher/subscriber config | MQTT tests |
| QoS 1 for connection | PDF §4.1 | Planned | MQTT subscriber config | MQTT tests |
| JSON Schema validation for all v3.0.0 schemas | GitHub tag 3.0.0 | In progress | `app.vda5050.validator` | `test_validator.py` |
| Order graph constraints | PDF §6.1 | In progress | `app.vda5050.order_builder` | `test_order_builder.py` |
