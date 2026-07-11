from .allocator import Allocator
from .secrets import Secrets
from asyncpg.pool import Pool
from src.libs.infra.logger import Logger
from src.libs.vk.vkLogger import VKLogger
class Context:

    def __init__(self, allocator: Allocator):
        self.allocator = allocator
    
    def secrets(self) -> Secrets:
        return self.allocator.secrets()
    
    async def pgDb(self) -> Pool:
        return await self.allocator.pgDbPool()

    async def logger(self) -> Logger:
        # TODO сделать другой логгер
        return VKLogger(self.allocator.getLogPath())