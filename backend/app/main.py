from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.mqtt.asyncio_compat import configure_windows_selector_event_loop_policy
from app.mqtt.worker import MqttWorker

configure_windows_selector_event_loop_policy()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    mqtt_worker = MqttWorker(settings) if settings.mqtt_enabled else None
    if mqtt_worker is not None:
        mqtt_worker.start()
    app.state.mqtt_worker = mqtt_worker
    try:
        yield
    finally:
        if mqtt_worker is not None:
            await mqtt_worker.stop()


app = FastAPI(
    title="TARS Fleet Manager API",
    version="1.0.0",
    description="Open-source VDA 5050 v3.0.0 fleet manager for research.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.backend_cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.service_name, "docs": "/docs"}
