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
from src.domain.messengers.models.response import Response
from src.domain.messengers.vk.entities.payload import Payload
from src.domain.messengers.vk.enums.actions import Actions


class UpdatesHandler:
    def __init__(
        self,
        keyboard_builder: InlineKeyboardBuilder,
        response_repository: ResponseRepository,
    ):
        self.keyboard_builder = keyboard_builder
        self.response_repository = response_repository

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

    async def handleMessageEvent(
        self, payload: Payload, user_uid: int, message_uid: int
    ) -> object:

        if payload.action == Actions.SEARCH_RADIATION:
            pass
        else:
            raise ValueError(f"Unknown action: {payload.action}")

        if payload == "":
            response = await self.response_repository.getResponseByUuid(
                str(message_uid)
            )
            return EditMessage(text="Текст заглушка", user_id=user_uid)
        raise ValueError(f"Unknown payload: {payload}")

    async def handleStart(self, user_uid: int) -> SendMessage:
        button_1 = await self.keyboard_builder.buildInlineButton(
            type=InlineButtonActionTypes.CALLBACK,
            label="Искать радиацию",
            payload=Payload(action=Actions.SEARCH_RADIATION),
        )

        await self.keyboard_builder.addButtonToRow(button_1)
        await self.keyboard_builder.addRowToKeyboard()
        keyboard = await self.keyboard_builder.buildInlineKeyboard()

        return SendMessage(
            text="Привет это очень большой тескст", user_id=user_uid, keyboard=keyboard
        )

    async def getHideKeyboardResponse(self, Response: Response) -> EditMessage:
        data = Response.data
        data["keyboard"] = None

        return EditMessage.model_validate(data)
