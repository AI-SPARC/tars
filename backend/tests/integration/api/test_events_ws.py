from fastapi.testclient import TestClient

from app.main import app
from app.services.event_bus import EventBus, get_event_bus


def test_websocket_streams_domain_events_and_removes_disconnected_clients() -> None:
    event_bus = EventBus()
    app.dependency_overrides[get_event_bus] = lambda: event_bus

    try:
        with TestClient(app) as client:
            with client.websocket_connect("/api/v1/events/ws") as websocket:
                event_bus.publish(
                    "mission.created",
                    mission_id="mission-1",
                    payload={"status": "assigned"},
                )
                message = websocket.receive_json()

                assert message["type"] == "mission.created"
                assert message["missionId"] == "mission-1"
                assert message["payload"] == {"status": "assigned"}
                assert message["id"]
                assert message["timestamp"]
                assert event_bus.subscriber_count == 1

            assert event_bus.subscriber_count == 0
    finally:
        app.dependency_overrides.clear()
