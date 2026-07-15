from src.domain.messengers.vk.enums.commands import Commands
from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)
from src.domain.messengers.vk.enums.InlineButtonActionTypes import (
    InlineButtonActionTypes,
)
from src.domain.messengers.vk.values.sendMessage import SendMessage


class UpdatesHandler:
    def __init__(self, keyboard_builder: InlineKeyboardBuilder):
        self.keyboard_builder = keyboard_builder

    async def handleNewMessage(self, text: str, user_uid: int) -> SendMessage:
        for command in Commands:
            if text == command.value:
                return await self.handleCommand(command, user_uid)
        return SendMessage(text="Текст заглушка", user_id=user_uid, keyboard=None)

    async def handleCommand(self, command: Commands, user_uid: int) -> SendMessage:
        if command == Commands.START:
            return await self.handleStart(user_uid)
        else:
            raise ValueError(f"Unknown command: {command}")

    async def handleStart(self, user_uid: int) -> SendMessage:
        button_1 = await self.keyboard_builder.buildInlineButton(
            type=InlineButtonActionTypes.CALLBACK, label="Привет"
        )
        button_2 = await self.keyboard_builder.buildInlineButton(
            type=InlineButtonActionTypes.CALLBACK, label="Пока"
        )

        await self.keyboard_builder.addButtonToRow(button_1)
        await self.keyboard_builder.addButtonToRow(button_2)
        await self.keyboard_builder.addRowToKeyboard()
        keyboard = await self.keyboard_builder.buildInlineKeyboard()

        return SendMessage(
            text="Привет это очень большой тескст", user_id=user_uid, keyboard=keyboard
        )
