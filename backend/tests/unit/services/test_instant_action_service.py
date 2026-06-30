from collections.abc import AsyncIterator

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base, MqttMessageLog, Robot
from app.mqtt.outbound import RecordingMqttPublisher
from app.services.instant_action_service import InstantActionService
from app.vda5050.validator import validate_message


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as value:
        yield value
    await engine.dispose()


async def test_send_cancel_order_publishes_valid_incremental_instant_actions(
    session: AsyncSession,
) -> None:
    robot = Robot(id="robot-actions", manufacturer="ResearchBot", serial_number="RB-ACTIONS")
    session.add(robot)
    await session.commit()
    publisher = RecordingMqttPublisher()
    service = InstantActionService(session, publisher)

    first = await service.send(robot.id, "cancelOrder")
    second = await service.send(robot.id, "cancelOrder")

    assert first.accepted is True
    assert second.accepted is True
    assert first.topic == "vda5050/v3/ResearchBot/RB-ACTIONS/instantActions"
    assert first.payload["headerId"] == 1
    assert second.payload["headerId"] == 2
    assert first.payload["actions"][0]["actionType"] == "cancelOrder"
    assert validate_message("instantActions", first.payload).valid is True
    assert len(publisher.publications) == 2
    logs = (await session.execute(select(MqttMessageLog))).scalars().all()
    assert [log.message_type for log in logs] == ["instantActions", "instantActions"]


async def test_send_instant_action_rejects_unknown_robot(session: AsyncSession) -> None:
    result = await InstantActionService(session, RecordingMqttPublisher()).send(
        "missing", "cancelOrder"
    )

    assert result.accepted is False
    assert result.errors == ["Robot not found"]
