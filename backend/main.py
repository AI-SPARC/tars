from fastapi import FastAPI
from fastapi_pagination import add_pagination
from core.config import settings
from core.cors import setup_cors
from core.database import engine
from contextlib import asynccontextmanager
from api.v1 import api_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    Ensures that the database connection is ready before serving requests.
    """
    if settings.DATABASE_TYPE == "sqlite":
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: conn.exec_driver_sql("PRAGMA foreign_keys=ON;"))
    
    yield


app = FastAPI(
    title=settings.API_NAME,
    version=settings.API_VERSION,
    docs_url=settings.API_DOCS,
    redoc_url=settings.API_REDOC,
    debug=settings.API_DEBUG,
    lifespan=lifespan,
)

if settings.ENABLE_LOCAL_CORS:
    setup_cors(app)

add_pagination(app)

app.include_router(api_router)


@app.get("/")
def root():
    """Root endpoint to check API status."""
    return {"message": "Fleet Manager API is running."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=False)