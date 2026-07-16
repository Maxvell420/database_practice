from src.domain.messengers.repositories.responseRepository import ResponseRepository
from src.domain.messengers.vk.values.editMessage import EditMessage
from src.libs.infra.logger import Logger
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.libs.vk.client import Client as VKClient


class VkResponseService:
    def __init__(
        self,
        response_repository: ResponseRepository,
        vk_client: VKClient,
        logger: Logger | None = None,
    ):
        self.response_repository = response_repository
        self.logger = logger
        self.vk_client = vk_client

    async def registerSendMessage(self, response: SendMessage, request_id: int) -> int:
        return await self.response_repository.createResponse(
            messenger_type=MessangerTypes.VK.value,
            request_id=request_id,
            data=response.model_dump_json(),
            user_uuid=str(response.user_id),
        )

    async def registerMessageEdit(self, response: EditMessage, request_id: int) -> int:
        return await self.response_repository.createResponse(
            messenger_type=MessangerTypes.VK.value,
            request_id=request_id,
            data=response.model_dump_json(),
            user_uuid=str(response.user_id),
        )

    async def updateResponseUuid(self, response_id: int, uuid: str) -> None:
        await self.response_repository.updateResponseUuid(response_id, uuid)

    async def processSendMessage(self, response_id: int, response: SendMessage) -> None:
        client_response = await self.vk_client.sendMessage(
            response.user_id, response.text, response.keyboard
        )

        await self.response_repository.updateResponseUuid(
            response_id, str(client_response.response)
        )
