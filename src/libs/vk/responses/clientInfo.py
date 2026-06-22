
from pydantic import BaseModel
class ClientInfo(BaseModel):
    button_actions: list[str]
    keyboard: bool
    inline_keyboard: bool
    carousel: bool
    lang_id: int
