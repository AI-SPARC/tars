from handlers.connection_handler import connection_handler

def get_message_type(topic):
    """
    Extract the message type from the MQTT topic.

    :param topic: The MQTT topic string.
    :type topic: str
    :return: The message type (the last part of the topic).
    :rtype: str
    """
    return topic.split("/")[-1]


async def dispatch_message(topic, message, queue):
    """
    Process MQTT messages before sending them to the WebSocket.

    :param topic: The MQTT topic of the received message.
    :type topic: str
    :param message: The payload of the MQTT message.
    :type message: str
    :param queue: The queue to put the processed message for sending to WebSocket.
    :type queue: asyncio.Queue
    """
    message_type = get_message_type(topic)

    if message_type == "connection":
        processed_message = await connection_handler(message)
    else:
        processed_message = message

    await queue.put((topic, processed_message))
