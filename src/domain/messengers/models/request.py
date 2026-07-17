from pydantic import BaseModel
from src.domain.messengers.enums.messangerTypes import MessangerTypes


class Request(BaseModel):
    id: int
    messenger_type: MessangerTypes
    data: dict
    user_uuid: str
    request_uuid: str
