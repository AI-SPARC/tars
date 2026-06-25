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
