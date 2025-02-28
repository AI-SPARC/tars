from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

from db.models.agv_model import AGVModel
from schemas.agv_schema import AGVCreate


class AGVRepository:
    """
    Repository for handling AGV database operations.
    """

    @staticmethod
    async def get_agvs(session: AsyncSession) -> Page[AGVModel]:
        """
        Retrieve a paginated list of AGVs.

        :param session: Database session.
        :return: Paginated list of AGVs.
        :raises RuntimeError: If database operation fails.
        """
        try:
            query = select(AGVModel)
            return await paginate(session, query)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error while fetching AGVs: {str(e)}") from e

    @staticmethod
    async def get_by_id(session: AsyncSession, agv_id: str) -> Optional[AGVModel]:
        """
        Retrieve a single AGV by its ID.

        :param session: Database session.
        :param agv_id: ID of the AGV (as string).
        :return: AGV instance if found, otherwise None.
        :raises SQLAlchemyError: If a database error occurs.
        """
        try:
            return await session.get(AGVModel, agv_id)
        except (SQLAlchemyError, ValueError) as e:
            raise RuntimeError(f"Database error while fetching AGV {agv_id}: {str(e)}") from e

    @staticmethod
    async def create(session: AsyncSession, agv_data: AGVCreate) -> AGVModel:
        """
        Create a new AGV entry in the database.

        :param session: Database session.
        :param agv_data: Data required to create an AGV.
        :return: Created AGV instance.
        :raises SQLAlchemyError: If a database error occurs.
        """
        try:
            agv = AGVModel(**agv_data.model_dump())
            session.add(agv)
            await session.commit()
            await session.refresh(agv)
            return agv
        except SQLAlchemyError as e:
            await session.rollback()
            raise RuntimeError(f"Database error while creating AGV: {str(e)}") from e
        
    @staticmethod
    async def update(session: AsyncSession, agv_id: str, agv_data: AGVCreate) -> Optional[AGVModel]:
        """
        Update an existing AGV by ID.

        :param session: Database session.
        :param agv_id: ID of the AGV.
        :param agv_data: Data to update (manufacturer, serial_number).
        :return: Updated AGV instance if successful, otherwise None.
        :raises RuntimeError: If database operation fails.
        """
        try:
            uuid_agv_id = str(agv_id)  # ✅ Converte UUID para String
            agv = await session.get(AGVModel, uuid_agv_id)
            if not agv:
                return None

            for key, value in agv_data.model_dump(exclude_unset=True).items():
                setattr(agv, key, value)

            await session.commit()
            await session.refresh(agv)
            return agv

        except SQLAlchemyError as e:
            await session.rollback()
            raise RuntimeError(f"Database error while updating AGV {agv_id}: {str(e)}") from e

    @staticmethod
    async def delete(session: AsyncSession, agv_id: str) -> Optional[AGVModel]:
        """
        Delete an AGV entry by ID.

        :param session: Database session.
        :param agv_id: ID of the AGV.
        :return: Deleted AGV instance if found, otherwise None.
        :raises SQLAlchemyError: If a database error occurs.
        """
        try:
            agv = await session.get(AGVModel, agv_id)
            if agv:
                await session.delete(agv)
                await session.commit()
                return agv
            return None
        except SQLAlchemyError as e:
            await session.rollback()
            raise RuntimeError(f"Database error while deleting AGV {agv_id}: {str(e)}") from e
