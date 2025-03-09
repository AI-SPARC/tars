from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from utils.topic_generator import generate_topics

router = APIRouter(
    prefix="/messenger",
    tags=["Messenger"],
)

@router.websocket("/ws/topics")
async def websocket_topics(websocket: WebSocket, db: AsyncSession = Depends(get_session)):
    """
    WebSocket endpoint that sends MQTT topics to the client.

    :param websocket: WebSocket connection.
    :type websocket: WebSocket
    :param db: Async database session.
    :type db: AsyncSession
    """
    await websocket.accept()
    topics = await generate_topics(db)
    await websocket.send_json(topics)
