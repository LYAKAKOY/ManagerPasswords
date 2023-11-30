from pydantic import BaseModel

from api.base_schemas import TunedModel


class CreatePassword(BaseModel):
    password: str


class ShowPassword(TunedModel):
    service_name: str
    password: str

class DeletedPassword(TunedModel):
    password_id: int