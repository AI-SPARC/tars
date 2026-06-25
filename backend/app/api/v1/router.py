from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.maps import router as maps_router
from app.api.v1.missions import router as missions_router
from app.api.v1.robots import router as robots_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(robots_router)
api_router.include_router(maps_router)
api_router.include_router(missions_router)
