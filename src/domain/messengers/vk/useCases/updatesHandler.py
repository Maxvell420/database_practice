from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.values.editMessage import EditMessage
from src.domain.messengers.vk.enums.actions import Actions
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.repositories.stateRepository import StateRepository
from src.domain.messengers.models.state import State
from src.domain.messengers.enums.states import States
from src.domain.messengers.vk.useCases.commandsHandler import CommandsHandler
from src.libs.vk.responses.update import Update
from src.libs.vk.enums.updateType import UpdateType
from src.domain.messengers.vk.values.vkPayload import VkPayload
from src.domain.messengers.vk.useCases.inlineStorage import InlineStorage
from src.domain.messengers.vk.storageKeyboardHandler import StorageKeyboardHandler
from src.libs.nspd.client import Client as NspdClient
from src.domain.map.facade import Facade as MapFacade


# Вот тут можно разбить обработку, но пока так
class UpdatesHandler:
    def __init__(
        self,
        keyboard_builder: InlineKeyboardBuilder,
        state_repository: StateRepository,
        commandsHandler: CommandsHandler,
        storageKeyboardHandler: StorageKeyboardHandler,
        inlineStorage: InlineStorage,
        nspdClient: NspdClient,
        mapFacade: MapFacade,
    ):
        self.keyboard_builder = keyboard_builder
        self.state_repository = state_repository
        self.commandsHandler = commandsHandler
        self.storageKeyboardHandler = storageKeyboardHandler
        self.inlineStorage = inlineStorage
        self.nspdClient = nspdClient
        self.mapFacade = mapFacade

    async def handleNewUpdate(self, update: Update) -> VkPayload:
        if update.type == UpdateType.MESSAGE_NEW:
            new_response = await self.handleNewMessage(update)
        elif update.type == UpdateType.MESSAGE_EVENT:
            new_response = await self.handleMessageEvent(update)
        else:
            raise ValueError(f"Unknown update type: {update.type}")

        return new_response

    async def handleNewMessage(self, update: Update) -> VkPayload:
        data = update.getMessageNewUpdate()
        command = await self.commandsHandler.findCommand(data.message.text)

        if not (command is None):
            await self.state_repository.deleteStates(
                str(data.message.from_id), MessangerTypes.VK
            )
            return await self.commandsHandler.handleCommand(
                command, str(data.message.from_id)
            )

        state = await self.state_repository.findState(
            str(data.message.from_id), MessangerTypes.VK
        )
        if not (state is None):
            return await self.handleStateUpdate(
                state, data.message.text, str(data.message.from_id)
            )

        return SendMessage(
            text="Текст заглушка", user_uid=str(data.message.from_id), keyboard=None
        )

    async def handleStateUpdate(
        self, state: State, text: str, user_uid: str
    ) -> EditMessage:
        if state.state == States.SEARCH_RADIATION:
            if state.data is None:
                raise ValueError("Message UID is None")
            buildings = await self.mapFacade.listBuildings(text)
            items = await self.inlineStorage.storeBuildings(
                state.data["message_uid"], buildings
            )
            keyboard = await self.storageKeyboardHandler.buildAllPages(items)
            # TODO: подумать как обрабатывать если 0 результатов
            message = EditMessage(
                text="Выберите адрес для поиска радиации",
                user_uid=user_uid,
                keyboard=keyboard[0],
                message_id=state.data["message_uid"],
            )
        else:
            raise ValueError(f"Unknown state: {state.state}")
        await self.state_repository.deleteState(state)
        return message

    async def handleMessageEvent(self, update: Update) -> EditMessage:
        data = update.getMessageEventUpdate()

        if data.object.payload is None:
            raise ValueError("Payload is None")
        if data.object.user_id is None:
            raise ValueError("User ID is None")
        if data.object.conversation_message_id is None:
            raise ValueError("Conversation message ID is None")

        await self.state_repository.deleteStates(
            str(data.object.user_id), MessangerTypes.VK
        )
        if data.object.payload.action == Actions.SEARCH_RADIATION:
            return await self.handleSearchRadiation(
                str(data.object.user_id), data.object.conversation_message_id
            )
        elif data.object.payload.action == Actions.PAGE_MOVE:
            return await self.handlePageMove(
                str(data.object.user_id),
                data.object.conversation_message_id,
                int(data.object.payload.value or 0),
            )
        else:
            raise ValueError(f"Unknown action: {data.object.payload.action}")

    async def handlePageMove(
        self, user_uid: str, response_uid: int, page: int
    ) -> EditMessage:
        items = await self.inlineStorage.getStorageItems(
            MessangerTypes.VK, response_uid
        )
        keyboard = await self.storageKeyboardHandler.buildAllPages(items)
        return EditMessage(
            # что будет если не передать текст?
            text="Выберите адрес для поиска радиации",
            user_uid=user_uid,
            message_id=response_uid,
            keyboard=keyboard[page],
        )

    async def handleSearchRadiation(
        self, user_uid: str, response_uid: int
    ) -> EditMessage:
        response = EditMessage(
            text="Введите адрес по которому будет проводиться поиск солнечной радиации",
            user_uid=user_uid,
            message_id=response_uid,
        )
        state = State(
            id=None,
            user_uid=user_uid,
            state=States.SEARCH_RADIATION,
            messenger_type=MessangerTypes.VK,
            data={"message_uid": response_uid},
        )
        await self.state_repository.persit(state)
        return response
