from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.services.location import LocationService
from src.api.schemas.responses import Distance

from src.api.dependecies.location import get_location_service
from src.api.dependecies.user import (
    get_token_payload,
    get_user_id_from_token,
    validate_token_type,
)

from src.api.schemas.requests import GenLocationRequest
from src.schemas.location import LocationScheme, LocationStatus
from src.schemas.auth import TokenType
from src.config import settings

from pydantic import Field

router = APIRouter(prefix=f"{settings.api_v1_prefix}/location", tags=["location"])


@router.post("/generate")
async def generate_location(
    location: GenLocationRequest,
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    if await location_service.get_location(user_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location already exists",
        )
    await location_service.generate_location(
        user_id,
        LocationScheme(**location.model_dump()),
    )
    return {"message": "Location generated"}


@router.post("/complete")
async def complete_location(
    complete_status: LocationStatus,
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    loc = await location_service.get_location(user_id)
    if loc is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location does not exist",
        )
    await location_service.complete_location(user_id, complete_status)
    return {"message": "Location completed"}


@router.get("/distance", response_model=Distance)
async def get_distance(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    loc = await location_service.get_location(user_id)
    if loc is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location does not exist",
        )
    dist = await location_service.get_distance(
        LocationScheme(**loc.model_dump()),
        LocationScheme(latitude=lat, longitude=lon),
    )
    return Distance(distance=dist, unit="m")
