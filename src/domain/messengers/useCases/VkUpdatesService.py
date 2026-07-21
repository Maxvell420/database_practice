from src.domain.messengers.repositories.requestRepository import RequestRepository
from src.libs.vk.responses.update import Update
from src.libs.vk.enums.updateType import UpdateType
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.libs.infra.logger import Logger
from src.domain.messengers.models.request import Request
from src.libs.vk.client import Client as VKClient
import json


class VkUpdatesService:
    def __init__(
        self,
        request_repository: RequestRepository,
        client: VKClient,
        logger: Logger | None = None,
    ):
        self.request_repository = request_repository
        self.client = client
        self.logger = logger

    async def getNewUpdates(self) -> dict[int, Update]:
        updates = await self.client.getUpdates()
        new_updates: dict[int, Update] = {}

        for update in updates:
            request_id = await self.registerUpdate(update)
            if request_id is None:
                continue
            new_updates[request_id] = update
        return new_updates

    async def getUnprocessedUpdates(self) -> dict[int, Update]:
        requests = await self.request_repository.listUnprocessedRequests()
        unprocessed_updates: dict[int, Update] = {}
        for request in requests:
            update = Update.model_validate_json(json.dumps(request.data))
            unprocessed_updates[request.id] = update
        return unprocessed_updates

    async def registerUpdate(self, update: Update) -> int | None:
        request_id = None
        if update.type == UpdateType.MESSAGE_NEW:
            message_new = update.getMessageNewUpdate()
            request_id = await self.request_repository.createRequest(
                messenger_type=MessangerTypes.VK.value,
                data=update.model_dump_json(),
                user_uuid=str(message_new.message.from_id),
                request_uuid=str(message_new.message.id),
            )
        elif update.type == UpdateType.MESSAGE_EVENT:
            message_event = update.getMessageEventUpdate()
            request_id = await self.request_repository.createRequest(
                messenger_type=MessangerTypes.VK.value,
                data=update.model_dump_json(),
                user_uuid=str(message_event.object.user_id),
                request_uuid=update.event_id,
            )
        elif update.type == UpdateType.MESSAGE_EDIT:
            # я не понимаю почему это приходит, но пока пусть будет так
            return None
        else:
            if self.logger is not None:
                await self.logger.error(f"Update type: {update.type} is not supported")
            raise ValueError(f"Update type: {update.type} is not supported")

        if request_id is None:
            if self.logger is not None:
                await self.logger.error(f"Request id is not found")
            raise ValueError(f"Request id is not found")
        return request_id

    # TODO: если не нашел запрос, то вероятно нужно прятать сообщение
    async def getRequestByUuid(self, request_uuid: str) -> Request:
        return await self.request_repository.getRequestByUuid(
            request_uuid, MessangerTypes.VK
        )
