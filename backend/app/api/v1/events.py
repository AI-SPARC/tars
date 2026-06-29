import asyncio
from contextlib import suppress

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.deps import EventBusDep

router = APIRouter(prefix="/events", tags=["events"])


@router.websocket("/ws")
async def events_websocket(websocket: WebSocket, event_bus: EventBusDep) -> None:
    await websocket.accept()
    try:
        async with event_bus.subscribe() as events:
            while True:
                event_task = asyncio.create_task(events.get())
                receive_task = asyncio.create_task(websocket.receive())
                done, pending = await asyncio.wait(
                    {event_task, receive_task}, return_when=asyncio.FIRST_COMPLETED
                )
                if receive_task in done:
                    message = receive_task.result()
                    if message["type"] == "websocket.disconnect":
                        event_task.cancel()
                        with suppress(asyncio.CancelledError):
                            await event_task
                        return
                if event_task in done:
                    await websocket.send_json(event_task.result().as_message())
                for task in pending:
                    task.cancel()
                    with suppress(asyncio.CancelledError):
                        await task
    except WebSocketDisconnect:
        return
