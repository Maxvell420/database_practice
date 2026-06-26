from pydantic import BaseModel


class SendMessageDataResponse(BaseModel):
    response: int
