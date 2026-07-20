from src.libs.infra.logger import Logger
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.builder import Builder
from src.domain.messengers.vk.entities.payload import Payload
from src.libs.infra.context import Context


class Facade:
    def __init__(self, context: Context, logger: Logger | None = None):
        self.logger = logger
        self.builder = Builder(context, logger)

    async def handleNewMessage(self, text: str, user_uid: str) -> SendMessage:
        useCase = await self.builder.buildUpdatesHandler()
        return await useCase.handleNewMessage(text, user_uid)

    async def handleMessageEvent(
        self, payload: Payload, user_uid: str, request_id: int
    ) -> object:
        useCase = await self.builder.buildUpdatesHandler()
        return await useCase.handleMessageEvent(payload, user_uid, request_id)
