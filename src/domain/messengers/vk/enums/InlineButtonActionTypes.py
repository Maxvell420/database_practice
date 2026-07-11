from enum import Enum


class InlineButtonActionTypes(Enum):
    TEXT = "text"
    LOCATION = "location"
    VKPAY = "vkpay"
    OPEN_LINK = "open_link"
    OPEN_APP = "open_app"
    CALLBACK = "callback"
