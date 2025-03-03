import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from services.agv_service import AGVService
from db.repositories.agv_repository import AGVRepository
from schemas.agv_schema import AGVCreate, AGVRead
from fastapi_pagination import Page
from datetime import datetime, timezone

@pytest.mark.asyncio
@patch.object(AGVRepository, 'create', new_callable=AsyncMock)
async def test_create_agv(mock_create, session: AsyncSession):
    """
    Test the creation of an AGV via the service layer.

    :param mock_create: Mocked method for AGVRepository.create.
    :type mock_create: AsyncMock
    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    agv_data = AGVCreate(manufacturer="Test Manufacturer", serial_number="123456")
    mock_create.return_value = AGVRead(
        id="1", manufacturer="Test Manufacturer", serial_number="123456",
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)
    )
    
    agv = await AGVService.create_agv(session, agv_data)
    
    assert agv is not None
    assert isinstance(agv, AGVRead)
    assert agv.manufacturer == "Test Manufacturer"
    assert agv.serial_number == "123456"
    mock_create.assert_awaited_once()

@pytest.mark.asyncio
@patch.object(AGVRepository, 'get_agvs', new_callable=AsyncMock)
async def test_get_all_agvs(mock_get_agvs, session: AsyncSession):
    """
    Test retrieving all AGVs with pagination.

    :param mock_get_agvs: Mocked method for AGVRepository.get_agvs.
    :type mock_get_agvs: AsyncMock
    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    mock_get_agvs.return_value = Page(
        items=[AGVRead(id="1", manufacturer="Test Manufacturer", serial_number="123456",
                       created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))],
        total=1, page=1, size=10
    )
    
    agvs = await AGVService.get_all_agvs(session)
    
    assert isinstance(agvs, Page)
    assert len(agvs.items) > 0
    assert isinstance(agvs.items[0], AGVRead)
    assert agvs.items[0].manufacturer == "Test Manufacturer"
    mock_get_agvs.assert_awaited_once()

@pytest.mark.asyncio
@patch.object(AGVRepository, 'get_by_id', new_callable=AsyncMock)
async def test_get_agv_by_id(mock_get_by_id, session: AsyncSession):
    """
    Test retrieving an AGV by its ID.

    :param mock_get_by_id: Mocked method for AGVRepository.get_by_id.
    :type mock_get_by_id: AsyncMock
    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    mock_get_by_id.return_value = AGVRead(
        id="1", manufacturer="Test Manufacturer", serial_number="123456",
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)
    )
    
    agv = await AGVService.get_agv_by_id(session, "1")
    assert agv is not None
    assert isinstance(agv, AGVRead)
    assert agv.id == "1"
    mock_get_by_id.assert_awaited_once()

@pytest.mark.asyncio
@patch.object(AGVRepository, 'update', new_callable=AsyncMock)
async def test_update_agv(mock_update, session: AsyncSession):
    """
    Test updating an AGV via the service layer.

    :param mock_update: Mocked method for AGVRepository.update.
    :type mock_update: AsyncMock
    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    updated_data = AGVCreate(manufacturer="Updated Manufacturer", serial_number="654321")
    mock_update.return_value = AGVRead(
        id="1", manufacturer="Updated Manufacturer", serial_number="654321",
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)
    )
    
    updated_agv = await AGVService.update_agv(session, "1", updated_data)
    
    assert updated_agv is not None
    assert isinstance(updated_agv, AGVRead)
    assert updated_agv.manufacturer == "Updated Manufacturer"
    assert updated_agv.serial_number == "654321"
    mock_update.assert_awaited_once()

@pytest.mark.asyncio
@patch.object(AGVRepository, 'delete', new_callable=AsyncMock)
async def test_delete_agv(mock_delete, session: AsyncSession):
    """
    Test deleting an AGV via the service layer.

    :param mock_delete: Mocked method for AGVRepository.delete.
    :type mock_delete: AsyncMock
    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    mock_delete.return_value = AGVRead(
        id="1", manufacturer="Test Manufacturer", serial_number="123456",
        created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)
    )
    
    deleted_agv = await AGVService.delete_agv(session, "1")
    assert deleted_agv is not None
    assert isinstance(deleted_agv, AGVRead)
    assert deleted_agv.id == "1"
    mock_delete.assert_awaited_once()