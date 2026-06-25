import pytest

from app.vda5050.topics import TopicParseError, parse_topic


def test_parse_valid_vda5050_topic() -> None:
    parsed = parse_topic("vda5050/v3/KIT/0001/state")

    assert parsed.interface_name == "vda5050"
    assert parsed.major_version == "v3"
    assert parsed.manufacturer == "KIT"
    assert parsed.serial_number == "0001"
    assert parsed.topic == "state"


@pytest.mark.parametrize(
    "topic",
    [
        "vda5050/v3/KIT/0001",
        "vda5050/v2/KIT/0001/state",
        "uagv/v3/KIT/0001/state",
        "vda5050/v3/KI/T/0001/state",
        "vda5050/v3/KIT/00+1/state",
        "vda5050/v3/KIT/0001/unknown",
    ],
)
def test_reject_invalid_vda5050_topic(topic: str) -> None:
    with pytest.raises(TopicParseError):
        parse_topic(topic)
