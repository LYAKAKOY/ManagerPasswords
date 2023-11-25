import uuid

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    login: str
    password: str

class ShowUser(TunedModel):
    user_id: uuid.UUID

class ChangePasswordUser(BaseModel):
    login: str
    password: str