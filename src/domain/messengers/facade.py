from src.libs.infra.context import Context
from src.domain.messengers.builder import Builder

class Facade:
    def __init__(self, context: Context):
        self.context = context
        self.builder = Builder(context)

    async def runVkRunner(self) -> None:
        vkRunner = await self.builder.buildVKRunner(await self.context.logger())
        await vkRunner.run()
