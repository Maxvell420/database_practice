from pydantic import BaseModel
from src.domain.messengers.vk.enums.storageItemTypes import StorageItemTypes
from typing import Any


class StorageItem(BaseModel):
    type: StorageItemTypes
    data: Any
