from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    login: str
    password: str