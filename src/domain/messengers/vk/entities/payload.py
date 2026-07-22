from pydantic import BaseModel
from src.domain.messengers.vk.enums.actions import Actions


class Payload(BaseModel):
    action: Actions
    value: None | str = None
