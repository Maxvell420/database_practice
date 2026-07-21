from src.domain.messengers.repositories.requestRepository import RequestRepository
from src.libs.vk.client import Client as VKClient
from src.libs.infra.logger import Logger
from src.domain.messengers.useCases.vkRunner import VKRunner
from src.libs.infra.context import Context
from src.domain.messengers.useCases.VkUpdatesService import VkUpdatesService
from src.domain.messengers.useCases.vkResponseService import VkResponseService
from src.domain.messengers.vk.facade import Facade as VKFacade


class Builder:

    def __init__(self, context: Context):
        self.context = context

    async def buildVKRunner(self, logger: Logger | None = None) -> VKRunner:
        return VKRunner(
            await self.buildVkUpdatesService(logger=logger),
            await self.buildVkResponseService(logger=logger),
            await self.buildVKClient(logger=logger),
            await self.buildVKFacade(logger=logger),
        )

    async def buildVkUpdatesService(
        self, logger: Logger | None = None
    ) -> VkUpdatesService:
        return VkUpdatesService(
            await self.buildRequestRepository(),
            await self.buildVKClient(logger=logger),
            logger,
        )

    async def buildVKFacade(self, logger: Logger | None = None) -> VKFacade:
        return VKFacade(self.context, logger)

    async def buildVkResponseService(
        self, logger: Logger | None = None
    ) -> VkResponseService:
        return VkResponseService(
            await self.buildVKClient(logger),
            logger,
        )

    async def buildVKClient(self, logger: Logger | None = None) -> VKClient:
        return VKClient(
            self.context.secrets().vk.token, self.context.secrets().vk.group_id, logger
        )

    async def buildRequestRepository(self) -> RequestRepository:
        return RequestRepository(await self.context.pgDb())
