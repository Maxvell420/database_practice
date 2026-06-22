
from .message import Message
from .clientInfo import ClientInfo
from pydantic import BaseModel
class Object(BaseModel):
    message: Message
    client_info: ClientInfo