from pydantic import BaseModel
from .object import Object
from src.libs.vk.enums.updateType import UpdateType


class MessageEvent(BaseModel):
    group_id: int
    event_id: str
    v: str
    type: UpdateType
    object: Object
