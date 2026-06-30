import asyncio
import json
import logging
from contextlib import suppress

import aiomqtt

from app.core.config import Settings
from app.db.base import AsyncSessionMaker
from app.mqtt.inbound import InboundMqttMessage, MqttInboundService

logger = logging.getLogger(__name__)


def build_subscription_filter(interface_name: str = "vda5050", major_version: str = "v3") -> str:
    return f"{interface_name}/{major_version}/+/+/+"


def next_reconnect_delay(current: float, maximum: float) -> float:
    return min(current * 2, maximum)


class MqttWorker:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.run(), name="tars-mqtt-worker")

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def run(self) -> None:
        subscription = build_subscription_filter(
            self.settings.mqtt_interface_name, self.settings.vda5050_major_version
        )
        delay = self.settings.mqtt_reconnect_min_seconds
        while True:
            try:
                await self._consume(subscription)
            except asyncio.CancelledError:
                raise
            except (aiomqtt.MqttError, OSError) as exc:
                logger.warning("MQTT connection failed; retrying in %.1fs: %s", delay, exc)
            await asyncio.sleep(delay)
            delay = next_reconnect_delay(delay, self.settings.mqtt_reconnect_max_seconds)

    async def _consume(self, subscription: str) -> None:
        async with aiomqtt.Client(
            hostname=self.settings.mqtt_host,
            port=self.settings.mqtt_port,
            username=self.settings.mqtt_username or None,
            password=self.settings.mqtt_password or None,
        ) as client:
            await client.subscribe(subscription)
            logger.info("Subscribed to VDA 5050 MQTT topics: %s", subscription)
            async for message in client.messages:
                try:
                    await self._handle_aiomqtt_message(message)
                except asyncio.CancelledError:
                    raise
                except Exception:
                    logger.exception("Failed to process MQTT message on %s", message.topic)

    async def _handle_aiomqtt_message(self, message: aiomqtt.Message) -> None:
        try:
            payload = json.loads(message.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            logger.warning("Dropping non-JSON MQTT payload on %s: %s", message.topic, exc)
            return

        async with AsyncSessionMaker() as session:
            service = MqttInboundService(session)
            await service.handle_message(
                InboundMqttMessage(
                    topic=str(message.topic),
                    payload=payload,
                    qos=int(message.qos),
                    retain=bool(message.retain),
                )
            )
