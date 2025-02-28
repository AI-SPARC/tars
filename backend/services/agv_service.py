from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from db.repositories.agv_repository import AGVRepository
from schemas.agv_schema import AGVCreate, AGVRead


class AGVService:
    """
    Service layer for handling AGV business logic.
    """

    @staticmethod
    async def get_all_agvs(session: AsyncSession) -> Page[AGVRead]:
        """
        Retrieve all AGVs with pagination.

        :param session: Database session.
        :return: Paginated list of AGVs.
        """
        return await AGVRepository.get_agvs(session)

    @staticmethod
    async def get_agv_by_id(session: AsyncSession, agv_id: str) -> Optional[AGVRead]:
        """
        Retrieve an AGV by its ID.

        :param session: Database session.
        :param agv_id: ID of the AGV.
        :return: AGV instance as AGVRead if found, otherwise None.
        :raises RuntimeError: If database operation fails.
        """
        agv = await AGVRepository.get_by_id(session, agv_id)
        return AGVRead.model_validate(agv) if agv else None
    
    @staticmethod
    async def create_agv(session: AsyncSession, agv_data: AGVCreate) -> AGVRead:
        """
        Create a new AGV.

        :param session: Database session.
        :param agv_data: AGV data (manufacturer, serial number).
        :return: Created AGV instance as AGVRead.
        :raises RuntimeError: If database operation fails.
        """
        agv = await AGVRepository.create(session, agv_data)
        return AGVRead.model_validate(agv)

    @staticmethod
    async def update_agv(session: AsyncSession, agv_id: str, agv_data: AGVCreate) -> Optional[AGVRead]:
        """
        Update an AGV.

        :param session: Database session.
        :param agv_id: ID of the AGV.
        :param agv_data: Data for updating the AGV.
        :return: Updated AGV instance if successful, otherwise None.
        :raises RuntimeError: If database operation fails.
        """
        agv = await AGVRepository.update(session, agv_id, agv_data)
        if not agv:
            return None
        return AGVRead.model_validate(agv)

    @staticmethod
    async def delete_agv(session: AsyncSession, agv_id: str) -> Optional[AGVRead]:
        """
        Delete an AGV by its ID.

        :param session: Database session.
        :param agv_id: ID of the AGV.
        :return: Deleted AGV instance as AGVRead if found, otherwise None.
        :raises RuntimeError: If database operation fails.
        """
        agv = await AGVRepository.delete(session, agv_id)
        return AGVRead.model_validate(agv) if agv else None
