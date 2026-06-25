from app.vda5050.validator import validate_message


def test_valid_connection_message_passes_schema_validation() -> None:
    payload = {
        "headerId": 1,
        "timestamp": "2026-06-25T13:00:00.00Z",
        "version": "3.0.0",
        "manufacturer": "ResearchBot",
        "serialNumber": "RB001",
        "connectionState": "ONLINE",
    }

    result = validate_message("connection", payload)

    assert result.valid is True
    assert result.errors == []


def test_missing_required_header_field_fails_schema_validation() -> None:
    payload = {
        "timestamp": "2026-06-25T13:00:00.00Z",
        "version": "3.0.0",
        "manufacturer": "ResearchBot",
        "serialNumber": "RB001",
        "connectionState": "ONLINE",
    }

    result = validate_message("connection", payload)

    assert result.valid is False
    assert any("headerId" in error for error in result.errors)


def test_unknown_message_type_fails_without_exception() -> None:
    result = validate_message("not-a-vda-topic", {})

    assert result.valid is False
    assert result.errors == ["Unsupported VDA 5050 message type: not-a-vda-topic"]
