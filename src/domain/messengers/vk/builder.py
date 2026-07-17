from src.libs.infra.logger import Logger
from src.domain.messengers.vk.useCases.updatesHandler import UpdatesHandler
from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)
from src.domain.messengers.repositories.requestRepository import RequestRepository
from src.domain.messengers.repositories.responseRepository import ResponseRepository
from src.libs.infra.context import Context


class Builder:
    def __init__(self, context: Context, logger: Logger | None = None):
        self.logger = logger
        self.context = context
        # TODO: подумать насчет состояний, возможно UpdatesHandler не надо создавать каждый раз

    async def buildUpdatesHandler(self) -> UpdatesHandler:
        return UpdatesHandler(
            await self.buildInlineKeyboardBuilder(),
            await self.buildResponseRepository(),
        )

    async def buildInlineKeyboardBuilder(self) -> InlineKeyboardBuilder:
        return InlineKeyboardBuilder()

    async def buildRequestRepository(self) -> RequestRepository:
        return RequestRepository(await self.context.pgDb())

    async def buildResponseRepository(self) -> ResponseRepository:
        return ResponseRepository(await self.context.pgDb())
