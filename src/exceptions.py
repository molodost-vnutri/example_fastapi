from fastapi import HTTPException, status


class PasswordException:
    @classmethod
    def raise_exception(cls, detail: str) -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

UserOrPasswordIncorrect = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Неверный пароль'
)

UserIsAlreadyRegister = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Юзернейм уже занят'
)

OldPasswordIncorrect = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Старый пароль не валидный'
)

OldAndNewPasswordDubble = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Новый пароль не может совпадать со старым паролем"
)

SuccessFullChangePassword = HTTPException(
    status_code=status.HTTP_200_OK,
    detail='Пароль успешно сменён'
)

TokenAbsent = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Токен не найден'
)

TokenExpired = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Токен истёк'
)

TokenIsInvalid = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Токен не валиден'
)

SuccessFullChangeUsername = HTTPException(
    status_code=status.HTTP_200_OK,
    detail='Юзернейм успешно изменён'
)

TaskNotFoundOrTaskIsPrivate = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Задача не найдена либо она не в публичном доступе'
)

TaskNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Задача не найдена'
)

SuccessFullChangeTask = HTTPException(
    status_code=status.HTTP_201_CREATED,
    detail='Задача успешно изменена'
)