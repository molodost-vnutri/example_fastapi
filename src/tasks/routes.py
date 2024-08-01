from fastapi import APIRouter, Depends

from src.exceptions import TaskNotFoundOrTaskIsPrivate, TaskNotFound, SuccessFullChangeTask
from src.tasks.schemas import STasks
from src.tasks.crud import TasksCRUD
from src.users.crud import UsersCRUD
from src.users.services.dependencies import get_current_user

router = APIRouter(
    prefix='/tasks',
    default=['Задачи']
)

@router.get('')
async def get_tasks_user(user_id = Depends(get_current_user)):
    return await UsersCRUD.get_tasks(user_id=user_id)

@router.post('/new_task')
async def add_task_user(task: STasks, user_id = Depends(get_current_user)):
    return await TasksCRUD.add_task(user_id=user_id, task=task)

@router.get('/public/task/{id}')
async def get_public_task(id: int):
    result = await TasksCRUD.find_one_or_none(id=id, public=True)
    if result:
        return result
    raise TaskNotFoundOrTaskIsPrivate

@router.post('/change/task')
async def change_task(task_id: int, task_body: STasks, user_id = Depends(get_current_user)):
    task = await TasksCRUD.find_one_or_none(user_id=user_id, id=task_id)
    if not task:
        raise TaskNotFound
    await TasksCRUD.update(name=task_body.name, title=task_body.title, public=task_body.public, id=task_id)
    return SuccessFullChangeTask