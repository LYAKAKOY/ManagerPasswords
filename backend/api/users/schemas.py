import uuid
from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from password_strength import PasswordStats
from api.base_schemas import TunedModel

class CheckPasswordStrength:
    @field_validator("password")
    def validate_surname(cls, value):
        if not PasswordStats(value).strength() > 0.5:
            raise HTTPException(status_code=422, detail="password is too simple")
        return value
class CreateUser(CheckPasswordStrength, BaseModel):
    login: str
    password: str

class ShowUser(TunedModel):
    user_id: uuid.UUID

class ChangePasswordUser(CheckPasswordStrength, BaseModel):
    login: str
    password: str