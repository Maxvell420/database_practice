from src.domain.messengers.repositories.stateRepository import StateRepository
from src.domain.messengers.vk.enums.commands import Commands
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.vk.values.sendMessage import SendMessage
from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)
from src.domain.messengers.vk.enums.InlineButtonActionTypes import (
    InlineButtonActionTypes,
)
from src.domain.messengers.vk.entities.payload import Payload
from src.domain.messengers.vk.enums.actions import Actions
from src.domain.messengers.vk.entities.inlineKeyboard import InlineKeyboard


class CommandsHandler:
    def __init__(
        self, state_repository: StateRepository, keyboard_builder: InlineKeyboardBuilder
    ):
        self.state_repository = state_repository
        self.keyboard_builder = keyboard_builder

    async def findCommand(self, text: str) -> Commands | None:
        for command in Commands:
            if command.value == text:
                return command
        return None

    async def handleCommand(self, command: Commands, user_uid: str) -> SendMessage:
        await self.state_repository.deleteStates(user_uid, MessangerTypes.VK)
        if command == Commands.START:
            return await self.handleStart(user_uid)
        else:
            raise ValueError(f"Unknown command: {command}")

    async def handleStart(self, user_uid: str) -> SendMessage:
        keyboard = await self.getStartKeyboard()

        return SendMessage(
            text="Привет это очень большой текст",
            user_uid=user_uid,
            keyboard=keyboard,
        )

    async def getStartKeyboard(self) -> InlineKeyboard:
        button_1 = await self.keyboard_builder.buildInlineButton(
            type=InlineButtonActionTypes.CALLBACK,
            label="Искать радиацию",
            payload=Payload(action=Actions.SEARCH_RADIATION),
        )

        await self.keyboard_builder.addButtonToRow(button_1)
        await self.keyboard_builder.addRowToKeyboard()
        return await self.keyboard_builder.buildInlineKeyboard()
