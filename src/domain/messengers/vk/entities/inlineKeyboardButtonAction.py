from pydantic import BaseModel, model_validator
from src.domain.messengers.vk.enums.InlineButtonActionTypes import (
    InlineButtonActionTypes,
)


class InlineKeyboardButtonAction(BaseModel):
    type: InlineButtonActionTypes
    payload: str | None = None
    label: str | None = None
    url: str | None = None
    link: str | None = None
    app_id: int | None = None
    owner_id: int | None = None
    hash: str | None = None

    # TODO: Сделать кастомные ошибки
    @model_validator(mode="after")
    def validate_action(self):
        if self.label is None:
            if self.type in [
                InlineButtonActionTypes.TEXT,
                InlineButtonActionTypes.OPEN_LINK,
                InlineButtonActionTypes.OPEN_APP,
                InlineButtonActionTypes.CALLBACK,
            ]:
                raise ValueError("label is required")

        if self.hash is None:
            if self.type in [InlineButtonActionTypes.VKPAY]:
                raise ValueError("Hash is required")
        if self.url is None:
            if self.type in [
                InlineButtonActionTypes.OPEN_LINK,
                InlineButtonActionTypes.OPEN_APP,
            ]:
                raise ValueError("URL is required")
        if self.link is None:
            if self.type in [
                InlineButtonActionTypes.OPEN_LINK,
                InlineButtonActionTypes.OPEN_APP,
            ]:
                raise ValueError("Link data is required")
        if self.app_id is None:
            if self.type in [InlineButtonActionTypes.OPEN_APP]:
                raise ValueError("App ID is required")
        return self
