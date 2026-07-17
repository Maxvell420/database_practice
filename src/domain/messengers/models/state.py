from pydantic import BaseModel

from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.enums.states import States


class State(BaseModel):
    user_id: int
    state: States
    messenger_type: MessangerTypes
    data: dict | None = None
