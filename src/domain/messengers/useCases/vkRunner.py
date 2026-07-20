from src.libs.vk.client import Client as VKClient
from src.libs.vk.enums.updateType import UpdateType
from src.libs.vk.responses.update import Update
from src.libs.infra.logger import Logger
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.facade import Facade as VKFacade
from src.domain.messengers.useCases.VkUpdatesService import VkUpdatesService
from src.domain.messengers.useCases.VkResponseService import VkResponseService
from src.domain.messengers.vk.values.editMessage import EditMessage


# тут нужно сделать загрузку не обработанных запросов и ответов и обработку их если демон перезапустился
class VKRunner:
    def __init__(
        self,
        updates_service: VkUpdatesService,
        response_service: VkResponseService,
        vk_client: VKClient,
        vk_facade: VKFacade,
        logger: Logger | None = None,
    ):
        self.updates_service = updates_service
        self.response_service = response_service
        self.vk_client = vk_client
        self.logger: Logger | None = logger
        self.new_updates: dict[int, Update] = {}
        self.new_responses: dict[int, SendMessage | EditMessage] = {}
        self.vk_facade = vk_facade

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
            request_id = await self.updates_service.registerUpdate(update)
            self.new_updates[request_id] = update

    async def processNewUpdates(self):
        for request_id, update in list[tuple[int, Update]](self.new_updates.items()):
            # вот это вот вынести в отдельный обработчик
            if update.type == UpdateType.MESSAGE_NEW:
                message_new = update.getMessageNewUpdate()
                new_response = await self.vk_facade.handleNewMessage(
                    message_new.message.text,
                    message_new.message.from_id,
                )

                response_id = await self.response_service.registerSendMessage(
                    new_response, request_id
                )
                self.new_responses[response_id] = new_response
            elif update.type == UpdateType.MESSAGE_EVENT:
                message_event = update.getMessageEventUpdate()
                if message_event.object.payload is None:
                    raise ValueError("Payload is None")
                if message_event.object.user_id is None:
                    raise ValueError("User ID is None")
                if message_event.object.conversation_message_id is None:
                    raise ValueError("Conversation message ID is None")
                new_response = await self.vk_facade.handleMessageEvent(
                    message_event.object.payload,
                    message_event.object.user_id,
                    message_event.object.conversation_message_id,
                )

                if isinstance(new_response, EditMessage):
                    response_id = await self.response_service.registerMessageEdit(
                        new_response, request_id
                    )
                    self.new_responses[response_id] = new_response
                else:
                    raise ValueError("Unknown response type")
            self.new_updates.pop(request_id)

    async def processNewResponses(self):
        for response_id, response in list[tuple[int, object]](
            self.new_responses.items()
        ):

            # возможно тут стоит завести тип отдельный для всех responses и не вызывать методы для каждого типа
            if isinstance(response, SendMessage):
                await self.response_service.processSendMessage(response_id, response)

            elif isinstance(response, EditMessage):
                await self.response_service.processMessageEdit(response)

            self.new_responses.pop(response_id)
