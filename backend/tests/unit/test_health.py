from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_service_metadata() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "tars-backend",
        "vda5050_version": "3.0.0",
    }
