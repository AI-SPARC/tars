from dataclasses import dataclass
from typing import Literal

VdaTopicName = Literal[
    "order",
    "instantActions",
    "state",
    "visualization",
    "connection",
    "factsheet",
    "zoneSet",
    "responses",
]

VALID_TOPICS: set[str] = {
    "order",
    "instantActions",
    "state",
    "visualization",
    "connection",
    "factsheet",
    "zoneSet",
    "responses",
}

FORBIDDEN_IDENTITY_CHARS = {"/", "+", "#", "$"}


class TopicParseError(ValueError):
    """Raised when an MQTT topic is not a valid VDA 5050 v3 topic."""


@dataclass(frozen=True)
class ParsedTopic:
    interface_name: str
    major_version: str
    manufacturer: str
    serial_number: str
    topic: str


def parse_topic(
    topic: str,
    *,
    expected_interface: str = "vda5050",
    expected_major_version: str = "v3",
) -> ParsedTopic:
    parts = topic.split("/")
    if len(parts) != 5:
        raise TopicParseError(
            "VDA 5050 topic must have 5 levels: "
            "interfaceName/majorVersion/manufacturer/serialNumber/topic"
        )

    interface_name, major_version, manufacturer, serial_number, topic_name = parts
    if interface_name != expected_interface:
        raise TopicParseError(f"Unsupported VDA 5050 interface name: {interface_name}")
    if major_version != expected_major_version:
        raise TopicParseError(f"Unsupported VDA 5050 major version: {major_version}")
    for field_name, value in {"manufacturer": manufacturer, "serialNumber": serial_number}.items():
        if not value or any(char in value for char in FORBIDDEN_IDENTITY_CHARS):
            raise TopicParseError(f"Invalid {field_name} in VDA 5050 topic: {value}")
    if topic_name not in VALID_TOPICS:
        raise TopicParseError(f"Unsupported VDA 5050 topic name: {topic_name}")

    return ParsedTopic(
        interface_name=interface_name,
        major_version=major_version,
        manufacturer=manufacturer,
        serial_number=serial_number,
        topic=topic_name,
    )


def build_topic(
    manufacturer: str,
    serial_number: str,
    topic: VdaTopicName,
    *,
    interface_name: str = "vda5050",
    major_version: str = "v3",
) -> str:
    parsed = parse_topic(f"{interface_name}/{major_version}/{manufacturer}/{serial_number}/{topic}")
    return "/".join(
        [
            parsed.interface_name,
            parsed.major_version,
            parsed.manufacturer,
            parsed.serial_number,
            parsed.topic,
        ]
    )
