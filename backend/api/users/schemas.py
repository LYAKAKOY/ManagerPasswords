import uuid
from pydantic import BaseModel
from api.base_schemas import TunedModel

class CreateUser(BaseModel):
    login: str
    password: str

class ShowUser(TunedModel):
    user_id: uuid.UUID

class ChangePasswordUser(BaseModel):
    login: str
    password: str