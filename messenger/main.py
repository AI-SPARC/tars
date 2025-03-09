import asyncio
import websockets
import aiomqtt
from config import MQTT_BROKER, WS_API_URL
from utils.fetch_topics import fetch_topics
from utils.dispatch_messages import dispatch_message


async def mqtt_client(ws, queue):
    """
    MQTT client that subscribes to topics retrieved via WebSocket.

    It fetches the topics from the API, subscribes to them, and listens for messages.

    :param ws: The WebSocket connection to fetch topics.
    :param queue: The queue to put the processed messages for sending to WebSocket.
    :type ws: websockets.WebSocketClientProtocol
    :type queue: asyncio.Queue
    :return: None
    :rtype: None
    """
    # Pass the WebSocket to fetch topics
    topics = await fetch_topics(ws)

    async with aiomqtt.Client(MQTT_BROKER) as client:
        await client.connect()
        print(f"Connected to MQTT Broker at {MQTT_BROKER}")

        for topic in topics:
            await client.subscribe(topic)
            print(f"Subscribed to: {topic}")

        async for message in client.deliver_message():
            topic = message.topic
            payload = message.payload.decode()
            print(f"MQTT Received ({topic}): {payload}")
            # Pass the queue to dispatch_message to add processed message to the queue
            await dispatch_message(topic, payload, queue)


async def websocket_client(queue):
    """
    WebSocket client that sends messages from the queue to the API.

    :param queue: The queue from which messages will be sent to the WebSocket.
    :type queue: asyncio.Queue
    :return: None
    :rtype: None
    """
    # Create the WebSocket connection and pass it to mqtt_client and fetch_topics
    async with websockets.connect(WS_API_URL) as ws:
        while True:
            # Run mqtt_client with the WebSocket connection and the queue
            await asyncio.gather(mqtt_client(ws, queue), process_websocket(ws, queue))


async def process_websocket(ws, queue):
    """
    Process WebSocket communication and send messages from the queue to the WebSocket API.

    :param ws: The WebSocket connection to send messages to.
    :param queue: The queue that holds the messages to send.
    :type ws: websockets.WebSocketClientProtocol
    :type queue: asyncio.Queue
    :return: None
    :rtype: None
    """
    while True:
        topic, message = await queue.get()
        await ws.send(message)
        print(f"Sent to WebSocket: {message}")


async def main():
    """
    Main function that runs the MQTT and WebSocket clients concurrently.

    :return: None
    :rtype: None
    """
    queue = asyncio.Queue()
    await websocket_client(queue)


if __name__ == "__main__":
    asyncio.run(main())
