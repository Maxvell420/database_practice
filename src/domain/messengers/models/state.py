from pydantic import BaseModel

from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.enums.states import States


class State(BaseModel):
    id: int | None = None
    user_uid: str
    state: States
    messenger_type: MessangerTypes
    data: dict | None = None
