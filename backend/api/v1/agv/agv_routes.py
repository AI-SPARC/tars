from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from core.deps import get_session
from services.agv_service import AGVService
from schemas.agv_schema import AGVRead, AGVCreate

router = APIRouter(
    prefix="/agvs",
    tags=["AGVs"],
    responses={404: {"description": "AGV not found"}},
)

@router.get(
    "/",
    response_model=Page[AGVRead],
    status_code=200,
    summary="List all AGVs",
    description="Retrieve a paginated list of all AGVs stored in the system.",
    responses={
        200: {"description": "Successful response"},
        500: {"description": "Internal server error"},
    },
)
async def list_agvs(db: AsyncSession = Depends(get_session)):
    """
    Retrieve a paginated list of all AGVs.

    **Returns:**  
    - A paginated list of AGVs.
    - **200 OK** if successful.
    - **500 Internal Server Error** if an unexpected issue occurs.
    """
    return await AGVService.get_all_agvs(db)

@router.get(
    "/{agv_id}",
    response_model=AGVRead,
    status_code=200,
    summary="Get a single AGV by ID",
    description="Retrieve details of a specific AGV using its unique ID.",
    responses={
        200: {"description": "AGV found and returned"},
        404: {"description": "AGV not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_agv(agv_id: str, db: AsyncSession = Depends(get_session)):
    """
    Retrieve a single AGV by its ID.

    **Parameters:**  
    - `agv_id`: The unique identifier of the AGV.

    **Returns:**  
    - The requested AGV details.
    - **404 Not Found** if the AGV does not exist.
    """
    agv = await AGVService.get_agv_by_id(db, agv_id)
    if not agv:
        raise HTTPException(status_code=404, detail="AGV not found")
    return agv

@router.post(
    "/",
    response_model=AGVRead,
    status_code=201,
    summary="Create a new AGV",
    description="Register a new AGV in the system.",
    responses={
        201: {"description": "AGV created successfully"},
        400: {"description": "Failed to create AGV"},
        500: {"description": "Internal server error"},
    },
)
async def create_new_agv(agv_data: AGVCreate, db: AsyncSession = Depends(get_session)):
    """
    Create a new AGV.

    **Request Body:**  
    - `manufacturer`: Name of the AGV manufacturer.
    - `serial_number`: Unique serial number of the AGV.

    **Returns:**  
    - The newly created AGV details.
    - **400 Bad Request** if creation fails.
    """
    agv = await AGVService.create_agv(db, agv_data)
    if not agv:
        raise HTTPException(status_code=400, detail="Failed to create AGV")
    return agv

@router.put(
    "/{agv_id}",
    response_model=AGVRead,
    status_code=200,
    summary="Update an AGV by ID",
    description="Modify the manufacturer and/or serial number of an existing AGV.",
    responses={
        200: {"description": "AGV updated successfully"},
        400: {"description": "Invalid request data"},
        404: {"description": "AGV not found"},
        500: {"description": "Internal server error"},
    },
)
async def update_agv(
    agv_id: str,
    agv_data: AGVCreate,
    db: AsyncSession = Depends(get_session),
):
    """
    Update an AGV.

    **Body Parameters**:
    - `manufacturer` (optional): New manufacturer name.
    - `serial_number` (optional): New serial number.

    **Returns**:
    - `200 OK`: Updated AGV.
    - `404 Not Found`: If AGV does not exist.
    """
    agv = await AGVService.update_agv(db, agv_id, agv_data)
    if not agv:
        raise HTTPException(status_code=404, detail="AGV not found")
    return agv

@router.delete(
    "/{agv_id}",
    response_model=AGVRead,
    status_code=200,
    summary="Delete an AGV by ID",
    description="Remove an AGV from the system using its ID.",
    responses={
        200: {"description": "AGV deleted successfully"},
        404: {"description": "AGV not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_agv_by_id(agv_id: str, db: AsyncSession = Depends(get_session)):
    """
    Delete an AGV by its ID.

    **Parameters:**  
    - `agv_id`: The unique identifier of the AGV.

    **Returns:**  
    - The deleted AGV details.
    - **404 Not Found** if the AGV does not exist.
    """
    agv = await AGVService.delete_agv(db, agv_id)
    if not agv:
        raise HTTPException(status_code=404, detail="AGV not found")
    return agv