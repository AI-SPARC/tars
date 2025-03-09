import json
import websockets
from typing import List

async def fetch_topics(ws: websockets.WebSocketClientProtocol) -> List[str]:
    """
    Fetch MQTT topics from the WebSocket API using an existing WebSocket connection.

    :param ws: The WebSocket connection to use for fetching topics.
    :type ws: websockets.WebSocketClientProtocol
    :return: List of MQTT topics.
    :rtype: list
    """
    topics_message = await ws.recv()
    topics = json.loads(topics_message)

    return topics
