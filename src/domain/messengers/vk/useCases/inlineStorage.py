from src.domain.messengers.vk.entities.storageItem import StorageItem
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.vk.enums.storageItemTypes import StorageItemTypes


class InlineStorage:
    def __init__(self):
        self.vk_storage: dict[int, dict[int, StorageItem]] = {}

    async def getStorageItem(
        self, messenger_type: MessangerTypes, message_uid: int
    ) -> StorageItem:
        if messenger_type == MessangerTypes.VK:
            item = self.vk_storage.get(messenger_type.value, {}).get(message_uid)
            # обработать ошибку если item не найден
            if item is None:
                raise ValueError(
                    f"Storage item not found for message_uid: {message_uid}"
                )
            return item
        raise ValueError(f"Messenger type not supported: {messenger_type}")

    async def listTestItem(self) -> list[StorageItem]:
        return [
            StorageItem.model_validate(
                {
                    "type": StorageItemTypes.VK_NPSD,
                    "data": "test",
                }
            ),
            StorageItem.model_validate(
                {
                    "type": StorageItemTypes.VK_NPSD,
                    "data": "test2",
                }
            ),
            StorageItem.model_validate(
                {
                    "type": StorageItemTypes.VK_NPSD,
                    "data": "test3",
                }
            ),
            StorageItem.model_validate(
                {
                    "type": StorageItemTypes.VK_NPSD,
                    "data": "test4",
                }
            ),
            StorageItem.model_validate(
                {
                    "type": StorageItemTypes.VK_NPSD,
                    "data": "test5",
                }
            ),
        ]
