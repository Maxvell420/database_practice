from .allocator import Allocator
from .secrets import Secrets
from asyncpg.pool import Pool

class Context:

    def __init__(self, allocator: Allocator):
        self.allocator = allocator
    
    def secrets(self) -> Secrets:
        return self.allocator.secrets()
    
    async def pgDb(self) -> Pool:
        return await self.allocator.pgDbPool()