from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.services.user import UserService
from src.schemas.user import UserCreate, UserRead
from src.api.schemas.requests import UserRegister
from src.db.repositories.user import UserRepository
from src.services.auth import AuthService
from src.api.dependecies.user import (
    get_user_service,
    get_auth_service,
    get_user_id_from_token,
    validate_token_type,
    get_token_jti,
)
from src.schemas.auth import TokenInfo, TokenType
from src.api.schemas.responses import Tokens
from src.config import settings


router = APIRouter(prefix=f"{settings.api_v1_prefix}/users", tags=["users"])


@router.post("/register", response_model=Tokens, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserRegister,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    if await user_service.get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    user_dict = user.model_dump()
    user_dict.update(
        {"hashed_password": auth_service.hash_password(user_dict["password"])}
    )
    user_dict.pop("password")
    user = UserCreate(**user_dict)

    user = await user_service.create_user(user)

    access_token = auth_service.issue_access_token(user)
    refresh_token = await auth_service.issue_refresh_token(user)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=Tokens)
async def login_user(
    user: UserRegister,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    db_user = await user_service.get_user_by_username(user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    if not auth_service.check_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )

    access_token = auth_service.issue_access_token(db_user)
    refresh_token = await auth_service.issue_refresh_token(db_user)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout_user(
    user_id: int = Depends(get_user_id_from_token),
    jti: str = Depends(get_token_jti),
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
    _=Depends(validate_token_type(TokenType.REFRESH)),
):
    db_user = await user_service.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    await auth_service.revoke_refresh_token(user_id, jti)
    return {"message": "User logged out"}
