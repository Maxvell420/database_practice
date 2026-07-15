from src.libs.infra.logger import Logger
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.builder import Builder
from src.libs.vk.responses.object import Object


class Facade:
    def __init__(self, logger: Logger | None = None):
        self.logger = logger
        self.builder = Builder(logger)

    async def handleNewMessage(self, text: str, user_uid: int) -> SendMessage:
        useCase = await self.builder.buildUpdatesHandler()
        return await useCase.handleNewMessage(text, user_uid)

    async def handleMessageEvent(self, payload: str, user_uid: int) -> Object:
        useCase = await self.builder.buildUpdatesHandler()
        return await useCase.handleMessageEvent(payload, user_uid)
