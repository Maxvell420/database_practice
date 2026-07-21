from src.domain.messengers.vk.values.editMessage import EditMessage
from src.domain.messengers.vk.values.vkPayload import VkPayload
from src.libs.infra.logger import Logger
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.libs.vk.client import Client as VKClient


class VkResponseService:
    def __init__(
        self,
        vk_client: VKClient,
        logger: Logger | None = None,
    ):
        self.logger = logger
        self.vk_client = vk_client

    # возможно тут будет ретрай
    async def registerVkResponse(self, response: VkPayload) -> None:
        if isinstance(response, SendMessage):
            await self.processSendMessage(response)
        elif isinstance(response, EditMessage):
            await self.processMessageEdit(response)
        else:
            raise ValueError(f"Unknown response type: {type(response)}")

    async def processSendMessage(self, response: SendMessage) -> None:
        await self.vk_client.sendMessage(
            response.user_uid, response.text, response.keyboard
        )

    async def processMessageEdit(self, response: EditMessage) -> None:
        await self.vk_client.editMessage(
            response.user_uid, response.text, response.message_id, response.keyboard
        )
