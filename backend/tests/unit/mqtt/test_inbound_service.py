import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base, MqttMessageLog, Robot, RobotStateSnapshot
from app.mqtt.inbound import InboundMqttMessage, MqttInboundService


@pytest.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as db_session:
        yield db_session
    await engine.dispose()


def connection_payload(state: str = "ONLINE") -> dict:
    return {
        "headerId": 1,
        "timestamp": "2026-06-25T13:00:00.000Z",
        "version": "3.0.0",
        "manufacturer": "ResearchBot",
        "serialNumber": "RB100",
        "connectionState": state,
    }


def state_payload() -> dict:
    return {
        "headerId": 2,
        "timestamp": "2026-06-25T13:00:01.000Z",
        "version": "3.0.0",
        "manufacturer": "ResearchBot",
        "serialNumber": "RB100",
        "orderId": "order-1",
        "orderUpdateId": 0,
        "lastNodeId": "A",
        "lastNodeSequenceId": 0,
        "nodeStates": [],
        "edgeStates": [],
        "driving": False,
        "actionStates": [],
        "instantActionStates": [],
        "powerSupply": {"stateOfCharge": 76.5, "charging": False},
        "operatingMode": "AUTOMATIC",
        "errors": [],
        "safetyState": {"activeEmergencyStop": "NONE", "fieldViolation": False},
    }


async def test_connection_message_creates_robot_updates_state_and_logs_message(
    session: AsyncSession,
) -> None:
    service = MqttInboundService(session)

    result = await service.handle_message(
        InboundMqttMessage(
            topic="vda5050/v3/ResearchBot/RB100/connection",
            payload=connection_payload(),
            qos=1,
            retain=True,
        )
    )

    robot = (await session.execute(select(Robot))).scalar_one()
    log = (await session.execute(select(MqttMessageLog))).scalar_one()
    assert result.accepted is True
    assert result.robot_id == robot.id
    assert robot.last_connection_state == "ONLINE"
    assert log.robot_id == robot.id
    assert log.direction == "inbound"
    assert log.message_type == "connection"
    assert log.schema_valid is True
    assert log.validation_errors == []
    assert log.qos == 1


async def test_state_message_persists_latest_snapshot_and_soc(session: AsyncSession) -> None:
    service = MqttInboundService(session)

    await service.handle_message(
        InboundMqttMessage(topic="vda5050/v3/ResearchBot/RB100/state", payload=state_payload())
    )

    robot = (await session.execute(select(Robot))).scalar_one()
    snapshot = (await session.execute(select(RobotStateSnapshot))).scalar_one()
    assert snapshot.robot_id == robot.id
    assert snapshot.order_id == "order-1"
    assert snapshot.battery_charge == 76.5
    assert snapshot.raw_payload["powerSupply"]["stateOfCharge"] == 76.5


async def test_invalid_vda_payload_is_logged_but_not_applied(session: AsyncSession) -> None:
    service = MqttInboundService(session)

    result = await service.handle_message(
        InboundMqttMessage(
            topic="vda5050/v3/ResearchBot/RB100/connection",
            payload={"headerId": 1},
            qos=1,
        )
    )

    robots = (await session.execute(select(Robot))).scalars().all()
    log = (await session.execute(select(MqttMessageLog))).scalar_one()
    assert result.accepted is False
    assert result.errors
    assert robots == []
    assert log.schema_valid is False
    assert log.validation_errors


async def test_invalid_topic_is_logged_without_robot(session: AsyncSession) -> None:
    service = MqttInboundService(session)

    result = await service.handle_message(
        InboundMqttMessage(topic="invalid/topic", payload={"headerId": 1}, qos=0)
    )

    log = (await session.execute(select(MqttMessageLog))).scalar_one()
    assert result.accepted is False
    assert log.topic == "invalid/topic"
    assert log.message_type == "unknown"
    assert log.robot_id is None
    assert log.validation_errors
