import uuid

from api.base_schemas import TunedModel
from fastapi import HTTPException
from password_strength import PasswordStats
from pydantic import BaseModel
from pydantic import field_validator


class CheckCredentials:
    @field_validator("login")
    def validate_login(cls, value):
        if not len(value) >= 5:
            raise HTTPException(status_code=422, detail="the login is too short")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if not PasswordStats(value).strength() > 0.5:
            raise HTTPException(status_code=422, detail="the password is too simple")
        return value


class CreateUser(CheckCredentials, BaseModel):
    login: str
    password: str


class ShowUser(TunedModel):
    user_id: uuid.UUID


class ChangePasswordUser(CheckCredentials, BaseModel):
    login: str
    password: str
