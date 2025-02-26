from fastapi import FastAPI
from config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.API_VERSION, debug=settings.DEBUG)


@app.get("/")
def root():
    """Root endpoint to check API status."""
    return {"message": "Fleet Manager API is running."}