from fastapi import APIRouter, Response, HTTPException, Depends

from src.users.schemas import SUser, SPasswordChange, SUsernameChange
from src.users.services.auth import service_auth_user, service_create_user, service_change_password, service_change_username
from src.users.services.dependencies import get_current_user

router = APIRouter(
    prefix='/profile',
    tags=['Авторизация и пользователи']
)

@router.post('')
async def create_user(body: SUser, response: Response):
    try:
        token = await service_create_user(body=body)
        response.set_cookie(key='access_token', value=token)
        return {'access_token': token}
    except HTTPException as e:
        raise e

@router.post('/auth')
async def auth_user(body: SUser, response: Response):
    try:
        token = await service_auth_user(body=body)
        response.set_cookie(key='access_token', value=token)
        return {'access_token': token}
    except HTTPException as e:
        raise e

@router.put('/change/password')
async def change_password(body: SPasswordChange, response: Response, user_id = Depends(get_current_user)):
    try:
        response.delete_cookie('access_token')
        return await service_change_password(body=body, user_id=user_id)
    except HTTPException as e:
        raise e

@router.put('/change/username')
async def change_username(body: SUsernameChange, user_id = Depends(get_current_user)):
    try:
        return await service_change_username(body=body, user_id=user_id)
    except HTTPException as e:
        raise e