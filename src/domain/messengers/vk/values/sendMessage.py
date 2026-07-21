from .vkPayload import VkPayload
from src.domain.messengers.vk.entities.inlineKeyboard import InlineKeyboard


class SendMessage(VkPayload):
    text: str
    user_uid: str
    # тут еще и простая клавиатура , но пока только inline
    keyboard: None | InlineKeyboard = None
