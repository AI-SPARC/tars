import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
WS_API_URL = os.getenv("WS_API_URL", "ws://localhost:8000/ws/topics")