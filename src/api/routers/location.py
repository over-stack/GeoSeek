from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.services.location import LocationService
from src.api.schemas.responses import Distance

from src.api.dependecies.location import get_location_service
from src.api.dependecies.user import (
    get_token_payload,
    get_user_id_from_token,
    validate_token_type,
)

from src.api.schemas.requests import LocationRequest
from src.schemas.location import LocationScheme, LocationStatus
from src.schemas.auth import TokenType
from src.config import settings
from src.api.schemas.responses import TrackResponse


router = APIRouter(prefix=f"{settings.api_v1_prefix}/locations", tags=["locations"])


@router.post(
    "/generate", status_code=status.HTTP_201_CREATED, description="Generate location"
)
async def generate_location(
    location: LocationRequest,
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    try:
        await location_service.generate_location(
            user_id,
            LocationScheme(**location.model_dump()),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return {"message": "Location generated"}


@router.post(
    "/cancel",
    response_model=TrackResponse,
    status_code=status.HTTP_200_OK,
    description="Cancel location",
)
async def cancel_location(
    location: LocationRequest,
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    try:
        loc, dist = await location_service.cancel_location(
            user_id,
            LocationScheme(**location.model_dump()),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return TrackResponse(
        status=LocationStatus.CANCELLED,
        location=loc,
        distance=Distance(distance=dist, unit="m"),
    )


@router.post(
    "/track",
    response_model=TrackResponse,
    status_code=status.HTTP_200_OK,
    description="Check distance to location",
)
async def check_distance(
    location: LocationRequest,
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    try:
        loc, dist = await location_service.track_location(
            user_id,
            LocationScheme(**location.model_dump()),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return TrackResponse(
        status=LocationStatus.CANCELLED,
        location=loc,
        distance=Distance(distance=dist, unit="m"),
    )


@router.get(
    "/history",
    response_model=list[LocationScheme],
    status_code=status.HTTP_200_OK,
    description="Get location history",
)
async def get_location_history(
    user_id: int = Depends(get_user_id_from_token),
    location_service: LocationService = Depends(get_location_service),
    _=Depends(validate_token_type(TokenType.ACCESS)),
):
    try:
        return await location_service.get_location_history(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
