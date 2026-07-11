from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator
from src.domain.messengers.facade import Facade
import asyncio
# переделать на DI
allocator = Allocator()
context = Context(allocator)
class Demon:

    receivedUpdates = []
    readyToSendResponses = []
    def __init__(self, context: Context):
        self.context = context

    async def run(self):
        facade = Facade(self.context)
        await facade.runVkRunner()

def main():
    demon = Demon(context)
    asyncio.run(demon.run())

main()