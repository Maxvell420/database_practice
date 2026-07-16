from src.domain.messengers.vk.entities.inlineKeyboardButton import InlineKeyboardButton
from src.domain.messengers.vk.entities.inlineKeyboardButtonAction import (
    InlineKeyboardButtonAction,
)
from src.domain.messengers.vk.enums.InlineButtonActionTypes import (
    InlineButtonActionTypes,
)
from src.domain.messengers.vk.entities.inlineKeyboard import InlineKeyboard
from src.domain.messengers.vk.entities.payload import Payload


class InlineKeyboardBuilder:
    def __init__(self):
        self.keyboard: list[list[InlineKeyboardButton]] = []
        self.row: list[InlineKeyboardButton] = []

    async def addButtonToRow(self, button: InlineKeyboardButton) -> None:
        self.row.append(button)

    async def addRowToKeyboard(self) -> None:
        if not self.row:
            raise ValueError("Row is empty")
        self.keyboard.append(self.row)
        self.row = []

    async def addDataToRow(self, data: InlineKeyboardButton) -> None:
        self.row.append(data)

    async def buildInlineButton(
        self,
        type: InlineButtonActionTypes,
        label: None | str = None,
        url: None | str = None,
        link: None | str = None,
        app_id: None | int = None,
        owner_id: None | int = None,
        hash: None | str = None,
        color: None | str = None,
        payload: None | Payload = None,
    ) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            action=InlineKeyboardButtonAction(
                type=type,
                label=label,
                url=url,
                link=link,
                app_id=app_id,
                owner_id=owner_id,
                hash=hash,
                payload=payload.model_dump_json() if payload else None,
            ),
            color=color,
        )

    async def buildInlineKeyboard(self) -> InlineKeyboard:
        keyboard = InlineKeyboard(buttons=self.keyboard, inline=True)
        await self.resetKeyboard()
        return keyboard

    async def resetKeyboard(self) -> None:
        self.keyboard = []
        self.row = []
