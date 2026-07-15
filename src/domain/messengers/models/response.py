from pydantic import BaseModel
from src.domain.messengers.enums.messangerTypes import MessangerTypes


class Response(BaseModel):
    id: int
    messenger_type: MessangerTypes
    request_id: int
    data: dict
    user_uuid: str
    response_uuid: str
