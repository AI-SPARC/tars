from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="TARS Fleet Manager API",
    version="0.1.0",
    description="Open-source VDA 5050 v3.0.0 fleet manager for research.",
)
app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.service_name, "docs": "/docs"}
