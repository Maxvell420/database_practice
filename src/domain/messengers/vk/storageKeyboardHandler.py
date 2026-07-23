from src.domain.messengers.vk.useCases.InlineKeyboardBuilder import (
    InlineKeyboardBuilder,
)
from src.domain.messengers.vk.enums.InlineButtonActionTypes import (
    InlineButtonActionTypes,
)
from src.domain.messengers.vk.entities.payload import Payload
from src.domain.messengers.vk.enums.actions import Actions
from src.domain.messengers.vk.entities.inlineKeyboard import InlineKeyboard
from src.domain.messengers.vk.entities.storageItem import StorageItem
from src.domain.messengers.vk.enums.storageItemTypes import StorageItemTypes

VK_LIMIT_ROW = 5


class StorageKeyboardHandler:
    def __init__(self, keyboard_builder: InlineKeyboardBuilder):
        self.keyboard_builder = keyboard_builder

    # TODO: как-то чувствуется что это не должно быть так
    def getActionByType(self, type: StorageItemTypes) -> Actions:
        if type == StorageItemTypes.VK_NPSD:
            return Actions.SEARCH_RADIATION
        else:
            raise ValueError(f"Unknown type: {type}")

    def address(self, text: str | None, address: str) -> str:
        if text is None:
            return address
        return f"{text}\n{address}"

    async def buildKeyboard(
        self, items: list[StorageItem], page: int = 0
    ) -> tuple[InlineKeyboard, str | None]:
        total_pages = max(1, (len(items) + VK_LIMIT_ROW - 1) // VK_LIMIT_ROW)
        page = max(0, min(page, total_pages - 1))

        start = page * VK_LIMIT_ROW
        page_items = items[start : start + VK_LIMIT_ROW]

        text: str | None = None
        for index, item in enumerate(page_items, start=start + 1):
            action = self.getActionByType(item.type)
            address, coordinates = await self.getItemData(item)
            button = await self.keyboard_builder.buildInlineButton(
                type=InlineButtonActionTypes.CALLBACK,
                label=str(index),
                payload=Payload(action=action, value=str(coordinates)),
            )
            await self.keyboard_builder.addButtonToRow(button)
            await self.keyboard_builder.addRowToKeyboard()
            text = self.address(text, f"{index}. {address}")

        if total_pages > 1:
            if page > 0:
                prev_button = await self.keyboard_builder.buildInlineButton(
                    type=InlineButtonActionTypes.CALLBACK,
                    label="◀",
                    payload=Payload(action=Actions.PAGE_MOVE, value=str(page - 1)),
                )
                await self.keyboard_builder.addButtonToRow(prev_button)

            if page < total_pages - 1:
                next_button = await self.keyboard_builder.buildInlineButton(
                    type=InlineButtonActionTypes.CALLBACK,
                    label="▶",
                    payload=Payload(action=Actions.PAGE_MOVE, value=str(page + 1)),
                )
                await self.keyboard_builder.addButtonToRow(next_button)

            await self.keyboard_builder.addRowToKeyboard()

        keyboard = await self.keyboard_builder.buildInlineKeyboard()
        return keyboard, text

    async def buildAllPages(
        self, items: list[StorageItem]
    ) -> list[tuple[InlineKeyboard, str | None]]:
        total_pages = max(1, (len(items) + VK_LIMIT_ROW - 1) // VK_LIMIT_ROW)
        return [
            await self.buildKeyboard(items, page=page) for page in range(total_pages)
        ]

    async def getItemData(self, item: StorageItem) -> tuple[str, str]:
        if item.type == StorageItemTypes.VK_NPSD:
            return item.data["address"], item.data["coordinates"]
        else:
            raise ValueError(f"Unknown type: {item.type}")
