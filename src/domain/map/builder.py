from src.libs.vk.client import Client as VKClient
from src.libs.infra.logger import Logger
from src.libs.nasapower.client import Client as NasaPowerClient
from src.domain.map.repositories.nasaPowerRepository import NasaPowerRepository
from src.libs.nspd.client import Client as NspdClient
from asyncpg.pool import Pool
from src.libs.vk.vkLogger import VKLogger
from src.libs.infra.context import Context


class Builder:

    def __init__(self, context: Context):
        self.context = context

    async def buildVKClient(self, logger: Logger | None = None) -> VKClient:
        return VKClient(
            self.context.secrets().vk.token, self.context.secrets().vk.group_id, logger
        )

    def buildNasaPowerClient(self, logger: Logger) -> NasaPowerClient:
        return NasaPowerClient(logger)

    def buildNspdClient(self, logger: Logger) -> NspdClient:
        return NspdClient(logger)

    async def buildNasaPowerRepository(self) -> NasaPowerRepository:
        return NasaPowerRepository(await self.context.pgDb())
