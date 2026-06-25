import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.deps import get_session
from app.db.base import Base
from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override_session():
        async with maker() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()
    await engine.dispose()


async def test_create_and_list_robots(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/robots",
        json={"manufacturer": "ResearchBot", "serialNumber": "RB001", "displayName": "Lab robot"},
    )

    assert create_response.status_code == 201
    assert create_response.json()["serialNumber"] == "RB001"

    list_response = await client.get("/api/v1/robots")

    assert list_response.status_code == 200
    assert list_response.json()[0]["manufacturer"] == "ResearchBot"


async def test_create_map_with_nodes_and_route_preview(client: AsyncClient) -> None:
    map_response = await client.post("/api/v1/maps", json={"name": "Lab"})
    map_id = map_response.json()["id"]

    await client.post(f"/api/v1/maps/{map_id}/nodes", json={"nodeKey": "A", "x": 0, "y": 0})
    await client.post(f"/api/v1/maps/{map_id}/nodes", json={"nodeKey": "B", "x": 1, "y": 0})
    edge_response = await client.post(
        f"/api/v1/maps/{map_id}/edges",
        json={"edgeKey": "A-B", "fromNodeKey": "A", "toNodeKey": "B", "distance": 1.0},
    )

    assert edge_response.status_code == 201

    route_response = await client.post(
        f"/api/v1/maps/{map_id}/route-preview", json={"startNodeKey": "A", "goalNodeKey": "B"}
    )

    assert route_response.status_code == 200
    assert route_response.json()["nodeKeys"] == ["A", "B"]


async def test_create_mission(client: AsyncClient) -> None:
    robot_response = await client.post(
        "/api/v1/robots", json={"manufacturer": "ResearchBot", "serialNumber": "RB003"}
    )

    mission_response = await client.post(
        "/api/v1/missions",
        json={
            "assignedRobotId": robot_response.json()["id"],
            "startNodeKey": "A",
            "goalNodeKey": "B",
        },
    )

    assert mission_response.status_code == 201
    assert mission_response.json()["status"] == "queued"
