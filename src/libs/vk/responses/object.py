from dataclasses import dataclass
from .message import Message
from .clientInfo import ClientInfo
@dataclass
class Object:
    message: Message
    client_info: ClientInfo