from api.base_schemas import TunedModel

class Token(TunedModel):
    access_token: str
    token_type: str