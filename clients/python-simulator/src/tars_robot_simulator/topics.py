from typing import Literal

from tars_robot_simulator.payloads import RobotIdentity

VdaRobotTopic = Literal[
    "connection",
    "state",
    "factsheet",
    "visualization",
    "responses",
    "order",
    "instantActions",
]


def build_topic(
    identity: RobotIdentity,
    topic: VdaRobotTopic,
    *,
    interface_name: str = "vda5050",
    major_version: str = "v3",
) -> str:
    return (
        f"{interface_name}/{major_version}/"
        f"{identity.manufacturer}/{identity.serial_number}/{topic}"
    )


def subscription_topics(identity: RobotIdentity) -> list[str]:
    return [build_topic(identity, "order"), build_topic(identity, "instantActions")]
