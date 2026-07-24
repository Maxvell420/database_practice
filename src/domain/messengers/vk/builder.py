from src.libs.infra.logger import Logger
from src.domain.messengers.vk.useCases.updatesHandler import UpdatesHandler
from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)
from src.domain.messengers.repositories.requestRepository import RequestRepository
from src.libs.infra.context import Context
from src.domain.messengers.repositories.stateRepository import StateRepository
from src.domain.messengers.vk.useCases.commandsHandler import CommandsHandler
from src.domain.messengers.vk.useCases.inlineStorage import InlineStorage
from src.domain.messengers.vk.useCases.storageKeyboardHandler import (
    StorageKeyboardHandler,
)
from src.libs.nspd.client import Client as NspdClient
from src.domain.map.facade import Facade as MapFacade


class Builder:
    def __init__(self, context: Context, logger: Logger | None = None):
        self.logger = logger
        self.context = context
        # TODO: подумать насчет состояний, возможно UpdatesHandler не надо создавать каждый раз
        self.inlineStorage = None

    async def buildUpdatesHandler(self) -> UpdatesHandler:
        return UpdatesHandler(
            await self.buildInlineKeyboardBuilder(),
            await self.buildStateRepository(),
            await self.buildCommandsHandler(),
            await self.buildStorageKeyboardHandler(),
            await self.buildInlineStorage(),
            await self.buildNspdClient(),
            await self.buildMapFacade(),
        )

    async def buildMapFacade(self) -> MapFacade:
        return MapFacade(self.context)

    # TODO: подумать...
    async def buildInlineStorage(self) -> InlineStorage:
        if self.inlineStorage is None:
            self.inlineStorage = InlineStorage()
        return self.inlineStorage

    async def buildNspdClient(self) -> NspdClient:
        return NspdClient(self.context.logger())

    async def buildCommandsHandler(self) -> CommandsHandler:
        return CommandsHandler(
            await self.buildStateRepository(), await self.buildInlineKeyboardBuilder()
        )

    async def buildStorageKeyboardHandler(self) -> StorageKeyboardHandler:
        return StorageKeyboardHandler(await self.buildInlineKeyboardBuilder())

    async def buildInlineKeyboardBuilder(self) -> InlineKeyboardBuilder:
        return InlineKeyboardBuilder()

    async def buildRequestRepository(self) -> RequestRepository:
        return RequestRepository(await self.context.pgDb())

    async def buildStateRepository(self) -> StateRepository:
        return StateRepository(await self.context.pgDb())
