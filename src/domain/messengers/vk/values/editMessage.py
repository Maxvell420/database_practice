from .vkPayload import VkPayload
from src.domain.messengers.vk.entities.inlineKeyboard import InlineKeyboard


class EditMessage(VkPayload):
    # На самом деле необязательная , но пока пусть будет
    text: str
    # тут еще и простая клавиатура , но пока только inline
    keyboard: None | InlineKeyboard = None
    user_uid: str
    message_id: int
