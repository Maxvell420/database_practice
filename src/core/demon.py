from src.libs.infra.context import Context
from src.libs.infra.allocator import Allocator
from src.libs.vk.client import Client as VKClient
import os
from src.libs.vk.vkLogger import VKLogger
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
        pass
        # while True:
        #     updates = await self.vkClient.getUpdates()
        #     if updates.isOk():
        #         for update in updates.data['updates']:
        #             if update['type'] == 'message_new':
        #                 message = update['message']
        #                 await self.vkClient.sendMessage(message['from_id'], message['text'])
