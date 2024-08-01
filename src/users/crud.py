from sqlalchemy import insert, select

from src.database import async_session_maker
from src.CoreCRUD import BaseCRUD
from src.users.models import Users

class UsersCRUD(BaseCRUD):
    model = Users
    @classmethod
    async def add(cls, username: str, password: str) -> str:
        async with async_session_maker() as session:
            async with session.begin():
                user_insert_stmt = insert(cls.model).values(username=username, password=password).returning(cls.model.id)
                result = await session.execute(user_insert_stmt)
                user_id = result.scalar_one()
                return user_id
    @classmethod
    async def get_tasks(cls, user_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=user_id)
            result = await session.execute(query)
            user: Users = result.scalar_one()
            await session.refresh(user, ["tasks"])
            return user.tasks