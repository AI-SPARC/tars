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


def test_cors_allows_configured_frontend_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
