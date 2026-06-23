from src.libs.infra.context import Context
from src.domain.map.builder import Builder
from src.libs.vk.client import Client as VKClient
from src.libs.nasapower.client import Client as NasaPowerClient
from src.libs.nspd.client import Client as NspdClient
from src.domain.map.repositories.nasaPowerRepository import NasaPowerRepository
from src.libs.vk.vkLogger import VKLogger
import os
class Facade:

    # TODO вытаскивать константу из контекста
    # Фасад хранит обьекты клиентов и репозиториев, которые он создает, плохо ли это?
    def __init__(self, context: Context):
        self.context = context
        self.builder = Builder()
        self.vkClient : VKClient | None = None
        self.nasaPowerClient : NasaPowerClient | None = None
        self.nspdClient : NspdClient | None = None
        self.nasaPowerRepository : NasaPowerRepository | None = None    

    async def buildVKClient(self) -> VKClient:
        if self.vkClient is None:
            logger = self.builder.buildVkLogger(self.context.allocator.getLogPath())
            self.vkClient = self.builder.buildVKClient(self.context.secrets().vk.token, self.context.secrets().vk.group_id, logger)
        return self.vkClient

    async def buildNasaPowerClient(self) -> NasaPowerClient:
        if self.nasaPowerClient is None:
            logger = self.builder.buildVkLogger(self.context.allocator.getLogPath())
            self.nasaPowerClient = self.builder.buildNasaPowerClient(logger)
        return self.nasaPowerClient

    async def buildNspdClient(self) -> NspdClient:
        if self.nspdClient is None:
            logger = self.builder.buildVkLogger(self.context.allocator.getLogPath())
            self.nspdClient = self.builder.buildNspdClient(logger)
        return self.nspdClient

    async def buildNasaPowerRepository(self) -> NasaPowerRepository:
        if self.nasaPowerRepository is None:
            self.nasaPowerRepository = self.builder.buildNasaPowerRepository(await self.context.pgDb())
        return self.nasaPowerRepository