import asyncio

import aiomqtt
import pytest

from app.core.config import Settings
from app.mqtt.worker import MqttWorker, build_subscription_filter, next_reconnect_delay


def test_build_subscription_filter_targets_vda5050_v3_topics() -> None:
    assert build_subscription_filter() == "vda5050/v3/+/+/+"


def test_build_subscription_filter_uses_custom_interface_and_version() -> None:
    assert build_subscription_filter("custom", "v9") == "custom/v9/+/+/+"


def test_reconnect_delay_uses_bounded_exponential_backoff() -> None:
    assert next_reconnect_delay(1, 30) == 2
    assert next_reconnect_delay(16, 30) == 30
    assert next_reconnect_delay(30, 30) == 30


async def test_worker_retries_after_mqtt_connection_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worker = MqttWorker(
        Settings(mqtt_reconnect_min_seconds=0.25, mqtt_reconnect_max_seconds=1.0)
    )
    attempts = 0
    sleeps: list[float] = []

    async def consume(subscription: str) -> None:
        nonlocal attempts
        assert subscription == "vda5050/v3/+/+/+"
        attempts += 1
        if attempts == 1:
            raise aiomqtt.MqttError("broker unavailable")
        raise asyncio.CancelledError

    async def record_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(worker, "_consume", consume)
    monkeypatch.setattr(asyncio, "sleep", record_sleep)

    with pytest.raises(asyncio.CancelledError):
        await worker.run()

    assert attempts == 2
    assert sleeps == [0.25]
