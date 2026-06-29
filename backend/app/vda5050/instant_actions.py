from datetime import UTC, datetime
from typing import Any


def build_instant_actions(
    *,
    manufacturer: str,
    serial_number: str,
    header_id: int,
    action_id: str,
    action_type: str,
    action_parameters: list[dict[str, Any]] | None = None,
    protocol_version: str = "3.0.0",
    timestamp: datetime | None = None,
) -> dict[str, Any]:
    emitted_at = (timestamp or datetime.now(UTC)).astimezone(UTC)
    action: dict[str, Any] = {
        "actionId": action_id,
        "actionType": action_type,
        "blockingType": "NONE",
    }
    if action_parameters:
        action["actionParameters"] = action_parameters
    return {
        "headerId": header_id,
        "timestamp": emitted_at.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "version": protocol_version,
        "manufacturer": manufacturer,
        "serialNumber": serial_number,
        "actions": [action],
    }
