from dataclasses import dataclass
@dataclass
class Update:
    group_id: int
    type: str
    event_id:str
    v:str
    
