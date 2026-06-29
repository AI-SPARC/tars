from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import MqttMessageLog
from app.services.event_bus import EventBus, get_event_bus
from app.services.robot_registry import RobotRegistryService
from app.vda5050.topics import TopicParseError, parse_topic
from app.vda5050.validator import validate_message


@dataclass(frozen=True)
class InboundMqttMessage:
    topic: str
    payload: dict[str, Any]
    qos: int = 0
    retain: bool = False


@dataclass(frozen=True)
class MqttInboundResult:
    accepted: bool
    message_type: str
    robot_id: str | None
    errors: list[str]


class MqttInboundService:
    def __init__(self, session: AsyncSession, event_bus: EventBus | None = None) -> None:
        self.session = session
        self.event_bus = event_bus or get_event_bus()
        self.robot_registry = RobotRegistryService(session, self.event_bus)

    async def handle_message(self, message: InboundMqttMessage) -> MqttInboundResult:
        try:
            parsed_topic = parse_topic(message.topic)
        except TopicParseError as exc:
            errors = [str(exc)]
            await self._log_message(
                message=message,
                message_type="unknown",
                robot_id=None,
                schema_valid=False,
                validation_errors=errors,
            )
            return MqttInboundResult(False, "unknown", None, errors)

        validation = validate_message(parsed_topic.topic, message.payload)
        if not validation.valid:
            await self._log_message(
                message=message,
                message_type=parsed_topic.topic,
                robot_id=None,
                schema_valid=False,
                validation_errors=validation.errors,
            )
            return MqttInboundResult(False, parsed_topic.topic, None, validation.errors)

        robot = await self.robot_registry.get_or_create(
            parsed_topic.manufacturer, parsed_topic.serial_number
        )
        if parsed_topic.topic == "connection":
            robot = await self.robot_registry.update_connection_state(
                robot.id, message.payload["connectionState"]
            )
        elif parsed_topic.topic == "factsheet":
            robot = await self.robot_registry.update_factsheet(robot.id, message.payload)
        elif parsed_topic.topic == "state":
            await self.robot_registry.save_state_snapshot(robot.id, message.payload)

        await self._log_message(
            message=message,
            message_type=parsed_topic.topic,
            robot_id=robot.id,
            schema_valid=True,
            validation_errors=[],
        )
        return MqttInboundResult(True, parsed_topic.topic, robot.id, [])

    async def _log_message(
        self,
        *,
        message: InboundMqttMessage,
        message_type: str,
        robot_id: str | None,
        schema_valid: bool,
        validation_errors: list[str],
    ) -> MqttMessageLog:
        log = MqttMessageLog(
            direction="inbound",
            topic=message.topic,
            qos=message.qos,
            retain=message.retain,
            robot_id=robot_id,
            message_type=message_type,
            payload=message.payload,
            schema_valid=schema_valid,
            validation_errors=validation_errors,
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        self.event_bus.publish(
            "mqtt.message.received",
            robot_id=robot_id,
            payload={
                "messageId": log.id,
                "topic": log.topic,
                "messageType": log.message_type,
                "schemaValid": log.schema_valid,
            },
        )
        if not schema_valid:
            self.event_bus.publish(
                "vda.validation.failed",
                robot_id=robot_id,
                payload={
                    "messageId": log.id,
                    "topic": log.topic,
                    "messageType": log.message_type,
                    "errors": validation_errors,
                },
            )
        return log
