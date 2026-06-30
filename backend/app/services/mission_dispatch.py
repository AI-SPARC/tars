from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Mission, MissionOrder, MqttMessageLog, Robot
from app.mqtt.outbound import MqttPublisher
from app.services.event_bus import EventBus, get_event_bus
from app.services.map_service import MapService
from app.vda5050.order_builder import RouteEdge, RouteNode, build_order
from app.vda5050.topics import build_topic
from app.vda5050.validator import validate_message


@dataclass(frozen=True)
class MissionDispatchResult:
    accepted: bool
    topic: str
    payload: dict[str, Any]
    errors: list[str]


class MissionDispatchService:
    def __init__(
        self,
        session: AsyncSession,
        publisher: MqttPublisher,
        event_bus: EventBus | None = None,
    ) -> None:
        self.session = session
        self.publisher = publisher
        self.event_bus = event_bus or get_event_bus()

    async def dispatch_mission(self, mission_id: str) -> MissionDispatchResult:
        mission = await self.session.get(Mission, mission_id)
        if mission is None:
            return MissionDispatchResult(False, "", {}, ["Mission not found"])
        if mission.assigned_robot_id is None:
            return MissionDispatchResult(False, "", {}, ["Mission has no assigned robot"])
        if mission.status != "assigned":
            return MissionDispatchResult(
                False, "", {}, [f"Mission cannot be dispatched from status '{mission.status}'"]
            )
        if mission.map_id is None:
            return MissionDispatchResult(False, "", {}, ["Mission has no map"])

        robot = await self.session.get(Robot, mission.assigned_robot_id)
        if robot is None:
            return MissionDispatchResult(False, "", {}, ["Assigned robot not found"])

        try:
            planned_route = await MapService(self.session).plan_route(
                mission.map_id, mission.start_node_key, mission.goal_node_key
            )
        except ValueError as exc:
            return MissionDispatchResult(False, "", {}, [str(exc)])

        latest_header_id = await self.session.scalar(
            select(func.max(MissionOrder.header_id)).where(MissionOrder.robot_id == robot.id)
        )
        header_id = (latest_header_id or 0) + 1
        payload = build_order(
            manufacturer=robot.manufacturer,
            serial_number=robot.serial_number,
            header_id=header_id,
            order_id=mission.id,
            nodes=[
                RouteNode(
                    node_id=node.node_key,
                    x=node.x,
                    y=node.y,
                    theta=node.theta,
                    map_id=mission.map_id,
                )
                for node in planned_route.nodes
            ],
            edges=[
                RouteEdge(
                    edge_id=leg.edge_key,
                    start_node_id=leg.from_node_key,
                    end_node_id=leg.to_node_key,
                )
                for leg in planned_route.legs
            ],
        )
        validation = validate_message("order", payload)
        topic = build_topic(robot.manufacturer, robot.serial_number, "order")
        mission_order = MissionOrder(
            mission_id=mission.id,
            robot_id=robot.id,
            order_id=mission.id,
            order_update_id=0,
            header_id=header_id,
            payload=payload,
            validation_status="valid" if validation.valid else "invalid",
        )
        self.session.add(mission_order)
        log = MqttMessageLog(
            direction="outbound",
            topic=topic,
            qos=0,
            retain=False,
            robot_id=robot.id,
            message_type="order",
            payload=payload,
            schema_valid=validation.valid,
            validation_errors=validation.errors,
        )
        self.session.add(log)
        if not validation.valid:
            await self.session.commit()
            self.event_bus.publish(
                "vda.validation.failed",
                robot_id=robot.id,
                mission_id=mission.id,
                payload={"topic": topic, "messageType": "order", "errors": validation.errors},
            )
            return MissionDispatchResult(False, topic, payload, validation.errors)

        try:
            await self.publisher.publish(topic=topic, payload=payload, qos=0, retain=False)
        except Exception:
            mission_order.validation_status = "publish_failed"
            await self.session.commit()
            return MissionDispatchResult(False, topic, payload, ["MQTT publish failed"])
        mission_order.published_at = datetime.now(UTC)
        mission.status = "sent"
        await self.session.commit()
        self.event_bus.publish(
            "mqtt.message.published",
            robot_id=robot.id,
            mission_id=mission.id,
            payload={"messageId": log.id, "topic": topic, "messageType": "order"},
        )
        self.event_bus.publish(
            "mission.dispatched",
            robot_id=robot.id,
            mission_id=mission.id,
            payload={"status": mission.status, "orderId": mission.id},
        )
        self.event_bus.publish(
            "mission.status.changed",
            robot_id=robot.id,
            mission_id=mission.id,
            payload={"status": mission.status},
        )
        return MissionDispatchResult(True, topic, payload, [])

    async def list_outbound_order_logs(self) -> list[MqttMessageLog]:
        result = await self.session.execute(
            select(MqttMessageLog).where(
                MqttMessageLog.direction == "outbound",
                MqttMessageLog.message_type == "order",
            )
        )
        return list(result.scalars())
