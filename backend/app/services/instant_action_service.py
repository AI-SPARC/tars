from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import MqttMessageLog, Robot
from app.mqtt.outbound import MqttPublisher
from app.services.event_bus import EventBus, get_event_bus
from app.vda5050.instant_actions import build_instant_actions
from app.vda5050.topics import build_topic
from app.vda5050.validator import validate_message


@dataclass(frozen=True)
class InstantActionResult:
    accepted: bool
    topic: str
    payload: dict[str, Any]
    errors: list[str]


class InstantActionService:
    def __init__(
        self,
        session: AsyncSession,
        publisher: MqttPublisher,
        event_bus: EventBus | None = None,
    ) -> None:
        self.session = session
        self.publisher = publisher
        self.event_bus = event_bus or get_event_bus()

    async def send(
        self,
        robot_id: str,
        action_type: str,
        action_parameters: list[dict[str, Any]] | None = None,
    ) -> InstantActionResult:
        robot = await self.session.get(Robot, robot_id)
        if robot is None:
            return InstantActionResult(False, "", {}, ["Robot not found"])

        header_id = await self._next_header_id(robot.id)
        payload = build_instant_actions(
            manufacturer=robot.manufacturer,
            serial_number=robot.serial_number,
            header_id=header_id,
            action_id=str(uuid4()),
            action_type=action_type,
            action_parameters=action_parameters,
        )
        validation = validate_message("instantActions", payload)
        topic = build_topic(robot.manufacturer, robot.serial_number, "instantActions")
        log = MqttMessageLog(
            direction="outbound",
            topic=topic,
            qos=0,
            retain=False,
            robot_id=robot.id,
            message_type="instantActions",
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
                payload={
                    "topic": topic,
                    "messageType": "instantActions",
                    "errors": validation.errors,
                },
            )
            return InstantActionResult(False, topic, payload, validation.errors)

        try:
            await self.publisher.publish(topic=topic, payload=payload, qos=0, retain=False)
        except Exception:
            await self.session.commit()
            return InstantActionResult(False, topic, payload, ["MQTT publish failed"])

        await self.session.commit()
        await self.session.refresh(log)
        self.event_bus.publish(
            "mqtt.message.published",
            robot_id=robot.id,
            payload={
                "messageId": log.id,
                "topic": topic,
                "messageType": "instantActions",
            },
        )
        return InstantActionResult(True, topic, payload, [])

    async def _next_header_id(self, robot_id: str) -> int:
        logs = (
            await self.session.execute(
                select(MqttMessageLog.payload).where(
                    MqttMessageLog.robot_id == robot_id,
                    MqttMessageLog.direction == "outbound",
                    MqttMessageLog.message_type == "instantActions",
                )
            )
        ).scalars()
        header_ids = [
            value
            for payload in logs
            if isinstance((value := payload.get("headerId")), int)
        ]
        return max(header_ids, default=0) + 1
