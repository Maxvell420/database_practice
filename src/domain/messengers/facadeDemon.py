from src.libs.infra.context import Context
from src.domain.messengers.builder import Builder


class FacadeDemon:
    def __init__(self, context: Context):
        self.context = context
        self.builder = Builder(context)
        self.vkRunner = None

    async def job(self) -> None:
        if self.vkRunner is None:
            raise Exception("VKRunner is not initialized")
        await self.vkRunner.job()

    async def load(self) -> None:
        self.vkRunner = await self.builder.buildVKRunner(self.context.logger())

        await self.vkRunner.load()
