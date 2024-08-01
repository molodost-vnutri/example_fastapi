from sqlalchemy import insert
from sqlalchemy.exc import NoResultFound

from src.database import async_session_maker
from src.CoreCRUD import BaseCRUD
from src.tasks.models import Tasks
from src.tasks.schemas import STasks

class TasksCRUD(BaseCRUD):
    model = Tasks

    @classmethod
    async def add_task(cls, user_id, task: STasks):
        async with async_session_maker() as session:
            async with session.begin():
                task_insert_stmt = insert(cls.model).values(
                    name=task.name,
                    title=task.title,
                    user_id=user_id,
                    public=task.public
                ).returning(cls.model.id)
                result = await session.execute(task_insert_stmt)
                try:
                    task_id = result.scalar_one()
                    return task_id
                except NoResultFound:
                    return None