import asyncio
import json
from dataclasses import dataclass
from typing import Any, Protocol

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from app.core.config import Settings, get_settings


@dataclass(frozen=True)
class RecordedPublish:
    topic: str
    payload: dict[str, Any]
    qos: int = 0
    retain: bool = False


class MqttPublisher(Protocol):
    async def publish(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        qos: int = 0,
        retain: bool = False,
    ) -> None: ...


class RecordingMqttPublisher:
    def __init__(self) -> None:
        self.publications: list[RecordedPublish] = []

    async def publish(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        qos: int = 0,
        retain: bool = False,
    ) -> None:
        self.publications.append(RecordedPublish(topic, payload, qos, retain))


class PahoMqttPublisher:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    async def publish(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        qos: int = 0,
        retain: bool = False,
    ) -> None:
        await asyncio.to_thread(
            self._publish_sync,
            topic=topic,
            payload=payload,
            qos=qos,
            retain=retain,
        )

    def _publish_sync(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        qos: int,
        retain: bool,
    ) -> None:
        encoded = json.dumps(payload, separators=(",", ":"))
        client = mqtt.Client(CallbackAPIVersion.VERSION2)
        client.connect(self.settings.mqtt_host, self.settings.mqtt_port, keepalive=30)
        result = client.publish(topic, payload=encoded, qos=qos, retain=retain)
        result.wait_for_publish()
        client.disconnect()


def get_mqtt_publisher() -> MqttPublisher:
    return PahoMqttPublisher()
