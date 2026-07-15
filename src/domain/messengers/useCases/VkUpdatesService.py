from src.domain.messengers.repositories.requestRepository import RequestRepository
from src.libs.vk.responses.update import Update
from src.libs.vk.enums.updateType import UpdateType
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.libs.infra.logger import Logger


class VkUpdatesService:
    def __init__(
        self, request_repository: RequestRepository, logger: Logger | None = None
    ):
        self.request_repository = request_repository
        self.logger = logger

    async def registerUpdate(self, update: Update) -> int:
        request_id = None
        if update.type == UpdateType.MESSAGE_NEW:
            if update.object.message is None:
                if self.logger is not None:
                    await self.logger.error(
                        f"Update type: {update.type} has no message"
                    )
                raise ValueError(f"Update type: {update.type} has no from_id")
            request_id = await self.request_repository.createRequest(
                messenger_type=MessangerTypes.VK.value,
                data=update.model_dump_json(),
                user_uuid=str(update.object.message.from_id),
                request_uuid=update.event_id,
            )
        elif update.type == UpdateType.MESSAGE_EVENT:
            request_id = await self.request_repository.createRequest(
                messenger_type=MessangerTypes.VK.value,
                data=update.model_dump_json(),
                user_uuid=str(update.object.user_id),
                request_uuid=update.event_id,
            )
        else:
            if self.logger is not None:
                await self.logger.error(f"Update type: {update.type} is not supported")
            raise ValueError(f"Update type: {update.type} is not supported")

        if request_id is None:
            if self.logger is not None:
                await self.logger.error(f"Request id is not found")
            raise ValueError(f"Request id is not found")
        return request_id
