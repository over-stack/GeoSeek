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
from fastapi.security import HTTPAuthorizationCredentials
from src.api.dependecies.dbs import get_redis_client
from redis import asyncio as aioredis
from src.exceptions.auth import InvalidTokenType, TokenNotFoundError

from src.config import settings

http_bearer = HTTPBearer(auto_error=False)


def get_auth_repository(rdb: aioredis.Redis = Depends(get_redis_client)):
    return AuthRepository(rdb)


def get_auth_service(auth_repo: AuthRepository = Depends(get_auth_repository)):
    return AuthService(auth_repo)


def get_user_repository(session: AsyncSession = Depends(get_async_session)):
    return UserRepository(session)


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)


async def get_token_payload(
    authService: AuthService = Depends(get_auth_service),
    creds: HTTPAuthorizationCredentials | None = Depends(http_bearer),
) -> dict:
    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = creds.credentials
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
    except InvalidTokenType as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type: {e.token_type}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except TokenNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_token_type(token_type: TokenType):
    async def __validate_token(
        authService: AuthService = Depends(get_auth_service),
        creds: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    ) -> None:
        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            token = creds.credentials
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
        except InvalidTokenType as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token type: {e.token_type}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except TokenNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return __validate_token


def get_user_id_from_token(payload: dict = Depends(get_token_payload)) -> int:
    return int(payload["sub"])


def get_token_jti(payload: dict = Depends(get_token_payload)) -> str:
    return payload["jti"]
