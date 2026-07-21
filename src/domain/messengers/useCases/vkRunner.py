from src.libs.vk.client import Client as VKClient
from src.libs.vk.responses.update import Update
from src.libs.infra.logger import Logger
from src.domain.messengers.vk.facade import Facade as VKFacade
from src.domain.messengers.useCases.VkUpdatesService import VkUpdatesService
from src.domain.messengers.vk.values.vkPayload import VkPayload
from src.domain.messengers.useCases.vkResponseService import VkResponseService


# тут нужно сделать загрузку не обработанных запросов и обработку их если демон перезапустился
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
        self.new_responses: list[VkPayload] = []
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
            if request_id is None:
                continue
            self.new_updates[request_id] = update

    async def processNewUpdates(self):
        for request_id, update in list[tuple[int, Update]](self.new_updates.items()):
            # вот это вот вынести в отдельный обработчик
            response = await self.vk_facade.handleNewUpdate(update)
            self.new_responses.append(response)
            self.new_updates.pop(request_id)

    async def processNewResponses(self):
        for response in self.new_responses:
            await self.response_service.registerVkResponse(response)
            self.new_responses.remove(response)
