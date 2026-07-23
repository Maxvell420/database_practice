from src.domain.messengers.vk.entities.storageItem import StorageItem
from src.domain.messengers.enums.messangerTypes import MessangerTypes
from src.domain.messengers.vk.enums.storageItemTypes import StorageItemTypes
from src.domain.map.values.building import Building


class InlineStorage:
    def __init__(self):
        self.vk_storage: dict[int, dict[int, list[StorageItem]]] = {}

    async def getStorageItems(
        self, messenger_type: MessangerTypes, message_uid: int
    ) -> list[StorageItem]:
        if messenger_type == MessangerTypes.VK:
            items = self.vk_storage.get(messenger_type.value, {}).get(message_uid)
            # обработать ошибку если item не найден
            if items is None:
                raise ValueError(
                    f"Storage item not found for message_uid: {message_uid}"
                )
            return items
        raise ValueError(f"Messenger type not supported: {messenger_type}")

    # TODO: message_uid это str?
    async def storeBuildings(
        self, message_uid: int, buildings: list[Building]
    ) -> list[StorageItem]:
        items = []
        for building in buildings:
            item = StorageItem.model_validate(
                {
                    "type": StorageItemTypes.VK_NPSD,
                    "data": {
                        "address": building.address,
                        "coordinates": building.coordinates,
                    },
                }
            )

            items.append(item)

        await self.placeItemsInStorage(MessangerTypes.VK, message_uid, items)

        return items

    async def placeItemsInStorage(
        self, messenger_type: MessangerTypes, message_uid: int, items: list[StorageItem]
    ) -> None:
        self.vk_storage.setdefault(messenger_type.value, {})[message_uid] = items
