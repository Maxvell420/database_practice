import asyncio
from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator
from src.libs.infra.demon import Demon
from src.libs.infra.logger import Logger
from src.domain.messengers.facadeDemon import FacadeDemon

# переделать на DI
allocator = Allocator()
context = Context(allocator)


class VkDemon(Demon):
    def __init__(self, context: Context, logger: Logger):
        super().__init__(context, logger)
        self.facadeDemon = FacadeDemon(context)

    async def job(self) -> None:
        await self.facadeDemon.job()

    async def load(self) -> None:
        await self.facadeDemon.load()


def main():
    demon = VkDemon(context, context.logger())
    asyncio.run(demon.run())


main()
