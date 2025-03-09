from sqlalchemy.ext.asyncio import AsyncSession
from services.agv_service import AGVService

async def generate_topics(db: AsyncSession):
    """
    Generate MQTT topics based on AGVs registered in the database.

    :param db: Async database session.
    :type db: AsyncSession
    :return: List of MQTT topic strings.
    :rtype: list
    """
    topics = []
    agvs_page = await AGVService.get_all_agvs(db)
    agvs = agvs_page.items

    for agv in agvs:
        base_topic = f"tars/v2/{agv.manufacturer}/{agv.serial_number}"
        topics.extend([
            f"{base_topic}/order",
            f"{base_topic}/instantActions",
            f"{base_topic}/state",
            f"{base_topic}/visualization",
            f"{base_topic}/connection",
            f"{base_topic}/factsheet",
        ])

    return topics
