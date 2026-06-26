from pydantic import BaseModel

class VKText(BaseModel):
    text: str
    user_id:int