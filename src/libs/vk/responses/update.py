from pydantic import BaseModel

from .object import Object
from src.libs.vk.enums.updateType import UpdateType
from src.libs.vk.responses.messageNew import MessageNew
from src.libs.vk.responses.messageEvent import MessageEvent


class Update(BaseModel):
    group_id: int
    type: UpdateType
    event_id: str
    v: str
    object: Object

    def getMessageNewUpdate(self) -> MessageNew:
        if self.object.message is None:
            raise ValueError("MESSAGE_NEW missing message")
        return MessageNew(
            group_id=self.group_id,
            event_id=self.event_id,
            v=self.v,
            type=self.type,
            object=self.object,
            message=self.object.message,
        )

    def getMessageEventUpdate(self) -> MessageEvent:
        return MessageEvent(
            group_id=self.group_id,
            event_id=self.event_id,
            v=self.v,
            type=self.type,
            object=self.object,
        )
