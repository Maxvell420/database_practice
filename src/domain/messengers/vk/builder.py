from src.libs.infra.logger import Logger
from src.domain.messengers.vk.useCases.updatesHandler import UpdatesHandler
from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)


class Builder:
    def __init__(self, logger: Logger | None = None):
        self.logger = logger
        # TODO: подумать насчет состояний, возможно UpdatesHandler не надо создавать каждый раз

    async def buildUpdatesHandler(self) -> UpdatesHandler:
        return UpdatesHandler(await self.buildInlineKeyboardBuilder())

    async def buildInlineKeyboardBuilder(self) -> InlineKeyboardBuilder:
        return InlineKeyboardBuilder()
