from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from src.services.auth import AuthService
from src.db.repositories.auth import AuthRepository
from src.schemas.auth import TokenType
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependecies.dbs import get_async_session, get_redis_client
from src.db.repositories.user import UserRepository
from src.services.user import UserService

from src.config import settings

http_bearer = HTTPBearer(auto_error=False)


def get_auth_repository(session: AsyncSession = Depends(get_async_session)):
    return AuthRepository(session)


def get_auth_service(auth_repo: AuthRepository = Depends(get_auth_repository)):
    return AuthService(auth_repo)


def get_user_repository(session: AsyncSession = Depends(get_async_session)):
    return UserRepository(session)


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)


async def get_token_payload(
    authService: AuthService = Depends(get_auth_service),
    token: dict = Depends(http_bearer),
) -> dict:
    try:
        return await authService.validate_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_token_type(token_type: TokenType):
    async def __validate_token(
        authService: AuthService = Depends(get_auth_service),
        token: dict = Depends(http_bearer),
    ) -> None:
        try:
            await authService.validate_token(token, token_type)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return __validate_token


def get_user_id_from_token(token: dict = Depends(get_token_payload)) -> int:
    return int(token["sub"])


def get_token_jti(token: dict = Depends(get_token_payload)) -> str:
    return token["jti"]
