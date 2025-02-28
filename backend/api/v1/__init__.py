from fastapi import APIRouter
from api.v1.agv.agv_routes import router as agv_router

api_router = APIRouter()

api_router.include_router(agv_router)
