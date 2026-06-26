from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator
from src.libs.vk.client import Client as VKClient
import os
from src.libs.vk.vkLogger import VKLogger
from src.domain.messengers.facade import Facade
import asyncio
# переделать на DI
allocator = Allocator()
context = Context(allocator)
logger = VKLogger(allocator.getLogPath())
class Demon:

    receivedUpdates = []
    readyToSendResponses = []
    def __init__(self, context: Context):
        self.context = context
        self.vkClient = VKClient(context.secrets().vk.token, context.secrets().vk.group_id, logger)

    async def run(self):
        facade = Facade(self.context)
        await facade.runVkRunner()

def main():
    demon = Demon(context)
    asyncio.run(demon.run())

main()