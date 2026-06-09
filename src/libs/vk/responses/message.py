from dataclasses import dataclass
@dataclass
class Message:
    id: int
    from_id: int
    date: int
    version:int
    out:int
    fwd_messages:list['Message']
    important:bool
    is_hidden:bool
    # attachments:list['Attachment']
    conversation_message_id:int
    text:str
    peer_id:int
    random_id:int
