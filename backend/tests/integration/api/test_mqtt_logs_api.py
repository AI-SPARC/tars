from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.deps import get_session
from app.db.base import Base, MqttMessageLog, Robot
from app.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_session():
        async with maker() as session:
            yield session

    async with maker() as session:
        robot = Robot(id="robot-logs", manufacturer="ResearchBot", serial_number="RB-LOGS")
        now = datetime.now(UTC)
        session.add(robot)
        session.add_all(
            [
                MqttMessageLog(
                    id="log-connection",
                    direction="inbound",
                    topic="vda5050/v3/ResearchBot/RB-LOGS/connection",
                    qos=1,
                    retain=True,
                    robot_id=robot.id,
                    message_type="connection",
                    payload={"connectionState": "ONLINE"},
                    schema_valid=True,
                    validation_errors=[],
                    created_at=now - timedelta(seconds=2),
                ),
                MqttMessageLog(
                    id="log-invalid-state",
                    direction="inbound",
                    topic="vda5050/v3/ResearchBot/RB-LOGS/state",
                    robot_id=robot.id,
                    message_type="state",
                    payload={"headerId": 1},
                    schema_valid=False,
                    validation_errors=["timestamp is required"],
                    created_at=now - timedelta(seconds=1),
                ),
                MqttMessageLog(
                    id="log-order",
                    direction="outbound",
                    topic="vda5050/v3/ResearchBot/RB-LOGS/order",
                    robot_id=robot.id,
                    message_type="order",
                    payload={"orderId": "mission-1"},
                    schema_valid=True,
                    validation_errors=[],
                    created_at=now,
                ),
            ]
        )
        await session.commit()

    app.dependency_overrides[get_session] = override_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as value:
        yield value
    app.dependency_overrides.clear()
    await engine.dispose()


async def test_list_mqtt_messages_is_newest_first_and_paginated(client: AsyncClient) -> None:
    first_page = await client.get("/api/v1/mqtt/messages", params={"pageSize": 2})

    assert first_page.status_code == 200
    assert first_page.json() == {
        "items": [
            {
                "id": "log-order",
                "direction": "outbound",
                "topic": "vda5050/v3/ResearchBot/RB-LOGS/order",
                "qos": 0,
                "retain": False,
                "robotId": "robot-logs",
                "messageType": "order",
                "payload": {"orderId": "mission-1"},
                "schemaValid": True,
                "validationErrors": [],
                "createdAt": first_page.json()["items"][0]["createdAt"],
            },
            {
                "id": "log-invalid-state",
                "direction": "inbound",
                "topic": "vda5050/v3/ResearchBot/RB-LOGS/state",
                "qos": 0,
                "retain": False,
                "robotId": "robot-logs",
                "messageType": "state",
                "payload": {"headerId": 1},
                "schemaValid": False,
                "validationErrors": ["timestamp is required"],
                "createdAt": first_page.json()["items"][1]["createdAt"],
            },
        ],
        "page": 1,
        "pageSize": 2,
        "total": 3,
        "pages": 2,
    }

    second_page = await client.get("/api/v1/mqtt/messages", params={"page": 2, "pageSize": 2})
    assert [item["id"] for item in second_page.json()["items"]] == ["log-connection"]


async def test_filter_mqtt_messages_by_protocol_metadata(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/mqtt/messages",
        params={
            "direction": "inbound",
            "messageType": "state",
            "robotId": "robot-logs",
            "schemaValid": "false",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == "log-invalid-state"
    assert body["items"][0]["validationErrors"] == ["timestamp is required"]


async def test_reject_invalid_log_query_parameters(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/mqtt/messages", params={"direction": "sideways", "pageSize": 101}
    )

    assert response.status_code == 422
