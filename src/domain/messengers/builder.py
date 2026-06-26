from src.domain.messengers.repositories.requestRepository import RequestRepository
from src.domain.messengers.repositories.responseRepository import ResponseRepository
from src.libs.vk.client import Client as VKClient
from src.libs.infra.logger import Logger
from src.domain.messengers.useCases.vkRunner import VKRunner
from src.libs.infra.context import Context
class Builder:

    def __init__(self, context: Context):
        self.context = context
    async def buildVKRunner(self, logger: Logger | None = None) -> VKRunner:
        return VKRunner(await self.buildRequestRepository(), await self.buildResponseRepository(), await self.buildVKClient(), logger)

    async def buildVKClient(self, logger: Logger | None = None) -> VKClient:
        return VKClient(self.context.secrets().vk.token, self.context.secrets().vk.group_id, logger)

    async def buildRequestRepository(self) -> RequestRepository:
        return RequestRepository(await self.context.pgDb())

    async def buildResponseRepository(self) -> ResponseRepository:
        return ResponseRepository(await self.context.pgDb())