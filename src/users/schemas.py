from pydantic import BaseModel, Field

class SUser(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    password: str = Field(min_length=12, max_length=32)

class SPasswordChange(BaseModel):
    old_password: str = Field(min_length=12, max_length=32)
    new_password: str = Field(min_length=12, max_length=32)

class SUsernameChange(BaseModel):
    new_username: str = Field(min_length=6, max_length=20)