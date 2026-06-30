from collections.abc import AsyncIterator

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import (
    Base,
    MapEdge,
    MapLayout,
    MapNode,
    Mission,
    MissionOrder,
    MqttMessageLog,
    Robot,
)
from app.mqtt.outbound import RecordedPublish, RecordingMqttPublisher
from app.services.event_bus import EventBus
from app.services.mission_dispatch import MissionDispatchService


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as db_session:
        yield db_session
    await engine.dispose()


async def test_dispatch_mission_publishes_order_and_logs_outbound(
    session: AsyncSession,
) -> None:
    robot = Robot(
        id="robot-dispatch-001",
        manufacturer="ResearchBot",
        serial_number="RB-DISPATCH-001",
    )
    layout = MapLayout(id="map-dispatch-001", name="Research lab")
    nodes = [
        MapNode(map_id=layout.id, node_key="A", x=0.0, y=0.0, theta=0.0),
        MapNode(map_id=layout.id, node_key="C", x=1.0, y=1.0, theta=0.5),
        MapNode(map_id=layout.id, node_key="B", x=2.0, y=0.0, theta=1.0),
    ]
    edges = [
        MapEdge(
            map_id=layout.id,
            edge_key="A-C",
            from_node_key="A",
            to_node_key="C",
            distance=1.0,
        ),
        MapEdge(
            map_id=layout.id,
            edge_key="C-B",
            from_node_key="C",
            to_node_key="B",
            distance=1.0,
        ),
        MapEdge(
            map_id=layout.id,
            edge_key="A-B-slow",
            from_node_key="A",
            to_node_key="B",
            distance=5.0,
        ),
    ]
    mission = Mission(
        map_id=layout.id,
        assigned_robot_id="robot-dispatch-001",
        start_node_key="A",
        goal_node_key="B",
        priority=5,
        status="assigned",
    )
    session.add_all([robot, layout, *nodes, *edges, mission])
    await session.commit()
    publisher = RecordingMqttPublisher()
    event_bus = EventBus()

    async with event_bus.subscribe() as events:
        result = await MissionDispatchService(session, publisher, event_bus).dispatch_mission(
            mission.id
        )
        emitted_types = [(await events.get()).type for _ in range(3)]

    assert result.accepted is True
    assert result.topic == "vda5050/v3/ResearchBot/RB-DISPATCH-001/order"
    assert result.payload["orderId"] == mission.id
    assert result.payload["nodes"][0]["nodeId"] == "A"
    assert [node["nodeId"] for node in result.payload["nodes"]] == ["A", "C", "B"]
    assert [edge["edgeId"] for edge in result.payload["edges"]] == ["A-C", "C-B"]
    assert result.payload["nodes"][1]["nodePosition"] == {
        "x": 1.0,
        "y": 1.0,
        "theta": 0.5,
        "allowedDeviationXY": {"a": 0.1, "b": 0.1, "theta": 0.0},
        "allowedDeviationTheta": 0.1,
        "mapId": layout.id,
    }
    assert publisher.publications == [
        RecordedPublish(topic=result.topic, payload=result.payload, qos=0, retain=False)
    ]

    log = (await session.execute(select(MqttMessageLog))).scalar_one()
    mission_order = (await session.execute(select(MissionOrder))).scalar_one()
    await session.refresh(mission)
    assert log.direction == "outbound"
    assert log.message_type == "order"
    assert log.schema_valid is True
    assert log.robot_id == robot.id
    assert mission.status == "sent"
    assert mission_order.header_id == 1
    assert mission_order.payload == result.payload
    assert mission_order.validation_status == "valid"
    assert mission_order.published_at is not None
    assert emitted_types == [
        "mqtt.message.published",
        "mission.dispatched",
        "mission.status.changed",
    ]


async def test_dispatch_mission_rejects_unassigned_mission(session: AsyncSession) -> None:
    mission = Mission(start_node_key="A", goal_node_key="B")
    session.add(mission)
    await session.commit()

    service = MissionDispatchService(session, RecordingMqttPublisher())

    result = await service.dispatch_mission(mission.id)

    assert result.accepted is False
    assert result.errors == ["Mission has no assigned robot"]


async def test_dispatch_mission_increments_order_header_per_robot(session: AsyncSession) -> None:
    robot = Robot(id="robot-headers", manufacturer="ResearchBot", serial_number="RB-HEADERS")
    layout = MapLayout(id="map-headers", name="Header test map")
    session.add_all(
        [
            robot,
            layout,
            MapNode(map_id=layout.id, node_key="A", x=0, y=0),
            MapNode(map_id=layout.id, node_key="B", x=1, y=0),
            MapEdge(
                map_id=layout.id,
                edge_key="A-B",
                from_node_key="A",
                to_node_key="B",
                distance=1,
            ),
        ]
    )
    await session.commit()
    publisher = RecordingMqttPublisher()
    service = MissionDispatchService(session, publisher)

    header_ids = []
    for _ in range(2):
        mission = Mission(
            map_id=layout.id,
            assigned_robot_id=robot.id,
            start_node_key="A",
            goal_node_key="B",
            status="assigned",
        )
        session.add(mission)
        await session.commit()
        result = await service.dispatch_mission(mission.id)
        header_ids.append(result.payload["headerId"])

    assert header_ids == [1, 2]


async def test_dispatch_mission_rejects_when_route_does_not_exist(
    session: AsyncSession,
) -> None:
    robot = Robot(id="robot-no-route", manufacturer="ResearchBot", serial_number="RB-NO-ROUTE")
    layout = MapLayout(id="map-no-route", name="Disconnected map")
    mission = Mission(
        map_id=layout.id,
        assigned_robot_id=robot.id,
        start_node_key="A",
        goal_node_key="B",
        status="assigned",
    )
    session.add_all(
        [
            robot,
            layout,
            MapNode(map_id=layout.id, node_key="A", x=0, y=0),
            MapNode(map_id=layout.id, node_key="B", x=1, y=0),
            mission,
        ]
    )
    await session.commit()

    result = await MissionDispatchService(
        session, RecordingMqttPublisher()
    ).dispatch_mission(mission.id)

    assert result.accepted is False
    assert result.errors == ["No route found"]
    assert (await session.execute(select(MissionOrder))).scalars().all() == []
