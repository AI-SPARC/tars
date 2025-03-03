import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.agv_repository import AGVRepository
from schemas.agv_schema import AGVCreate
from fastapi_pagination import Params

@pytest.mark.asyncio
async def test_create_agv(session: AsyncSession):
    """
    Test creating an AGV and storing it in the database.

    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    agv_data = AGVCreate(manufacturer="Test Manufacturer", serial_number="123456")
    agv = await AGVRepository.create(session, agv_data)

    assert agv is not None
    assert agv.manufacturer == "Test Manufacturer"
    assert agv.serial_number == "123456"

@pytest.mark.asyncio
async def test_get_agvs(session: AsyncSession):
    """
    Test retrieving AGVs using pagination parameters.

    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    agv_data = AGVCreate(manufacturer="Test Manufacturer", serial_number="123456")
    await AGVRepository.create(session, agv_data)

    agvs = await AGVRepository.get_agvs(session, Params(size=10, page=1))

    assert len(agvs.items) > 0
    assert agvs.items[0].manufacturer == "Test Manufacturer"

@pytest.mark.asyncio
async def test_get_by_id(session: AsyncSession):
    """
    Test fetching an AGV by its unique identifier.

    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    agv_data = AGVCreate(manufacturer="Test Manufacturer", serial_number="123456")
    created_agv = await AGVRepository.create(session, agv_data)

    agv = await AGVRepository.get_by_id(session, created_agv.id)
    assert agv is not None
    assert agv.id == created_agv.id

@pytest.mark.asyncio
async def test_update_agv(session: AsyncSession):
    """
    Test updating an existing AGV in the database.

    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    agv_data = AGVCreate(manufacturer="Test Manufacturer", serial_number="123456")
    created_agv = await AGVRepository.create(session, agv_data)

    updated_data = AGVCreate(manufacturer="Updated Manufacturer", serial_number="654321")
    updated_agv = await AGVRepository.update(session, created_agv.id, updated_data)

    assert updated_agv is not None
    assert updated_agv.manufacturer == "Updated Manufacturer"
    assert updated_agv.serial_number == "654321"

@pytest.mark.asyncio
async def test_delete_agv(session: AsyncSession):
    """
    Test deleting an AGV and verifying its removal.

    :param session: Asynchronous database session.
    :type session: AsyncSession
    """
    agv_data = AGVCreate(manufacturer="Test Manufacturer", serial_number="123456")
    created_agv = await AGVRepository.create(session, agv_data)

    deleted_agv = await AGVRepository.delete(session, created_agv.id)
    assert deleted_agv is not None
    assert deleted_agv.id == created_agv.id

    agv_check = await AGVRepository.get_by_id(session, created_agv.id)
    assert agv_check is None
