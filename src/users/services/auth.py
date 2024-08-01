from datetime import UTC, datetime, timedelta
from re import search

from passlib.context import CryptContext
from jwt import encode
from fastapi import HTTPException

from src.exceptions import PasswordException, SuccessFullChangePassword, OldAndNewPasswordDubble, UserIsAlreadyRegister, UserOrPasswordIncorrect, OldPasswordIncorrect, SuccessFullChangeUsername
from src.users.crud import UsersCRUD
from src.config import settings
from src.users.schemas import SUser, SPasswordChange, SUsernameChange

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def depend_password(password: str) -> HTTPException | None:
    if not password.isascii():
        raise PasswordException.raise_exception('Пароль должен содержать только печатаемые символы')
    if not search(r'[A-Z]', password):
        raise PasswordException.raise_exception('Пароль должен содержать минимум одну анлийскую букву верхнего регистра')
    if not search(r'[a-z]', password):
        raise PasswordException.raise_exception('Пароль должен содержать минимум одну анлийскую букву нижнего регистра')
    if not search(r'[0-9]', password):
        raise PasswordException.raise_exception('Пароль должен содержать хотя бы одно число')
    if not search(r'[\W_]', password):
        raise PasswordException.raise_exception('Пароль должен содержать хотя бы один спец символ')

def hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=password, hash=hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=3)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

async def service_auth_user(body: SUser) -> HTTPException | str:
    user = await UsersCRUD.find_one_or_none(username=body.username)
    if not user:
        raise UserOrPasswordIncorrect
    if not verify_password(password=body.password, hashed_password=user.password):
        raise UserOrPasswordIncorrect
    token = create_access_token({'sub': user.id})
    return token

async def service_create_user(body: SUser):
    user = await UsersCRUD.find_one_or_none(username=body.username)
    if user:
        raise UserIsAlreadyRegister
    hash_password = hashed_password(password=body.password)
    user_id = await UsersCRUD.add(
        username=body.username,
        password=hash_password
    )
    token = create_access_token({'sub': user_id})
    return token

async def service_change_password(body: SPasswordChange, user_id: str):
    password = depend_password(body.new_password)
    if password:
        raise password
    user = await UsersCRUD.find_one_or_none(id=user_id)
    if not verify_password(password=body.old_password, hashed_password=user.password): #type: ignore
        raise OldPasswordIncorrect
    if verify_password(password=body.new_password, hashed_password=user.password): #type: ignore
        raise OldAndNewPasswordDubble
    hash_password = hashed_password(password=body.new_password)
    await UsersCRUD.update(password=hash_password, id=user_id)
    return SuccessFullChangePassword

async def service_change_username(body: SUsernameChange, user_id: str):
    user = await UsersCRUD.find_one_or_none(username=body.new_username)
    if user:
        raise UserIsAlreadyRegister
    await UsersCRUD.update(username=body.new_username, id=user_id)
    return SuccessFullChangeUsername