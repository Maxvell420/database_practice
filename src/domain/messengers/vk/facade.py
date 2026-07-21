from src.domain.messengers.vk.values.vkPayload import VkPayload
from src.libs.infra.logger import Logger
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.builder import Builder
from src.domain.messengers.vk.entities.payload import Payload
from src.libs.infra.context import Context
from src.libs.vk.responses.update import Update


class Facade:
    def __init__(self, context: Context, logger: Logger | None = None):
        self.logger = logger
        self.builder = Builder(context, logger)

    async def handleNewUpdate(self, update: Update) -> VkPayload:
        useCase = await self.builder.buildUpdatesHandler()
        return await useCase.handleNewUpdate(update)
