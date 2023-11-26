import uuid
from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from password_strength import PasswordStats
from api.base_schemas import TunedModel

class CheckCredentials:
    @field_validator("login")
    def validate_surname(cls, value):
        if not len(value) >= 5:
            raise HTTPException(status_code=422, detail="login is too short")
        return value
    @field_validator("password")
    def validate_surname(cls, value):
        if not PasswordStats(value).strength() > 0.5:
            raise HTTPException(status_code=422, detail="password is too simple")
        return value
class CreateUser(CheckCredentials, BaseModel):
    login: str
    password: str

class ShowUser(TunedModel):
    user_id: uuid.UUID

class ChangePasswordUser(CheckCredentials, BaseModel):
    login: str
    password: str