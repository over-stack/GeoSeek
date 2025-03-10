from src.db.repositories.user import UserRepository
from src.schemas.user import UserCreate, UserRead
from src.api.schemas.requests import UserRegister


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate) -> UserRead:
        return await self.user_repo.create_user(user)

    async def get_user_by_id(self, user_id: int) -> UserRead:
        return await self.user_repo.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> UserRead:
        return await self.user_repo.get_user_by_username(username)
