from tars_robot_simulator.payloads import (
    RobotIdentity,
    build_connection_payload,
    build_state_payload,
)
from tars_robot_simulator.topics import build_topic, subscription_topics


def test_build_topic_uses_vda5050_v3_shape() -> None:
    identity = RobotIdentity(manufacturer="ResearchBot", serial_number="RB-SIM-001")

    assert build_topic(identity, "state") == "vda5050/v3/ResearchBot/RB-SIM-001/state"


def test_subscription_topics_list_commands_from_fleet_control() -> None:
    identity = RobotIdentity(manufacturer="ResearchBot", serial_number="RB-SIM-001")

    assert subscription_topics(identity) == [
        "vda5050/v3/ResearchBot/RB-SIM-001/order",
        "vda5050/v3/ResearchBot/RB-SIM-001/instantActions",
    ]


def test_connection_payload_is_vda5050_v3_compatible() -> None:
    identity = RobotIdentity(manufacturer="ResearchBot", serial_number="RB-SIM-001")

    payload = build_connection_payload(identity, header_id=7, connection_state="ONLINE")

    assert payload["headerId"] == 7
    assert payload["version"] == "3.0.0"
    assert payload["manufacturer"] == "ResearchBot"
    assert payload["serialNumber"] == "RB-SIM-001"
    assert payload["connectionState"] == "ONLINE"
    assert payload["timestamp"].endswith("Z")


def test_state_payload_uses_v3_power_supply_and_safety_names() -> None:
    identity = RobotIdentity(manufacturer="ResearchBot", serial_number="RB-SIM-001")

    payload = build_state_payload(identity, header_id=8, state_of_charge=66.5)

    assert payload["powerSupply"] == {"stateOfCharge": 66.5, "charging": False}
    assert payload["safetyState"] == {"activeEmergencyStop": "NONE", "fieldViolation": False}
    assert payload["nodeStates"] == []
    assert payload["edgeStates"] == []
    assert payload["actionStates"] == []
    assert payload["instantActionStates"] == []
