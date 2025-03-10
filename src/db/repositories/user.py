from src.db.models.user import User
from src.schemas.user import UserCreate, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate) -> UserRead:
        async with self.session.begin():
            db_user = User(**user.model_dump())
            self.session.add(db_user)
            await self.session.commit()
            return UserRead.model_validate(db_user)

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        async with self.session.begin():
            db_user = await self.session.get(User, user_id)
            if db_user is None:
                return None
            return UserRead.model_validate(db_user)

    async def get_user_by_username(self, username: str) -> UserRead | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(User).where(User.username == username)
            )
            db_user = result.scalar_one_or_none()
            if db_user is None:
                return None
            return UserRead.model_validate(db_user)
