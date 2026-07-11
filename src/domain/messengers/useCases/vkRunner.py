from src.domain.messengers.repositories.requestRepository import RequestRepository
from src.domain.messengers.repositories.responseRepository import ResponseRepository
from src.libs.vk.client import Client as VKClient
from src.libs.vk.enums.updateType import UpdateType
from src.libs.vk.responses.update import Update
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.libs.infra.logger import Logger
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.facade import Facade as VKFacade


# тут нужно сделать загрузку не обработанных запросов и ответов и обработку их если демон перезапустился
class VKRunner:
    def __init__(
        self,
        request_repository: RequestRepository,
        response_repository: ResponseRepository,
        vk_client: VKClient,
        logger: Logger | None = None,
    ):
        self.request_repository = request_repository
        self.response_repository = response_repository
        self.vk_client = vk_client
        self.logger: Logger | None = logger
        self.new_updates: dict[int, Update] = {}
        self.new_responses: dict[int, SendMessage] = {}
        self.vk_facade = VKFacade(logger)

    # получаю новые обновления в первом действии
    # обрабатываю их во втором действии и сохраняю на отправку
    # отправляю ответы в третьем действии
    async def run(self):
        while True:
            await self.getNewUpdates()
            await self.processNewUpdates()
            await self.processNewResponses()

    async def getNewUpdates(self):
        # тут прокинуть время longpoll
        updates = await self.vk_client.getUpdates()
        for update in updates:
            request_id = await self.request_repository.createRequest(
                messenger_type=MessangerTypes.VK.value,
                data=update.model_dump_json(),
                user_uuid=str(update.object.message.from_id),
                request_uuid=update.event_id,
            )
            self.new_updates[request_id] = update

    async def processNewUpdates(self):
        for request_id, update in list[tuple[int, Update]](self.new_updates.items()):
            if update.type == UpdateType.MESSAGE_NEW:
                message = update.object.message

                new_response = await self.vk_facade.handleNewMessage(
                    message.text, message.from_id
                )

                response_id = await self.response_repository.createResponse(
                    messenger_type=MessangerTypes.VK.value,
                    request_id=request_id,
                    data=new_response.model_dump_json(),
                    user_uuid=str(update.object.message.from_id),
                )
                self.new_responses[response_id] = new_response

            self.new_updates.pop(request_id)

    async def processNewResponses(self):
        for response_id, response in list[tuple[int, SendMessage]](
            self.new_responses.items()
        ):
            client_response = await self.vk_client.sendMessage(
                response.user_id, response.text, response.keyboard
            )
            await self.response_repository.updateResponseUuid(
                response_id, str(client_response.response)
            )
            self.new_responses.pop(response_id)
