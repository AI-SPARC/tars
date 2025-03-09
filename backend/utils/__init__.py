def generate_topics():
    """Gera a lista de tópicos MQTT com base nos AGVs registrados."""
    topics = []
    for agv in AGVS:
        base_topic = f"vda5050/{agv['manufacturer']}/{agv['agvId']}"
        topics.extend([
            f"{base_topic}/factsheet",
            f"{base_topic}/order",
            f"{base_topic}/state"
        ])
    return topics