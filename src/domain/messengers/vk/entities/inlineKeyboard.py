from pydantic import BaseModel
from src.domain.messengers.vk.entities.inlineKeyboardButton import InlineKeyboardButton


class InlineKeyboard(BaseModel):
    buttons: list[list[InlineKeyboardButton]]
    inline: bool = True
