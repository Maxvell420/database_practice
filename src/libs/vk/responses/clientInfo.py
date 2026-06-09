from dataclasses import dataclass

@dataclass
class ClientInfo:
    button_actions: list[str]
    keyboard: bool
    inline_keyboard: bool
    carousel: bool
    lang_id: int
