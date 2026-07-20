from enum import Enum


class UpdateType(Enum):
    MESSAGE_NEW = "message_new"
    MESSAGE_EVENT = "message_event"
    MESSAGE_EDIT = "message_edit"
