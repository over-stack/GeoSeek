from fastapi import APIRouter, Depends, HTTPException, status

from src.services.location import LocationService

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
    status: LocationStatus,
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    await location_service.complete_location(user_id, status)
    return {"message": "Location completed"}
