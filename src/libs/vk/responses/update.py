from pydantic import BaseModel
from .object import Object
from src.libs.vk.enums.updateType import UpdateType


class Update(BaseModel):
    group_id: int
    type: UpdateType
    event_id: str
    v: str
    object: Object
