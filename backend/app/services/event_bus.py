import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class DomainEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    robot_id: str | None = Field(default=None, serialization_alias="robotId")
    mission_id: str | None = Field(default=None, serialization_alias="missionId")
    payload: dict[str, Any] = Field(default_factory=dict)

    def as_message(self) -> dict[str, Any]:
        return self.model_dump(mode="json", by_alias=True, exclude_none=True)


class EventBus:
    def __init__(self, *, subscriber_buffer_size: int = 100) -> None:
        if subscriber_buffer_size < 1:
            raise ValueError("subscriber_buffer_size must be positive")
        self.subscriber_buffer_size = subscriber_buffer_size
        self._subscribers: dict[
            asyncio.Queue[DomainEvent], asyncio.AbstractEventLoop
        ] = {}

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)

    @asynccontextmanager
    async def subscribe(self) -> AsyncIterator[asyncio.Queue[DomainEvent]]:
        queue: asyncio.Queue[DomainEvent] = asyncio.Queue(
            maxsize=self.subscriber_buffer_size
        )
        self._subscribers[queue] = asyncio.get_running_loop()
        try:
            yield queue
        finally:
            self._subscribers.pop(queue, None)

    def publish(
        self,
        event_type: str,
        *,
        robot_id: str | None = None,
        mission_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> DomainEvent:
        event = DomainEvent(
            type=event_type,
            robot_id=robot_id,
            mission_id=mission_id,
            payload=payload or {},
        )
        try:
            current_loop = asyncio.get_running_loop()
        except RuntimeError:
            current_loop = None
        for queue, subscriber_loop in tuple(self._subscribers.items()):
            if subscriber_loop is current_loop:
                self._enqueue(queue, event)
            elif subscriber_loop.is_running():
                subscriber_loop.call_soon_threadsafe(self._enqueue, queue, event)
        return event

    @staticmethod
    def _enqueue(queue: asyncio.Queue[DomainEvent], event: DomainEvent) -> None:
        if queue.full():
            queue.get_nowait()
        queue.put_nowait(event)


event_bus = EventBus()


def get_event_bus() -> EventBus:
    return event_bus
