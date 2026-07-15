from .message import Message
from .clientInfo import ClientInfo
from pydantic import BaseModel


class Object(BaseModel):
    message: Message | None = None
    client_info: ClientInfo | None = None
    user_id: int | None = None
    peer_id: int | None = None
    event_id: str | None = None
    payload: str | None = None
    conversation_message_id: int | None = None
