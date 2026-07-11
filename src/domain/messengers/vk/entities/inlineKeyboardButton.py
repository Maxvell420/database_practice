from pydantic import BaseModel
from src.domain.messengers.vk.entities.inlineKeyboardButtonAction import (
    InlineKeyboardButtonAction,
)


class InlineKeyboardButton(BaseModel):
    action: InlineKeyboardButtonAction
    color: str | None = None
