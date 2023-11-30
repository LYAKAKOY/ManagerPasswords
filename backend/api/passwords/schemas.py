import uuid

from api.base_schemas import TunedModel
from pydantic import BaseModel


class CreatePassword(BaseModel):
    password: str


class ShowPassword(TunedModel):
    service_name: str
    password: str


class DeletedPassword(TunedModel):
    user_id: uuid.UUID
