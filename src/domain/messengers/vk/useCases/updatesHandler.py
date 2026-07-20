from src.domain.messengers.vk.enums.commands import Commands
from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)
from src.domain.messengers.vk.enums.InlineButtonActionTypes import (
    InlineButtonActionTypes,
)
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.values.editMessage import EditMessage
from src.domain.messengers.repositories.responseRepository import ResponseRepository
from src.domain.messengers.vk.entities.payload import Payload
from src.domain.messengers.vk.enums.actions import Actions
from src.domain.messengers.vk.values.editMessage import EditMessage
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.vk.entities.inlineKeyboard import InlineKeyboard
from src.domain.messengers.repositories.stateRepository import StateRepository
from src.domain.messengers.models.state import State
from src.domain.messengers.enums.states import States


class UpdatesHandler:
    def __init__(
        self,
        keyboard_builder: InlineKeyboardBuilder,
        response_repository: ResponseRepository,
        state_repository: StateRepository,
    ):
        self.keyboard_builder = keyboard_builder
        self.response_repository = response_repository
        self.state_repository = state_repository

    async def handleNewMessage(self, text: str, user_uid: int) -> SendMessage:
        for command in Commands:
            if text == command.value:
                return await self.handleCommand(command, user_uid)

        state = await self.state_repository.findState(str(user_uid), MessangerTypes.VK)
        if not (state is None):
            pass

        return SendMessage(text="Текст заглушка", user_id=user_uid, keyboard=None)

    async def handleStateUpdate(
        self, state: State, text: str, user_uid: str
    ) -> SendMessage:
        if state.state == States.SEARCH_RADIATION:
            return SendMessage(
                text="Это сообщение от стейта", user_id=user_uid, keyboard=None
            )

        else:
            raise ValueError(f"Unknown state: {state.state}")

    async def handleCommand(self, command: Commands, user_uid: str) -> SendMessage:
        if command == Commands.START:
            return await self.handleStart(user_uid)
        else:
            raise ValueError(f"Unknown command: {command}")

    async def handleMessageEvent(
        self, payload: Payload, user_uid: str, message_uid: int
    ) -> object:

        if payload.action == Actions.SEARCH_RADIATION:
            return await self.handleSearchRadiation(user_uid, message_uid)
        else:
            raise ValueError(f"Unknown action: {payload.action}")

        raise ValueError(f"Unknown payload: {payload}")

    async def handleSearchRadiation(
        self, user_uid: int, response_uid: int
    ) -> EditMessage:
        response = EditMessage(
            text="Введите адрес по которому будет проводиться поиск солнечной радиации",
            peer_id=user_uid,
            message_id=response_uid,
        )
        state = State(
            id=None,
            user_id=user_uid,
            state=States.SEARCH_RADIATION,
            messenger_type=MessangerTypes.VK,
        )
        await self.state_repository.persit(state)
        return response

    async def getStartKeyboard(self) -> InlineKeyboard:
        button_1 = await self.keyboard_builder.buildInlineButton(
            type=InlineButtonActionTypes.CALLBACK,
            label="Искать радиацию",
            payload=Payload(action=Actions.SEARCH_RADIATION),
        )

        await self.keyboard_builder.addButtonToRow(button_1)
        await self.keyboard_builder.addRowToKeyboard()
        return await self.keyboard_builder.buildInlineKeyboard()

    async def handleStart(self, user_uid: str) -> SendMessage:
        keyboard = await self.getStartKeyboard()

        return SendMessage(
            text="Привет это очень большой текст",
            user_id=int(user_uid),
            keyboard=keyboard,
        )
