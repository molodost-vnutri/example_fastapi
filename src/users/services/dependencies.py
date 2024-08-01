from datetime import UTC, datetime
from fastapi import Depends, Request
from jwt import decode

from src.config import settings
from src.exceptions import (
    TokenAbsent,
    TokenExpired,
    TokenIsInvalid
)

def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise TokenAbsent
    return token.strip()

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except Exception:
        raise TokenIsInvalid
    expire: str = payload.get('exp') # type: ignore

    expire_datetime = datetime.fromtimestamp(expire, tz=UTC) # type: ignore

    if not expire or expire_datetime < datetime.now(UTC):
        raise TokenExpired
    
    user_id: str | None = payload.get('sub')
    if not user_id:
        raise TokenIsInvalid
    return int(user_id)